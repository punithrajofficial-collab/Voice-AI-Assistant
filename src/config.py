"""
Centralized configuration for the Voice AI Assistant.
All values are overridable via environment variables (.env file).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Groq LLM settings ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# --- Whisper STT settings ---
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")  # tiny/base/small/medium/large-v3
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")  # int8 = fast on CPU

# --- gTTS settings ---
TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")

# --- System behaviour ---
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful, concise voice assistant. Keep answers short (2-4 sentences) "
    "and conversational, since your replies will be spoken aloud to the user."
)

TEMP_AUDIO_DIR = os.getenv("TEMP_AUDIO_DIR", "temp_audio")
