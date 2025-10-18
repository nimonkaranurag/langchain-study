from typing import Dict, Optional

from langchain.prompts import PromptTemplate

from assistants.assistant_builder import AssistantBuilder
from assistants.hr_assistant.hr_assistant import HRAssistant
from assistants.utils import get_provider


class HRAssistantBuilder(AssistantBuilder):

    def __init__(
        self,
        system_instruction_variables: Optional[Dict[str, str]],
        raw_system_instructions: str,
    ):
        self.raw_system_instructions = raw_system_instructions
        self.system_instruction_variables = system_instruction_variables

    def build(self) -> HRAssistant:

        llm = get_provider()
        rendered_system_instructions = self.render_prompt()

        return HRAssistant(
            llm=llm,
            system_instructions=rendered_system_instructions,
        )

    def render_prompt(self) -> str:
        return PromptTemplate(
            input_variables=list(self.system_instruction_variables.keys()),
            template=self.raw_system_instructions,
            template_format="f-string",
        ).format(
            **self.system_instruction_variables,
        )
