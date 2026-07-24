"""
Speech-to-Text module.
Uses faster-whisper (CTranslate2 backend) for fast CPU/GPU transcription.
"""
from faster_whisper import WhisperModel

from src.config import WHISPER_MODEL_SIZE, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE


class SpeechToText:
    def __init__(self, model_size: str = None, device: str = None, compute_type: str = None):
        self.model_size = model_size or WHISPER_MODEL_SIZE
        self.device = device or WHISPER_DEVICE
        self.compute_type = compute_type or WHISPER_COMPUTE_TYPE
        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )

    def transcribe(self, audio_path: str, language: str = "en") -> str:
        """
        Transcribe an audio file (wav/mp3/m4a/etc.) to text.

        Args:
            audio_path: path to the audio file on disk.
            language: optional ISO language code to force (e.g. "en").
                      If None, Whisper auto-detects the language.

        Returns:
            The transcribed text, stripped of leading/trailing whitespace.
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=True,  # skip silence, improves accuracy on short recordings
        )
        text = " ".join(segment.text.strip() for segment in segments)
        return text.strip()
