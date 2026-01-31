import torch


class Config:
    whisper_model: str = "tiny"
    flan_model: str = "google/flan-t5-large"
    num_agents: int = 3
    silence_threshold: float = 200.0
    silence_duration: float = 2.0
    max_context_turns: int = 20
    similarity_threshold: float = 0.6
    similarity_window: int = 5
    thread_update_interval: int = 3
    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
