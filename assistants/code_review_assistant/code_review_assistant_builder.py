"""
Builder for the Code Review Assistant.
"""
from typing import Any, Optional
from langchain.prompts import PromptTemplate

from assistants.assistant_builder import AssistantBuilder
from assistants.logger import get_logger
from assistants.utils import get_provider

from .code_review_assistant import CodeReviewAssistant
from .tools import analyze_code, check_pep8

logger = get_logger()


class CodeReviewAssistantBuilder(AssistantBuilder):
    """Builder following repo conventions. Mirrors other assistant builders.
    Accepts raw system instruction and tool list, and returns a configured assistant.
    """

    def __init__(
        self,
        raw_system_instructions: str = "You are a Python code review assistant. Provide clear, concise, and actionable feedback.",
        system_instruction_variables: Optional[dict] = None,
        tools: Optional[list] = None,
    ) -> None:
        self.raw_system_instructions = raw_system_instructions
        self.system_instruction_variables = system_instruction_variables or {}
        self.tools = tools or []

    def register_default_tools(self):
        # register local analysis tools if tools weren't provided
        if not self.tools:
            self.tools = [analyze_code, check_pep8]

    def render_prompt(self) -> str:
        # Use PromptTemplate to render template variables if any
        variables = list(self.system_instruction_variables.keys())
        prompt = PromptTemplate(
            input_variables=variables,
            template=self.raw_system_instructions,
            template_format="f-string",
        ).format(**self.system_instruction_variables) if variables else self.raw_system_instructions
        return prompt

    def build(self) -> CodeReviewAssistant:
        # Ensure default tools present
        self.register_default_tools()

        llm = get_provider()
        # If the LLM supports binding tools, bind them (safe-run)
        try:
            llm_with_tools = llm.bind_tools(self.tools)
        except Exception:
            logger.debug("LLM provider doesn't support bind_tools or failed; using raw llm")
            llm_with_tools = llm

        assistant = CodeReviewAssistant(
            llm=llm_with_tools,
            system_instructions=self.render_prompt(),
            tools=self.tools,
        )
        return assistant
