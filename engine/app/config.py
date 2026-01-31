import os
import torch


class Config:
    openrouter_model: str = "openai/gpt-3.5-turbo"
    flan_model: str = "google/flan-t5-large"
    whisper_model: str = "tiny"
    num_agents: int = 3
    single_person_mode: bool = False
    silence_threshold: float = 200.0
    silence_duration: float = 1.25
    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    max_context_turns: int = 20
    similarity_threshold: float = 0.6
    similarity_window: int = 5
    thread_update_interval: int = 3
    use_intent_classification: bool = False
    debug: bool = False
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    enable_tts: bool = True
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY", "")
    elevenlabs_voice_id: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    tts_timeout: float = 10.0
    
    student_voices: list = [
        "21m00Tcm4TlvDq8ikWAM",
        "AZnzlk1XvdvUeBnXmlld",
        "EXAVITQu4vr4xnSDxMaL",
        "ErXwobaYiN019PkySvjV",
        "MF3mGyEYCl7XYWbV9V6O",
        "TxGEqnHWrfWFTfGW9XjX"
    ]
