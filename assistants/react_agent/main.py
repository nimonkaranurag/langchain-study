from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_tavily import TavilySearch
from rich.console import Console

from assistants import init_env
from assistants.utils import get_ollama_provider

init_env()

console = Console()

tools = [TavilySearch()]
llm = get_ollama_provider()

PROMPT_OWNER_STRING = "hwchase17/react"
react_prompt: PromptTemplate = hub.pull(PROMPT_OWNER_STRING)

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

    while True:
        user_input = console.input("[b magenta]User🙋🏽‍♂️:")
        if "QUIT" in user_input:
            break

        assistant_response = agent_executor.invoke(
            input={
                "input": user_input,
            }
        )

        console.print(f"[b cyan]HR🤖:[/b cyan]{assistant_response}")


if __name__ == "__main__":
    main()
