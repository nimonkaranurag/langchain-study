from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_tavily import TavilySearch
from rich.console import Console

from assistants import init_env
from assistants.react_agent import get_search_agent_react_template
from assistants.react_agent.schemas import SearchAgentResponse
from assistants.utils import get_provider

init_env()

console = Console()

tools = [TavilySearch()]
llm = get_provider()

"""
PROMPT_OWNER_STRING = "hwchase17/react"
react_prompt: PromptTemplate = hub.pull(PROMPT_OWNER_STRING)
"""

output_parser = PydanticOutputParser(
    pydantic_object=SearchAgentResponse,
)

react_prompt = PromptTemplate(
    input_variables=[
        "tools",
        "tool_names",
        "format_instructions",
        "input",
        "agent_scratchpad",
    ],
    template=get_search_agent_react_template(),
    template_format="jinja2",
).partial(format_instructions=output_parser.get_format_instructions())

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt,
)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

response_output_extractor=RunnableLambda(
    lambda response: response["output"]
)

response_output_formatter=RunnableLambda(
    lambda response_output: output_parser.parse(response_output)
)

agent_query_pipeline = \
    agent_executor | response_output_extractor | response_output_formatter

def main():

    user_input = console.input("[b magenta]User🙋🏽‍♂️:")

    formatted_assistant_response: SearchAgentResponse = agent_query_pipeline.invoke(
        input={
            "input": user_input,
        }
    )

    console.print(
        f"[b cyan]Search Assistant🔎:[/b cyan]{formatted_assistant_response.agent_response}"
    )
    console.print(
        f"[b yellow][dim]Sources:{formatted_assistant_response.sources}"
    )


if __name__ == "__main__":
    main()
