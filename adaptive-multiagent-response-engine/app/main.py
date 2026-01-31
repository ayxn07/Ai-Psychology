import os
import sys
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

    print(f"Loading FLAN-T5 ({config.flan_model})...")
    flan_client = FlanClient(config)

    memory = ConversationStore(similarity_window=config.similarity_window)
    thread_inferencer = ThreadInferencer(
        update_interval=config.thread_update_interval
    )
    similarity_checker = SimilarityChecker(threshold=config.similarity_threshold)

    agents = []
    for i in range(config.num_agents):
        agent_name = f"Agent_{i + 1}"
        agent = Agent(name=agent_name, flan_client=flan_client)
        agents.append(agent)

    orchestrator = Orchestrator(
        agents=agents,
        flan_client=flan_client,
        memory=memory,
        thread_inferencer=thread_inferencer,
        similarity_checker=similarity_checker,
        config=config
    )

    print("Initializing audio recorder...")
    recorder = AudioRecorder(config)

    print("\n" + "=" * 50)
    print("System ready. Speak to interact.")
    print("Press Ctrl+C to exit.")
    print("=" * 50 + "\n")

    try:
        while True:
            wav_path = recorder.record_utterance()
            if not wav_path:
                continue
            try:
                transcript = asr.transcribe(wav_path)
            finally:
                if os.path.exists(wav_path):
                    os.remove(wav_path)
            if is_trivial(transcript):
                continue
            print(f"[PRIMARY]: {transcript}")
            orchestrator.run_interaction(transcript)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        recorder.cleanup()
        print("Goodbye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
