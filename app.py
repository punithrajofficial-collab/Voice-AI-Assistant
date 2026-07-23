"""
Voice AI Assistant - Streamlit app.

Pipeline: mic recording -> Whisper (STT) -> Groq Llama 3.1 (LLM) -> gTTS (TTS) -> playback
"""
import streamlit as st
from audio_recorder_streamlit import audio_recorder

from src.stt import SpeechToText
from src.llm import LLMEngine
from src.tts import TextToSpeech
from src.utils import save_audio_bytes, cleanup_file

st.set_page_config(page_title="Voice AI Assistant", page_icon="🎙️", layout="centered")


@st.cache_resource(show_spinner="Loading models (first run only)...")
def load_pipeline():
    stt = SpeechToText()
    llm = LLMEngine()
    tts = TextToSpeech()
    return stt, llm, tts


st.title("🎙️ Voice AI Assistant")
st.caption("Speak → Whisper transcribes → Llama 3.1 replies → gTTS speaks back")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("⚙️ Settings")
    st.write("**STT:** faster-whisper (base)")
    st.write("**LLM:** Groq Llama 3.1")
    st.write("**TTS:** gTTS")
    st.divider()
    if st.button("🗑️ Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()

try:
    stt_engine, llm_engine, tts_engine = load_pipeline()
except ValueError as e:
    st.error(f"Configuration error: {e}")
    st.info("Add your GROQ_API_KEY to a .env file (see .env.example) and restart the app.")
    st.stop()

st.subheader("Record your message")
audio_bytes = audio_recorder(
    pause_threshold=2.0,
    text="Click to record",
    recording_color="#e63946",
    neutral_color="#457b9d",
    icon_size="2x",
)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    with st.spinner("Transcribing..."):
        audio_path = save_audio_bytes(audio_bytes, extension="wav")
        user_text = stt_engine.transcribe(audio_path)
        cleanup_file(audio_path)

    if user_text:
        st.markdown(f"**🧑 You said:** {user_text}")

        with st.spinner("Thinking..."):
            reply_text = llm_engine.generate_response(user_text, st.session_state.chat_history)

        st.markdown(f"**🤖 Assistant:** {reply_text}")

        with st.spinner("Generating speech..."):
            audio_reply_path = tts_engine.synthesize(reply_text)

        with open(audio_reply_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True)
        cleanup_file(audio_reply_path)

        st.session_state.chat_history.append({"role": "user", "content": user_text})
        st.session_state.chat_history.append({"role": "assistant", "content": reply_text})
    else:
        st.warning("Could not detect any speech in that recording. Please try again.")

if st.session_state.chat_history:
    st.subheader("💬 Conversation history")
    for msg in st.session_state.chat_history:
        role_label = "🧑 You" if msg["role"] == "user" else "🤖 Assistant"
        st.write(f"**{role_label}:** {msg['content']}")
