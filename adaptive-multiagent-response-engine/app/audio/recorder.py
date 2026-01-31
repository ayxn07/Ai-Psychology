import pyaudio
import numpy as np
import wave
import tempfile
import os
from app.config import Config


class AudioRecorder:
    def __init__(self, config: Config):
        self.config = config
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16

    def calculate_rms(self, data: bytes) -> float:
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        if len(audio_data) == 0:
            return 0.0
        return np.sqrt(np.mean(audio_data ** 2))


    def record_utterance(self) -> str:
        stream = self.audio.open(
            format=self.format,
            channels=self.config.channels,
            rate=self.config.sample_rate,
            input=True,
            frames_per_buffer=self.config.chunk_size
        )

        frames = []
        silent_chunks = 0
        chunks_per_second = self.config.sample_rate / self.config.chunk_size
        max_silent_chunks = int(self.config.silence_duration * chunks_per_second)
        started = False
        max_seconds = 5
        max_chunks = int(max_seconds * chunks_per_second)
        chunk_count = 0

        print("Listening (max 5s)... Speak now!")

        while chunk_count < max_chunks:
            data = stream.read(self.config.chunk_size, exception_on_overflow=False)
            rms = self.calculate_rms(data)
            chunk_count += 1

            frames.append(data)

            if rms > self.config.silence_threshold:
                started = True
                silent_chunks = 0
            elif started:
                silent_chunks += 1
                if silent_chunks >= max_silent_chunks:
                    break

        stream.stop_stream()
        stream.close()

        if not frames or not started:
            return ""

        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_path = temp_file.name
        temp_file.close()

        with wave.open(temp_path, "wb") as wf:
            wf.setnchannels(self.config.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.config.sample_rate)
            wf.writeframes(b"".join(frames))

        return temp_path

    def cleanup(self):
        self.audio.terminate()
