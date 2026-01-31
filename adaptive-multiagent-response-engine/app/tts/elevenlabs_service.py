import logging
from typing import Optional
from elevenlabs import ElevenLabs

logger = logging.getLogger(__name__)


class ElevenLabsTTSService:
    def __init__(
        self,
        api_key: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        timeout: int = 30,
        tts_enabled: bool = True
    ):
        self.api_key = api_key
        self.voice_id = voice_id
        self.timeout = timeout
        self.tts_enabled = tts_enabled
        self.client = ElevenLabs(api_key=api_key)

    def text_to_speech(self, text: str, voice_id: str = None, language: str = "English") -> Optional[bytes]:
        if not self.tts_enabled:
            return None
        
        use_voice = voice_id if voice_id else self.voice_id
        
        if language.lower() == "english" or language.lower() == "en":
            model_id = "eleven_turbo_v2_5"
        else:
            model_id = "eleven_multilingual_v2"
        
        try:
            audio_generator = self.client.text_to_speech.convert(
                voice_id=use_voice,
                text=text,
                model_id=model_id
            )
            
            audio_data = b"".join(audio_generator)
            return audio_data
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return None
