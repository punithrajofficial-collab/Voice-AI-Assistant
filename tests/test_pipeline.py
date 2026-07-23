"""
Basic unit tests for the Voice AI Assistant pipeline.
Run with: pytest tests/
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.tts import TextToSpeech
from src.utils import cleanup_file, save_audio_bytes


def test_tts_generates_file():
    tts = TextToSpeech()
    path = tts.synthesize("Hello, this is a test.")
    assert os.path.exists(path)
    assert path.endswith(".mp3")
    cleanup_file(path)
    assert not os.path.exists(path)


def test_tts_empty_text_raises():
    tts = TextToSpeech()
    with pytest.raises(ValueError):
        tts.synthesize("")


def test_tts_whitespace_only_raises():
    tts = TextToSpeech()
    with pytest.raises(ValueError):
        tts.synthesize("   ")


def test_save_and_cleanup_audio_bytes(tmp_path):
    fake_bytes = b"RIFF....WAVEfmt "
    directory = str(tmp_path)
    filepath = save_audio_bytes(fake_bytes, directory=directory, extension="wav")
    assert os.path.exists(filepath)
    with open(filepath, "rb") as f:
        assert f.read() == fake_bytes
    cleanup_file(filepath)
    assert not os.path.exists(filepath)


def test_cleanup_file_on_nonexistent_path_does_not_raise():
    # Should silently no-op, never throw
    cleanup_file("this/path/does/not/exist.wav")
