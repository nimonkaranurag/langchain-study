from datetime import datetime

from rich.console import Console

from assistants import init_env
from assistants.logger import get_logger
from assistants.study_assistant.study_assistant_builder import (
    StudyAssistantBuilder,
)
from assistants.study_assistant.study_material_ingestor import (
    LangChainNotesIngestionPipeline,
    LangChainNotesIngestor,
)
from assistants.study_assistant.tools import (
    get_langchain_documentation,
    get_repo_readme,
    search_the_internet,
)

init_env()

logger = get_logger()

console = Console()

STUDY_ASSISTANT_TEMPLATE = """You are a helpful study assistant.
Your task is to help the user navigate the "langchain-study" repo and to provide information directly from the langchain documentation when asked a question about these topics.
"""


def main():

    logger.info("[b d]Ingesting repo's README")

    readme_ingestor = LangChainNotesIngestor(
        langchain_notes_path="./README.md",
        notes_namespace=f"repo-readme-{datetime.today().date().isoformat()}",
    )
    readme_ingestion_pipeline = LangChainNotesIngestionPipeline(
        ingestor=readme_ingestor,
    )

    try:
        readme_ingestion_pipeline.run()

        logger.info("[b d]Ingestion Successful")
    except Exception as e:

        logger.error(
            f"[b d]Failed to ingest repo README: {e}",
            exc_info=True,
            stack_info=True,
        )
        logger.info(
            f"[b d]README could not be ingested, the study-assistant is initialized with only langchain documentation by default."
        )
        pass

    logger.info("[b d]Building assistant")

    study_assistant_builder = StudyAssistantBuilder(
        raw_system_instructions=STUDY_ASSISTANT_TEMPLATE,
        tools=[
            get_langchain_documentation,
            get_repo_readme,
            search_the_internet,
        ],
    )

    try:
        study_assistant = study_assistant_builder.build()
    except Exception as e:
        raise RuntimeError(f"Failed to build assistant: {e}")

    logger.info("[b d]Assistant built successfully!")

    logger.info("[b d]Beginning user-assistant interaction")

    console.print(
        "[b green] Type [b yellow]'QUIT'[/b yellow] to terminate interaction."
    )
    while True:
        user_input = console.input("[b magenta]User🙋🏽‍♂️:")
        if "QUIT" in user_input:
            break

        formatted_assistant_response = study_assistant.query(
            user_input=user_input,
        )

        console.print(
            f"[b cyan]Study Assistant🤖:[/b cyan]{formatted_assistant_response.agent_response}"
        )
        console.print(
            f"[b yellow][dim]Sources:{formatted_assistant_response.sources}"
        )


if __name__ == "__main__":
    main()
