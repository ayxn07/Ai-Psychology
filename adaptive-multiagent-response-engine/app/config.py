import torch


class Config:
    # OpenRouter model - change this to try different AI models
    # See all models: https://openrouter.ai/models
    # 
    # Recommended options:
    #   - "anthropic/claude-3.5-sonnet" (best quality, $3/M tokens)
    #   - "openai/gpt-4o-mini" (fast, cheap, $0.15/M tokens)
    #   - "openai/gpt-3.5-turbo" (fast, cheap, $0.50/M tokens)
    #   - "meta-llama/llama-3.1-70b-instruct:free" (free, good)
    #   - "google/gemini-flash-1.5:free" (free, fast)
    openrouter_model: str = "openai/gpt-3.5-turbo"
    
    # FLAN-T5 settings (fallback only, poor quality)
    flan_model: str = "google/flan-t5-large"
    
    # Whisper ASR settings
    whisper_model: str = "tiny"
    
    # Agent settings
    num_agents: int = 3
    
    # Audio settings
    silence_threshold: float = 200.0
    silence_duration: float = 2.0
    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    
    # Memory settings
    max_context_turns: int = 20
    similarity_threshold: float = 0.6
    similarity_window: int = 5
    thread_update_interval: int = 3
    
    # Performance optimization
    use_intent_classification: bool = False  # Set False for faster responses
    
    # Debug mode
    debug: bool = False  # Set True to see what's happening
    
    # Device
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
