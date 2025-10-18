from langchain_core.runnables import RunnableSequence

from assistants.assistant import Assistant
from assistants.logger import get_logger
from assistants.search_assistant.schemas import SearchAgentResponse

logger = get_logger()


class SearchAssistant(Assistant):

    def __init__(self, assistant_query_pipeline: RunnableSequence):

        self.assistant_query_pipeline = assistant_query_pipeline

    def query(self, user_input: str) -> SearchAgentResponse:

        logger.info(
            f"[b d]Triggering assistant query pipeline with the user input: {user_input}"
        )

        return self.assistant_query_pipeline.invoke(
            input={
                "input": user_input,
            },
        )
