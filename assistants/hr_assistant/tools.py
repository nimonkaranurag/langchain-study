import os
from typing import Optional, Tuple

from langchain.agents import tool
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from pinecone import Pinecone

from assistants.hr_assistant.schemas import (
    Date,
    TimeOffRequest,
    TimeOffResponse,
)


@tool(response_format="content_and_artifact")
def request_time_off(request: TimeOffRequest) -> Tuple[str, TimeOffResponse]:
    """
    Apply for time-off in the provided date range.
    Args:
        employee_email (str): The employee's work email.
        start_date (Date): The starting date for requesting time-off.
        end_date (Date): The ending date for requesting time-off.
    """

    employee_email: str = request.employee_email
    if employee_email != "nimo@ibm.com":
        raise ValueError(
            f"No employee with email: {employee_email} exists, please provide a valid employee email."
        )

    start_date: Date = request.start_date
    end_date: Date = request.end_date

    response_message = (
        f"The time off request for the employee with email: {employee_email} "
        f"has been successfully made for the dates:\n"
        f"{str(start_date)} to {str(end_date)}.\n"
        "Please approach your in-office manager for approval."
    )

    response = TimeOffResponse(
        status=200,
    )

    return (
        response_message,
        response,
    )


@tool
def get_relevant_company_policies(query: str, top_k: int = 5) -> str:
    """
    A search tool that can retrieve company policies relevant to a query.
    The query is matched against a vector database that contains company policies.

    Args:
        query (str): A re-phrasing of the user's query so that it can match with the relevant HR policy.
        top_k (int): The number of matched results to return.
    Returns:
        A formatted string with the top policies matched for similarity against the "query" input.
    """

    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    POLICIES_NAMESPACE = "hr_policies"

    pinecone_client = Pinecone()
    policies_index = pinecone_client.Index(name=PINECONE_INDEX_NAME)

    embeddings_model = PineconeEmbeddings(model="llama-text-embed-v2")

    query_embedding = embeddings_model.embed_query(query)

    raw_results = policies_index.query(
        vector=query_embedding,
        top_k=top_k,
        namespace=POLICIES_NAMESPACE,
        include_metadata=True,
    )
    if not raw_results or not raw_results["matches"]:
        return f"No results found for the query: {query}"

    policies: str = "Here are the relevant policies:\n\n"
    for match in raw_results["matches"]:

        metadata = match.get("metadata", {})

        policies += f"{metadata.get("text", "N/A")}\n"
        policies += f"Section: {metadata.get("Section", "N/A")}\n"
        policies += f"Policy: {metadata.get("Policy", "N/A")}\n\n"

    return policies
