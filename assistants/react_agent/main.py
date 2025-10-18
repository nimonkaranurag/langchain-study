from rich.console import Console

from assistants import init_env
from assistants.logger import get_logger
from assistants.react_agent import get_search_agent_react_template
from assistants.react_agent.schemas import SearchAgentResponse
from assistants.react_agent.search_assistant import SearchAssistant
from assistants.react_agent.search_assistant_builder import SearchAssistantBuilder

logger = get_logger()

console = Console()


def main():

    logger.info("[b d]Initializing environment")
    init_env()

    logger.info("[b d]Building search assistant")
    search_assistant: SearchAssistant = SearchAssistantBuilder().build()

    user_input = console.input("[b magenta]User🙋🏽‍♂️:")

    formatted_assistant_response: SearchAgentResponse = search_assistant.query(
        user_input=user_input,
    )

    console.print(
        f"[b cyan]Search Assistant🔎:[/b cyan]{formatted_assistant_response.agent_response}"
    )
    console.print(f"[b yellow][dim]Sources:{formatted_assistant_response.sources}")


if __name__ == "__main__":
    main()
