import logging
import io
import pygame
from typing import Optional

logger = logging.getLogger(__name__)


class AudioPlayer:
    def __init__(self):
        try:
            pygame.mixer.init()
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize audio player: {e}")
            self.initialized = False

    def play_audio(self, audio_data: bytes) -> bool:
        if not self.initialized:
            logger.warning("Audio player not initialized")
            return False
        
        try:
            audio_stream = io.BytesIO(audio_data)
            pygame.mixer.music.load(audio_stream)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            return True
            
        except Exception as e:
            logger.error(f"Audio playback error: {e}")
            return False

    def stop(self):
        if self.initialized:
            pygame.mixer.music.stop()

    def __del__(self):
        if self.initialized:
            pygame.mixer.quit()
