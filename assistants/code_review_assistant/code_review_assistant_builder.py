"""
Builder for the Code Review Assistant.
"""
from typing import Any

try:
    from assistants.assistant_builder import AssistantBuilder
except Exception:
    from assistants.assistant_builder import AssistantBuilder  # type: ignore

from .code_review_assistant import CodeReviewAssistant
from .tools import analyze_code, check_pep8


class CodeReviewAssistantBuilder(AssistantBuilder):
    def __init__(self):
        super().__init__()
        # System prompt focused on code review
        self.set_system_prompt(
            "You are a Python code review assistant. Provide clear, concise, and actionable feedback."
        )

    def register_default_tools(self) -> None:
        self.register_tool("analyze_code", analyze_code)
        self.register_tool("check_pep8", check_pep8)

    def build(self) -> CodeReviewAssistant:
        self.register_default_tools()
        assistant = CodeReviewAssistant()
        # If the assistant needs the prompt or tools, set attributes
        assistant.system_prompt = self.system_prompt
        assistant.tools = self.tools
        return assistant
