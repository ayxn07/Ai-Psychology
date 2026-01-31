import logging
from typing import Optional
from elevenlabs import ElevenLabs
import os
from datetime import datetime
import wave
import struct

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
        
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

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
                model_id=model_id,
                output_format="pcm_44100"
            )
            
            audio_data = b"".join(audio_generator)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            wav_filename = f"tts_{timestamp}.wav"
            wav_filepath = os.path.join(self.temp_dir, wav_filename)
            
            with wave.open(wav_filepath, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                wav_file.writeframes(audio_data)
            
            logger.info(f"Saved TTS audio to {wav_filepath}")
            
            return audio_data
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return None





