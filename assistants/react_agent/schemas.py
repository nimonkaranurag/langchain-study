from typing import List

from pydantic import BaseModel, Field


class SourceURL(BaseModel):
    """
    Represents a schema used for formatting URLs.
    """

    url: str = Field(
        description="a resource used by the agent to generate its final response."
    )


class SearchAgentResponse(BaseModel):
    """
    Represents a schema used for formatting the final answer of the agent.
    """

    agent_response: str = Field(description="the answer provided by the agent.")
    sources: List[SourceURL] = Field(
        default_factory=list,
        description="a list of URLs used by the agent its final response.",
    )
