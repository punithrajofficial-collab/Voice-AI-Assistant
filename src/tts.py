"""
Text-to-Speech module using gTTS (Google Text-to-Speech).
Chosen because it needs no local audio drivers/models, which makes it
reliable on Streamlit Community Cloud and inside minimal Docker images.
"""
import os
import uuid

from gtts import gTTS

from src.config import TTS_LANGUAGE, TEMP_AUDIO_DIR


class TextToSpeech:
    def __init__(self, language: str = None, output_dir: str = None):
        self.language = language or TTS_LANGUAGE
        self.output_dir = output_dir or TEMP_AUDIO_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def synthesize(self, text: str) -> str:
        """
        Convert text into an mp3 file and return its filepath.

        Raises:
            ValueError: if text is empty.
        """
        if not text or not text.strip():
            raise ValueError("Text for speech synthesis cannot be empty.")

        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(self.output_dir, filename)

        tts = gTTS(text=text, lang=self.language)
        tts.save(filepath)
        return filepath
