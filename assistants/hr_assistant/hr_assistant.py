from typing import List, Tuple

from langchain_ollama.chat_models import ChatOllama

from assistants.assistant import Assistant


class HRAssistant(Assistant):

    def __init__(
        self,
        llm: ChatOllama,
        system_instructions: str,
    ):
        self.llm = llm
        self.system_instructions = system_instructions
        self.conversation_history: List[Tuple[str, str]] = [
            (
                "system",
                system_instructions,
            )
        ]

    def query(self, user_input: str) -> str:

        self._update_conversation_history(
            "user",
            user_input,
        )

        assistant_response = self.llm.invoke(self.conversation_history).content

        self._update_conversation_history(
            "assistant",
            assistant_response,
        )

        return assistant_response

    def _update_conversation_history(self, role: str, message: str):
        self.conversation_history.append(
            (role, message),
        )
