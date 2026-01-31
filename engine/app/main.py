import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app.config import Config
from app.audio.recorder import AudioRecorder
from app.asr.whisper_asr import WhisperASR
from app.llm.flan import FlanClient
from app.memory.store import ConversationStore
from app.memory.threads import ThreadInferencer
from app.agents.agent import Agent
from app.agents.orchestrator import Orchestrator
from app.utils.similarity import SimilarityChecker


def is_trivial(text: str) -> bool:
    if not text:
        return True
    cleaned = text.strip().lower()
    if len(cleaned) < 3:
        return True
    trivial_phrases = {"", "um", "uh", "hmm", "hm", "ah", "oh", "okay", "ok"}
    if cleaned in trivial_phrases:
        return True
    return False


def main():
    print("Initializing Adaptive Multi-Agent Response Engine...")

    config = Config()

    print(f"Loading Whisper ASR ({config.whisper_model})...")
    asr = WhisperASR(config)

    print(f"Loading LLM...")
    from app.llm.llm_manager import LLMManager
    llm_manager = LLMManager(config)
    print(f"✓ Using {llm_manager.get_client_name()} for question generation")

    memory = ConversationStore(similarity_window=config.similarity_window)
    thread_inferencer = ThreadInferencer(
        update_interval=config.thread_update_interval
    )
    similarity_checker = SimilarityChecker(threshold=config.similarity_threshold)

    actual_num_agents = 1 if config.single_person_mode else config.num_agents
    
    agents = []
    for i in range(actual_num_agents):
        if config.single_person_mode:
            agent_name = "Interviewer"
        else:
            agent_name = f"Student_{i + 1}"
        agent = Agent(name=agent_name, flan_client=llm_manager)
        agents.append(agent)

    orchestrator = Orchestrator(
        agents=agents,
        flan_client=llm_manager,
        memory=memory,
        thread_inferencer=thread_inferencer,
        similarity_checker=similarity_checker,
        config=config
    )

    print("Initializing audio recorder...")
    recorder = AudioRecorder(config)

    print("\n" + "=" * 50)
    if config.single_person_mode:
        print("SINGLE PERSON INTERVIEW MODE")
        print("=" * 50)
        print("One interviewer will interact with you.")
    else:
        print("THERAPY TRAINING SIMULATION")
        print("=" * 50)
        print("You are the PATIENT. Speak about your concerns.")
        print("Student therapists will ask questions to learn.")
    print("Press Ctrl+C to exit.")
    print("=" * 50 + "\n")

    try:
        while True:
            wav_path = recorder.record_utterance()
            if not wav_path:
                continue
            try:
                transcript, detected_language = asr.transcribe(wav_path)
            finally:
                if os.path.exists(wav_path):
                    os.remove(wav_path)
            if is_trivial(transcript):
                continue
            print(f"[PATIENT]: {transcript}")
            orchestrator.run_interaction(transcript, detected_language)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        recorder.cleanup()
        print("Goodbye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
