import os
from typing import Optional


class OpenRouterClient:
    """
    OpenRouter API client - access to many models through one API.
    Supports GPT-4, Claude, Llama, Mistral, and many more.
    Get key from: https://openrouter.ai/keys
    """
    
    def __init__(self, model: str = "anthropic/claude-3.5-sonnet", api_key: Optional[str] = None):
        try:
            from openai import OpenAI
            
            # Get API key from parameter or environment
            key = api_key or os.getenv("OPENROUTER_API_KEY")
            
            if not key:
                raise ValueError("OPENROUTER_API_KEY not set")
            
            # OpenRouter uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=key,
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = model
            self.available = True
            print(f"✓ OpenRouter initialized with {model}")
        except ImportError:
            print("⚠ OpenAI package not installed. Run: pip install openai")
            self.available = False
        except ValueError as e:
            print(f"⚠ {e}")
            print("  Set environment variable: $env:OPENROUTER_API_KEY='sk-or-v1-...'")
            print("  Get your key from: https://openrouter.ai/keys")
            self.available = False
        except Exception as e:
            print(f"⚠ OpenRouter initialization failed: {e}")
            print("  Get your key from: https://openrouter.ai/keys")
            self.available = False
    
    def generate(self, prompt: str, max_new_tokens: int = 128, temperature: float = 0.7) -> str:
        if not self.available:
            return "Can you tell me more about that?"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a student therapist learning to ask therapeutic questions. Keep responses brief and always ask questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_new_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            return "What are your thoughts on that?"
