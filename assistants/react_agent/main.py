from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_tavily import TavilySearch
from rich.console import Console

from assistants import init_env
from assistants.react_agent.resources.react_prompt import \
    SEARCH_ENGINE_REACT_PROMPT
from assistants.react_agent.schemas import SearchAgentResponse
from assistants.utils import get_ollama_provider

init_env()

console = Console()

tools = [TavilySearch()]
llm = get_ollama_provider()

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
    template=SEARCH_ENGINE_REACT_PROMPT,
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


def main():

    user_input = console.input("[b magenta]User🙋🏽‍♂️:")

    assistant_response = agent_executor.invoke(
        input={
            "input": user_input,
        }
    )

    formatted_response: SearchAgentResponse = output_parser.parse(
        assistant_response["output"]
    )

    console.print(
        f"[b cyan]Search Assistant🔎:[/b cyan]{formatted_response.agent_response}"
    )
    console.print(f"[b yellow][dim]Sources:{formatted_response.sources}")


if __name__ == "__main__":
    main()
