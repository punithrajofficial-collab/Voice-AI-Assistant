"""
LLM module. Uses Groq's OpenAI-compatible API to run Llama 3.1
for fast, low-latency text generation (suited to a voice pipeline).
"""
from groq import Groq

from src.config import GROQ_API_KEY, GROQ_MODEL, SYSTEM_PROMPT


class LLMEngine:
    def __init__(self, api_key: str = None, model: str = None):
        if not (api_key or GROQ_API_KEY):
            raise ValueError(
                "GROQ_API_KEY is not set. Add it to your .env file or pass it explicitly."
            )
        self.client = Groq(api_key=api_key or GROQ_API_KEY)
        self.model = model or GROQ_MODEL

    def generate_response(self, user_text: str, chat_history: list = None) -> str:
        """
        Generate a conversational reply.

        Args:
            user_text: the latest user utterance (already transcribed).
            chat_history: list of {"role": "user"/"assistant", "content": str}
                          dicts representing prior turns.

        Returns:
            The assistant's reply text.
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if chat_history:
            messages.extend(chat_history)
        messages.append({"role": "user", "content": user_text})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )
        return completion.choices[0].message.content.strip()
