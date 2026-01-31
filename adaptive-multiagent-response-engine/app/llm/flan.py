import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.config import Config


class FlanClient:
    def __init__(self, config: Config):
        self.config = config
        self.device = torch.device(config.device)
        self.tokenizer = AutoTokenizer.from_pretrained(config.flan_model)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(config.flan_model).to(self.device)
        self.model.eval()

    def generate(self, prompt: str, max_new_tokens: int = 128, temperature: float = 0.7) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                num_beams=1 if temperature > 0 else 4,
                early_stopping=True
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.strip()
