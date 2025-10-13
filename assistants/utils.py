from typing import Optional

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq


def _get_ollama_provider(
    model: Optional[str] = "llama3.1:8b",
) -> ChatOllama:
    return ChatOllama(
        model=model,
        temperature=0.2,
        num_predict=256,
    )

def _get_groq_provider(
        model: Optional[str] = "llama-3.3-70b-versatile",
) -> ChatGroq:
    return ChatGroq(
        model=model,
        temperature=0.2,
        max_tokens=256,
    )

def get_provider(
        provider_name: str = "groq",
        model: str = "llama-3.3-70b-versatile",
):
    if provider_name=="groq":
        return _get_groq_provider(
            model=model,
        )
    elif provider_name=="ollama":
        return _get_ollama_provider(
            model=model,
        )