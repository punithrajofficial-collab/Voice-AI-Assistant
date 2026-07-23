"""
Voice AI Assistant - FastAPI backend.

Exposes the STT -> LLM -> TTS pipeline as REST endpoints so it can be
consumed by any frontend (mobile app, web app, curl, Postman, etc.).

Run with: uvicorn api:app --host 0.0.0.0 --port 8000
"""
import os
from typing import List, Dict

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from src.stt import SpeechToText
from src.llm import LLMEngine
from src.tts import TextToSpeech
from src.utils import cleanup_file

app = FastAPI(
    title="Voice AI Assistant API",
    description="Speech-to-Text -> LLM -> Text-to-Speech pipeline",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stt_engine = SpeechToText()
llm_engine = LLMEngine()
tts_engine = TextToSpeech()

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)


class ChatRequest(BaseModel):
    text: str
    chat_history: List[Dict[str, str]] = []


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Upload an audio file and get back its transcription."""
    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        text = stt_engine.transcribe(temp_path)
    finally:
        cleanup_file(temp_path)
    return {"transcription": text}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send text + optional chat history, get back the LLM's reply."""
    reply = llm_engine.generate_response(request.text, request.chat_history)
    return ChatResponse(reply=reply)


@app.post("/speak")
async def speak(request: ChatRequest):
    """Send text, get back an mp3 audio file of it being spoken."""
    audio_path = tts_engine.synthesize(request.text)
    return FileResponse(audio_path, media_type="audio/mpeg", filename="reply.mp3")


@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    """
    Full pipeline in one call: upload audio -> transcription -> LLM reply
    -> returns both the reply text and a path to the spoken mp3 reply.
    """
    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        user_text = stt_engine.transcribe(temp_path)
        if not user_text:
            raise HTTPException(status_code=400, detail="No speech detected in audio.")
        reply_text = llm_engine.generate_response(user_text)
        audio_reply_path = tts_engine.synthesize(reply_text)
    finally:
        cleanup_file(temp_path)

    return JSONResponse({
        "transcription": user_text,
        "reply": reply_text,
        "audio_reply_path": audio_reply_path,
    })


@app.get("/download-audio/{filename}")
async def download_audio(filename: str):
    """Fetch a previously generated TTS mp3 by filename."""
    filepath = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(filepath, media_type="audio/mpeg", filename=filename)
