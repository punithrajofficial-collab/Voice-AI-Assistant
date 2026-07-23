"""
Shared utility helpers used across the Streamlit app and FastAPI service.
"""
import os
import uuid


def cleanup_file(filepath: str) -> None:
    """Delete a temp file if it exists; never raises."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except OSError:
        pass


def save_audio_bytes(audio_bytes: bytes, directory: str = "temp_audio", extension: str = "wav") -> str:
    """Persist raw audio bytes (e.g. from a mic recorder widget) to disk and return the path."""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, f"{uuid.uuid4().hex}.{extension}")
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    return filepath
