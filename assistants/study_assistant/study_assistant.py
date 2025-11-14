from typing import Any, List

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool

from assistants.assistant import Assistant
from assistants.logger import get_logger
from assistants.search_assistant.schemas import SearchAgentResponse

logger = get_logger()

MAX_RETRIES = 5


class AssistantFailedError(Exception):
    pass


class StudyAssistant(Assistant):

    def __init__(
        self,
        llm: Any,
        response_llm: Any,
        system_instructions: str,
        tools: List[BaseTool],
    ):
        self.llm = llm
        self.response_llm = response_llm
        self.system_instructions = system_instructions
        self.conversation_history: List[Any] = [
            SystemMessage(
                content=system_instructions,
            )
        ]
        self.tool_map = {tool.name: tool for tool in tools}

    def query(self, user_input: str) -> SearchAgentResponse:

        logger.debug(
            f"[b d]Sending the user message: {user_input} to the assistant"
        )

        self.conversation_history.append(
            HumanMessage(
                content=user_input,
            )
        )

        logger.debug(
            f"[b d]Entering assistant response loop, max retries set to: {MAX_RETRIES}"
        )

        for _ in range(MAX_RETRIES):

            assistant_response: AIMessage = self.llm.invoke(
                self.conversation_history,
            )

            self.conversation_history.append(
                assistant_response,
            )

            if not assistant_response.tool_calls:

                logger.debug(
                    f"[b d]A text response was returned by the assistant"
                )

                structured_response = self.response_llm.invoke(
                    [
                        SystemMessage(
                            content="Format the response according to the schema"
                        ),
                        HumanMessage(content=assistant_response.content),
                    ]
                )

                return structured_response

            for tool_call in assistant_response.tool_calls:

                logger.debug(
                    f"[b d]Trying to execute the following tool: {tool_call} recommended by the assistant"
                )

                tool_response: ToolMessage = self._execute_tool(tool_call)

                logger.debug(
                    f"[d b]The following response was returned by the tool: {tool_response}"
                )

                self.conversation_history.append(
                    tool_response,
                )

        logger.error(
            f"[b d]Assistant failed after {MAX_RETRIES} retries.\n"
            f"[b d]Last response contained tool calls: {assistant_response.tool_calls}"
        )

        raise AssistantFailedError("Failed to process request.")

    def _execute_tool(self, tool_call: dict) -> ToolMessage:

        tool_name = tool_call["name"]

        try:

            selected_tool = self.tool_map[tool_name]

            logger.debug(f"[b d]Invoking tool: {selected_tool.name}")

            return selected_tool.invoke(
                tool_call,
            )

        except Exception as e:

            tool_id = tool_call["id"]
            tool_args = tool_call["args"]

            logger.error(
                f"[b d]Failed to execute the tool with id: {tool_id}\n"
                f"[b d]Tool name: {tool_name}\n"
                f"[b d]Tool args: {tool_args}\n"
                f"[b d]The following error was encountered: {e}"
            )

            return ToolMessage(
                content=f"Error executing {tool_name}: {str(e)}",
                tool_call_id=tool_id,
            )
