from typing import Optional

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_tavily import TavilySearch
from pydantic import BaseModel

from assistants.assistant_builder import AssistantBuilder
from assistants.logger import get_logger
from assistants.react_agent.schemas import SearchAgentResponse
from assistants.react_agent.search_assistant import SearchAssistant
from assistants.utils import get_provider

PROMPT_OWNER_STRING = "hwchase17/react"
react_prompt: PromptTemplate = hub.pull(PROMPT_OWNER_STRING)

logger = get_logger()


class SearchAssistantBuilder(AssistantBuilder):

    def __init__(self, prompt_template: Optional[PromptTemplate] = react_prompt):
        self.prompt_template = prompt_template

    def build(
        self,
        output_schema: Optional[type[BaseModel]] = None,
        tools: Optional[list] = None,
    ) -> SearchAssistant:

        if output_schema is None:
            logger.info(
                "[b d]Using default `SearchAgentResponse` output schema for formatting output response"
            )
            output_schema = SearchAgentResponse

        if tools is None:
            logger.info(
                "[b d]Using default `TavilySearch()` tool for the assistant's search engine"
            )
            tools = [
                TavilySearch(),
            ]

        llm = get_provider()
        structured_llm = llm.with_structured_output(
            schema=output_schema,
        )

        agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=self.prompt_template,
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
        )

        response_output_extractor = RunnableLambda(lambda response: response["output"])

        logger.info("[b d]Creating an assistant query pipeline")
        assistant_query_pipeline = (
            agent_executor | response_output_extractor | structured_llm
        )

        return SearchAssistant(
            assistant_query_pipeline=assistant_query_pipeline,
        )
