from typing import Dict, Optional

from langchain.prompts import PromptTemplate

from assistants.assistant_builder import AssistantBuilder
from assistants.hr_assistant.hr_assistant import HRAssistant
from assistants.logger import get_logger
from assistants.utils import get_provider

logger = get_logger()


class HRAssistantBuilder(AssistantBuilder):

    def __init__(
        self,
        system_instruction_variables: Optional[Dict[str, str]],
        raw_system_instructions: str,
        tools: list,
    ):
        self.raw_system_instructions = raw_system_instructions
        self.system_instruction_variables = system_instruction_variables
        self.tools = tools

    def build(self) -> HRAssistant:

        llm = get_provider()

        logger.debug(
            f"[b d]Binding tools to model: {type(llm)}/{llm.model_name}"
        )

        llm_with_tools = llm.bind_tools(
            self.tools,
        )

        logger.debug(
            "[b d]Rendering HR assistant to the prompt template:\n"
            f"[b d]{self.raw_system_instructions[:100]} ..."
        )

        rendered_system_instructions = self.render_prompt()

        return HRAssistant(
            llm=llm_with_tools,
            system_instructions=rendered_system_instructions,
            tools=self.tools,
        )

    def render_prompt(self) -> str:

        input_variables = list(self.system_instruction_variables.keys())

        return PromptTemplate(
            input_variables=input_variables,
            template=self.raw_system_instructions,
            template_format="f-string",
        ).format(
            **self.system_instruction_variables,
        )
