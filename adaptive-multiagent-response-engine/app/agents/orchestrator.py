from typing import List, Optional, Tuple
from app.agents.agent import Agent
from app.llm.flan import FlanClient
from app.llm.prompts import INTENT_CLASSIFICATION_PROMPT
from app.memory.store import ConversationStore
from app.memory.threads import ThreadInferencer
from app.utils.similarity import SimilarityChecker
from app.config import Config


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
        # Simplified: Use round-robin to reduce LLM calls
        # If last agent spoke, give them priority for continuity
        last_agent_name = self.memory.last_agent
        if last_agent_name:
            for agent in self.agents:
                if agent.name == last_agent_name:
                    # 50% chance to continue with same agent for continuity
                    import random
                    if random.random() < 0.5:
                        return agent
        
        # Otherwise use round-robin
        selected = self.agents[self.round_robin_index]
        self.round_robin_index = (self.round_robin_index + 1) % len(self.agents)
        return selected

    def check_and_regenerate(
        self,
        agent: Agent,
        response: str,
        context: str,
        intent: str,
        strategy: str
    ) -> str:
        recent_outputs = self.memory.get_recent_agent_outputs()

        if self.similarity_checker.is_too_similar(response, recent_outputs):
            # Try up to 2 times to get a unique question
            for attempt in range(2):
                new_response = agent.generate_response(context, intent, strategy)
                if not self.similarity_checker.is_too_similar(new_response, recent_outputs):
                    return new_response
            # If still similar, return it anyway but with variation
            return new_response

        return response

    def process_turn(self, primary_text: str) -> Tuple[str, str, str]:
        if self.config.use_intent_classification:
            intent = self.classify_intent(primary_text)
        else:
            intent = "INFORMATION"  # Default intent for speed
        
        self.memory.add_primary_turn(primary_text, intent)
        self.thread_inferencer.update_if_needed(self.memory)
        context = self.memory.build_context(self.config.max_context_turns)
        selected_agent = self.select_speaking_agent(context, intent)
        strategy = selected_agent.select_strategy(context, intent)
        response = selected_agent.generate_response(context, intent, strategy)
        response = self.check_and_regenerate(selected_agent, response, context, intent, strategy)
        self.memory.add_agent_turn(selected_agent.name, response, strategy)
        # Return the single response - removed double-response bug
        return selected_agent.name, strategy, response

    def run_interaction(self, primary_text: str) -> None:
        try:
            print("Processing...", end="", flush=True)
            agent_name, strategy, response = self.process_turn(primary_text)
            print("\r" + " " * 20 + "\r", end="")  # Clear "Processing..."
            
            # Format agent name as "STUDENT 1", "STUDENT 2", etc.
            student_num = agent_name.split("_")[-1] if "_" in agent_name else "1"
            
            # Make sure response is not empty
            if not response or len(response.strip()) < 3:
                response = "Can you tell me more about that?"
            
            print(f"[STUDENT {student_num}]: {response}\n")
        except Exception as e:
            print(f"\n⚠ Error generating response: {e}")
            print("Trying again...\n")
