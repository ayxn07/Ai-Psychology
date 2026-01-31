from faster_whisper import WhisperModel
from app.config import Config


class WhisperASR:
    def __init__(self, config: Config):
        self.config = config
        compute_type = "float16" if config.device == "cuda" else "int8"
        self.model = WhisperModel(
            config.whisper_model,
            device=config.device,
            compute_type=compute_type
        )

    def transcribe(self, wav_path: str) -> str:
        segments, _ = self.model.transcribe(wav_path, beam_size=5)
        text_parts = []
        for segment in segments:
            text_parts.append(segment.text.strip())
        return " ".join(text_parts).strip()
