from typing import List, Optional, Tuple
from app.agents.agent import Agent
from app.llm.flan import FlanClient
from app.llm.prompts import INTENT_CLASSIFICATION_PROMPT
from app.memory.store import ConversationStore
from app.memory.threads import ThreadInferencer
from app.utils.similarity import SimilarityChecker
from app.config import Config
from app.tts.elevenlabs_service import ElevenLabsTTSService
from app.tts.audio_player import AudioPlayer
import logging

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(
        self,
        agents: List[Agent],
        flan_client: FlanClient,
        memory: ConversationStore,
        thread_inferencer: ThreadInferencer,
        similarity_checker: SimilarityChecker,
        config: Config
    ):
        self.agents = agents
        self.flan_client = flan_client
        self.memory = memory
        self.thread_inferencer = thread_inferencer
        self.similarity_checker = similarity_checker
        self.config = config
        self.round_robin_index = 0
        self.tts_service: Optional[ElevenLabsTTSService] = None
        self.audio_player: Optional[AudioPlayer] = None
        self.agent_voice_map = {}
        self.detected_language = "English"
        
        if not self.config.single_person_mode:
            for i, agent in enumerate(agents):
                voice_index = i % len(self.config.student_voices)
                self.agent_voice_map[agent.name] = self.config.student_voices[voice_index]
        
        if self.config.enable_tts:
            if self.config.elevenlabs_api_key:
                try:
                    self.tts_service = ElevenLabsTTSService(
                        api_key=self.config.elevenlabs_api_key,
                        voice_id=self.config.elevenlabs_voice_id,
                        timeout=self.config.tts_timeout,
                        tts_enabled=self.config.enable_tts
                    )
                    self.audio_player = AudioPlayer()
                    logger.info("TTS service initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize TTS service: {e}")
                    self.tts_service = None
                    self.audio_player = None
            else:
                logger.warning("TTS enabled but ELEVENLABS_API_KEY not configured - TTS disabled")

    def classify_intent(self, text: str) -> str:
        prompt = INTENT_CLASSIFICATION_PROMPT.format(text=text)
        response = self.flan_client.generate(prompt, max_new_tokens=16, temperature=0.1)
        intent = response.strip().upper()

        valid_intents = [
            "INFORMATION", "EMOTIONAL_EXPRESSION", "REQUEST_REPEAT",
            "REQUEST_CLARIFICATION", "DEFENSIVE", "ELABORATION", "QUESTION"
        ]

        for valid in valid_intents:
            if valid in intent:
                return valid

        return "INFORMATION"

    def select_speaking_agent(self, context: str, intent: str) -> Agent:
        last_agent_name = self.memory.last_agent
        if last_agent_name:
            for agent in self.agents:
                if agent.name == last_agent_name:
                    import random
                    if random.random() < 0.5:
                        return agent
        
        selected = self.agents[self.round_robin_index]
        self.round_robin_index = (self.round_robin_index + 1) % len(self.agents)
        return selected

    def check_and_regenerate(
        self,
        agent: Agent,
        response: str,
        context: str,
        intent: str,
        strategy: str,
        language: str
    ) -> str:
        recent_outputs = self.memory.get_recent_agent_outputs()

        if self.similarity_checker.is_too_similar(response, recent_outputs):
            for attempt in range(2):
                new_response = agent.generate_response(context, intent, strategy, language)
                if not self.similarity_checker.is_too_similar(new_response, recent_outputs):
                    return new_response
            return new_response

        return response

    def process_turn(self, primary_text: str, detected_language: str = "English") -> Tuple[str, str, str]:
        self.detected_language = detected_language
        
        if self.config.use_intent_classification:
            intent = self.classify_intent(primary_text)
        else:
            intent = "INFORMATION"
        
        self.memory.add_primary_turn(primary_text, intent)
        self.thread_inferencer.update_if_needed(self.memory)
        context = self.memory.build_context(self.config.max_context_turns)
        selected_agent = self.select_speaking_agent(context, intent)
        strategy = selected_agent.select_strategy(context, intent)
        response = selected_agent.generate_response(context, intent, strategy, detected_language)
        response = self.check_and_regenerate(selected_agent, response, context, intent, strategy, detected_language)
        self.memory.add_agent_turn(selected_agent.name, response, strategy)
        return selected_agent.name, strategy, response

    def run_interaction(self, primary_text: str, detected_language: str = "English") -> None:
        try:
            print("Processing...", end="", flush=True)
            agent_name, strategy, response = self.process_turn(primary_text, detected_language)
            print("\r" + " " * 20 + "\r", end="", flush=True)
            
            if agent_name == "Interviewer":
                display_name = "INTERVIEWER"
            else:
                student_num = agent_name.split("_")[-1] if "_" in agent_name else "1"
                display_name = f"STUDENT {student_num}"
            
            if not response or len(response.strip()) < 3:
                response = "Can you tell me more about that?"
            
            if self.tts_service and self.audio_player:
                try:
                    print("Generating audio...", end="", flush=True)
                    
                    voice_id = None
                    if not self.config.single_person_mode and agent_name in self.agent_voice_map:
                        voice_id = self.agent_voice_map[agent_name]
                    
                    audio_data = self.tts_service.text_to_speech(response, voice_id=voice_id, language=detected_language)
                    print("\r" + " " * 20 + "\r", end="", flush=True)
                    if audio_data:
                        self.audio_player.play_audio(audio_data)
                except Exception as e:
                    print("\r" + " " * 20 + "\r", end="", flush=True)
                    logger.error(f"TTS_ERROR [RUNTIME]: Error during TTS processing: {e}")
            
            print(f"[{display_name}]: {response}\n")
        except Exception as e:
            print(f"\n⚠ Error generating response: {e}")
            print("Trying again...\n")
