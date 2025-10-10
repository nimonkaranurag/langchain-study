from typing import Optional

from langchain_ollama.chat_models import ChatOllama


def get_ollama_provider(
    model: Optional[str] = "llama3.1:8b",
) -> ChatOllama:
    return ChatOllama(
        model=model,
        temperature=0.7,
        num_predict=500,
    )
