import os
from pathlib import Path
from typing import Any, List, Optional, Union

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents.base import Document
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import (
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

from assistants import __root_dir__
from assistants.data_ingestor import Ingestor, IngestionPipeline
from assistants.logger import get_logger
from assistants import init_env

init_env()

logger = get_logger()

POLICIES_DOCUMENT_PATH = os.path.join(
    __root_dir__,
    "hr_assistant",
    "resources",
    "policies.md",
)
PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
)


class HRPoliciesIngestor(Ingestor):

    def __init__(
        self,
        policies_document_path: Optional[
            Union[str, Path]
        ] = POLICIES_DOCUMENT_PATH,
        index_name: Optional[str] = PINECONE_INDEX_NAME,
    ):
        self.policies_document_path = policies_document_path

        self.index_name = index_name
        if not self.index_name:
            logger.error(
                "Please set `PINECONE_INDEX_NAME` to the name of the pinecone vector store in the `.env` file"
            )
            raise ValueError

    def load_document(self) -> Document:

        document_loader: UnstructuredMarkdownLoader = self._get_loader()
        document: Document = document_loader.load()[0]

        logger.debug(
            f"[b d]Successfully loaded the policies document from: {document.metadata["source"]}\n"
            f"[b d]Document Preview: {document.page_content[:256]} ..."
        )

        return document

    @staticmethod
    def split_document_into_chunks(document: Document) -> List[Document]:

        logger.info("Splitting markdown policies document by headers")

        header_splitter: MarkdownHeaderTextSplitter = (
            HRPoliciesIngestor._get_header_splitter()
        )
        document_split_by_headers: List[Document] = header_splitter.split_text(
            document.page_content
        )

        logger.info("Splitting header sections into smaller chunks")

        text_splitter = HRPoliciesIngestor._get_text_splitter()
        chunked_document: List[Document] = text_splitter.split_documents(
            documents=document_split_by_headers,
        )

        logger.debug(f"Final chunks count: {len(chunked_document)}")

        return chunked_document

    @staticmethod
    def get_document_embeddings(
        chunked_document: List[Document],
    ) -> Optional[Any]:

        logger.info(
            "Pinecone handles auto-generation of embeddings, given the raw document.\n"
            "Skipping manual embedding generation ..."
        )

        return None

    def store_embeddings(
        self, chunked_document: List[Document], embedding: Optional[Any] = None
    ) -> int:

        logger.info(
            f"Storing embeddings in the vector index: {self.index_name}"
        )

        PineconeVectorStore.from_documents(
            documents=chunked_document,
            embedding=embedding,
            index_name=self.index_name,
        )

        return 200

    def _get_loader(self) -> UnstructuredMarkdownLoader:

        return UnstructuredMarkdownLoader(
            file_path=self.policies_document_path,
            mode="elements",
        )

    @staticmethod
    def _get_header_splitter() -> MarkdownHeaderTextSplitter:

        return MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("##", "Section"),
                ("###", "Policy"),
            ],
            strip_headers=False,
        )

    @staticmethod
    def _get_text_splitter() -> CharacterTextSplitter:

        return CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

class HRPoliciesIngestionPipeline(IngestionPipeline):
    def __init__(self, ingestor: HRPoliciesIngestor):
        self.policies_ingestor = ingestor

    def run(self):

        logger.info(
            "Running policies ingestion pipeline ..."
        )

        document = self.policies_ingestor.load_document()
        chunked_document = self.policies_ingestor.split_document_into_chunks(document=document)
        embedding = self.policies_ingestor.get_document_embeddings(chunked_document=chunked_document)

        logger.info(
            "Storing chunked documents and their embeddings into the vector store ..."
        )

        status_code: int = self.policies_ingestor.store_embeddings(
            chunked_document=chunked_document,
            embedding=embedding,
        )

        if status_code == 200:
            logger.info(
                f"Policies ingested successfully into the vector index: {self.policies_ingestor.index_name}"
            )
        

if __name__=="__main__":

    dummy_ingestor = HRPoliciesIngestor()
    dummy_ingestion_pipeline = HRPoliciesIngestionPipeline(
        ingestor=dummy_ingestor,
    )

    dummy_ingestion_pipeline.run()