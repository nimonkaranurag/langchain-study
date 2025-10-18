from typing import Optional

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from assistants.logger import get_logger

logger = get_logger()


class ProviderCallbackHandler(BaseCallbackHandler):

    def on_chat_model_start(
        self,
        serialized,
        messages,
        *,
        run_id,
        parent_run_id=None,
        tags=None,
        metadata=None,
        **kwargs,
    ):

        conversation_preview = "\n".join(
            message.content[:50] for message in messages[0]
        )

        logger.debug(
            f"[b d]Chat Model Run Started: {serialized.get('name', 'unknown')}\n"
            f"[b d]Conversation History:{conversation_preview}",
        )

        if metadata:
            logger.debug(
                f"[b d]Metadata: {metadata}",
            )

        if tags:
            logger.debug(f"[b d]Tags: {tags}")

    def on_llm_end(self, response, *, run_id, parent_run_id=None, **kwargs):

        if response.generations:
            logger.debug(f"[b d]Response generated: {response.generations}")

        if hasattr(response, "llm_output") and response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})

            if token_usage:
                logger.debug(f"[b d]Token Usage: {token_usage}")


def _get_ollama_provider(
    model: Optional[str] = "llama3.1:8b",
) -> ChatOllama:
    return ChatOllama(
        model=model,
        temperature=0.2,
        num_predict=256,
        callbacks=[
            ProviderCallbackHandler(),
        ],
    )


def _get_groq_provider(
    model: Optional[str] = "llama-3.3-70b-versatile",
) -> ChatGroq:
    return ChatGroq(
        model=model,
        temperature=0.2,
        max_tokens=256,
        callbacks=[
            ProviderCallbackHandler(),
        ],
    )


def get_provider(
    provider_name: str = "groq",
    model: str = "llama-3.3-70b-versatile",
):
    if provider_name == "groq":
        return _get_groq_provider(
            model=model,
        )
    elif provider_name == "ollama":
        return _get_ollama_provider(
            model=model,
        )
