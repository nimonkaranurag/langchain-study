import os

import rich
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from langchain_text_splitters import (
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

from assistants import init_env


def main():

    init_env()

    with open("./README.md", mode="r") as f:
        document = f.read()

    document_split_by_headers = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("##", "SECTION"),
            ("###", "SUBSECTION"),
        ],
        strip_headers=False,
    ).split_text(document)

    chunked_document = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
    ).split_documents(document_split_by_headers)

    PineconeVectorStore.from_documents(
        documents=chunked_document,
        embedding=PineconeEmbeddings(model="llama-text-embed-v2"),
        namespace="study-assistant",
        index_name=os.getenv("PINECONE_INDEX_NAME"),
    )

    rich.print("[b green]Ingestion Successful")


if __name__ == "__main__":
    main()
