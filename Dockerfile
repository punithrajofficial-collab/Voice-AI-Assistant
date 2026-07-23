FROM python:3.11-slim

WORKDIR /app

# ffmpeg is required by faster-whisper/gTTS for audio decoding/encoding
# libsndfile1 is required by the soundfile package
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p temp_audio

EXPOSE 8501
EXPOSE 8000

# Default: run the Streamlit UI. Override CMD to run the FastAPI service instead:
#   docker run <image> uvicorn api:app --host 0.0.0.0 --port 8000
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
