import os

from langchain.agents import tool
from langchain_pinecone import PineconeEmbeddings
from pinecone import Pinecone

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
README_NAMESPACE = "repo-readme"
LANGCHAIN_DOCS_NAMESPACE = "study-assistant"


def _query_pinecone(query: str, top_k: int, namespace: str):

    pinecone_index = Pinecone().Index(PINECONE_INDEX_NAME)

    encoded_query = PineconeEmbeddings(
        model="llama-text-embed-v2",
    ).embed_query(query)

    results = pinecone_index.query(
        vector=encoded_query,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True,
    )

    return results


def _format_response(intro_string: str, user_query: str, results) -> str:

    if not results or not results["matches"]:
        return f"No results found for the query: {user_query}"

    response = ""
    response += intro_string
    for result in results["matches"]:

        metadata = result.get("metadata", {})

        response += f"Title: {metadata.get("TITLE", "N/A")}\n"
        response += f"Section: {metadata.get("SECTION", "N/A")}\n"
        response += f"Subsection: {metadata.get("SUBSECTION", "N/A")}\n"
        response += f"{metadata.get("text", "N/A")}\n\n"

    return response


@tool
def get_repo_readme(user_query: str, num_of_results_to_fetch: int = 5) -> str:
    """
    Get the README of the repo concatenated as a single string.
    This tool is to be used for user queries relating to how they can use the "langchain-study" repository.
    For example, if the user asks: "how do I run the hr_assistant?" then the README likely contains instructions on how this can be achieved.
    The query passed is used for fetching only the relevant section of the README.

    Args:
        user_query (str): a paraphrasing of the user's question that is matched against the README for relevant sections.
        num_of_results_to_fetch (int): the number of relevant results to return that match in the README against the user's query.
    """

    results = _query_pinecone(
        query=user_query,
        top_k=num_of_results_to_fetch,
        namespace=README_NAMESPACE,
    )
    return _format_response(
        intro_string="Here are the relevant sections from the README:\n\n",
        user_query=user_query,
        results=results,
    )


@tool
def get_langchain_documentation(
    user_query: str, num_of_results_to_fetch: int = 5
) -> str:
    """
    Get the relevant sections from langchain's documentation, matched against the user's query.
    This tool returns a formatted string containing all sections relevant to the user's query in the langchain documentation.

    Args:
        user_query (str): a paraphrasing of the user's question, matched against langchain documentation for relevance.
        num_of_results_to_fetch (int): the number of relevant matches to return.
    """

    results = _query_pinecone(
        query=user_query,
        top_k=num_of_results_to_fetch,
        namespace=LANGCHAIN_DOCS_NAMESPACE,
    )
    return _format_response(
        intro_string="Here are the relevant sections from the Langchain documentation:\n\n",
        user_query=user_query,
        results=results,
    )
