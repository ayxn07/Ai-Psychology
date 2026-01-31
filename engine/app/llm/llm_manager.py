from typing import Optional
from app.config import Config


class LLMManager:
    
    def __init__(self, config: Config):
        self.config = config
        self.client = None
        self.client_name = "none"
        
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            from app.llm.openrouter_client import OpenRouterClient
            client = OpenRouterClient(model=self.config.openrouter_model)
            if client.available:
                self.client = client
                self.client_name = "OpenRouter"
                return
        except Exception as e:
            print(f"Could not initialize OpenRouter: {e}")
        
        print("⚠ WARNING: Using FLAN-T5 (poor quality).")
        print("  Set OPENROUTER_API_KEY for best quality")
        print("  Get key from: https://openrouter.ai/keys")
        
        from app.llm.flan import FlanClient
        self.client = FlanClient(self.config)
        self.client_name = "FLAN-T5"
    
    def generate(self, prompt: str, max_new_tokens: int = 128, temperature: float = 0.7) -> str:
        return self.client.generate(prompt, max_new_tokens, temperature)
    
    def get_client_name(self) -> str:
        return self.client_name
