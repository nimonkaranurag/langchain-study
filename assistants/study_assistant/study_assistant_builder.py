from typing import Dict, Optional

from langchain.prompts import PromptTemplate

from assistants.assistant_builder import AssistantBuilder
from assistants.logger import get_logger
from assistants.search_assistant.schemas import SearchAgentResponse
from assistants.study_assistant.study_assistant import StudyAssistant
from assistants.utils import get_provider

logger = get_logger()


class StudyAssistantBuilder(AssistantBuilder):

    def __init__(
        self,
        raw_system_instructions: str,
        tools: list,
        system_instruction_variables: Optional[Dict[str, str]] = None,
    ):
        self.raw_system_instructions = raw_system_instructions
        self.system_instruction_variables = system_instruction_variables
        self.tools = tools

    def build(self) -> StudyAssistant:

        llm = get_provider()

        logger.debug(
            f"[b d]Binding tools to model: {type(llm)}/{llm.model_name}"
        )

        llm_with_tools = llm.bind_tools(
            self.tools,
        )

        llm_with_structured_output = llm.with_structured_output(
            schema=SearchAgentResponse,
        )

        logger.debug(
            "[b d]Rendering Study assistant input variables to the prompt template:\n"
            f"[b d]{self.raw_system_instructions[:100]} ..."
        )

        rendered_system_instructions = self.render_prompt()

        return StudyAssistant(
            llm=llm_with_tools,
            response_llm=llm_with_structured_output,
            system_instructions=rendered_system_instructions,
            tools=self.tools,
        )

    def render_prompt(self) -> str:

        return self.raw_system_instructions
