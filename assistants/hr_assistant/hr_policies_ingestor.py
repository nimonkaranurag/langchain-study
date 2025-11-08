import os
from pathlib import Path
from typing import Any, List, Optional, Union

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents.base import Document
from langchain_pinecone import PineconeEmbeddings, PineconeVectorStore
from langchain_text_splitters import (
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

from assistants import __root_dir__, init_env
from assistants.data_ingestor import IngestionPipeline, Ingestor
from assistants.logger import get_logger

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
PINECONE_INDEX_POLICIES_NAMESPACE = "hr_policies"


class HRPoliciesIngestor(Ingestor):

    def __init__(
        self,
        policies_document_path: Optional[
            Union[str, Path]
        ] = POLICIES_DOCUMENT_PATH,
        index_name: Optional[str] = PINECONE_INDEX_NAME,
        policies_namespace: Optional[str] = PINECONE_INDEX_POLICIES_NAMESPACE,
    ):
        self.policies_document_path = policies_document_path

        self.index_name = index_name
        if not self.index_name:
            raise ValueError(
                "Please set `PINECONE_INDEX_NAME` to the name of the pinecone vector store in the `.env` file"
            )
        self.policies_namespace = policies_namespace

    def load_document(self) -> str:

        with open(self.policies_document_path, "r", encoding="utf-8") as f:
            document = f.read()

        logger.debug(
            f"[b d]Successfully loaded policies from: {self.policies_document_path}"
        )
        logger.debug(f"[b d]Content length: {len(document)} characters")

        return document

    @staticmethod
    def split_document_into_chunks(document: str) -> List[Document]:

        header_splitter: MarkdownHeaderTextSplitter = (
            HRPoliciesIngestor._get_header_splitter()
        )
        document_split_by_headers: List[Document] = header_splitter.split_text(
            document
        )

        logger.info("[b d]Splitting header sections into smaller chunks")

        text_splitter = HRPoliciesIngestor._get_text_splitter()
        chunked_document: List[Document] = text_splitter.split_documents(
            documents=document_split_by_headers,
        )

        if chunked_document:
            logger.debug(f"[b d]Final chunks count: {len(chunked_document)}")
            for document_chunk in chunked_document:
                logger.debug(
                    f"[b i d]Chunk preview:{document_chunk.page_content}"
                )
        else:
            raise RuntimeError("Chunking unsuccessful")

        return chunked_document

    @staticmethod
    def get_embedding_model() -> Optional[Any]:

        logger.info("[b d]Using Pinecone's integrated embeddings model")

        return PineconeEmbeddings(model="llama-text-embed-v2")

    def store_embeddings(
        self,
        chunked_document: List[Document],
        embedding_model: PineconeEmbeddings,
    ) -> int:

        logger.info(
            f"[b d]Storing embeddings in the vector index: {self.index_name}"
        )

        PineconeVectorStore.from_documents(
            documents=chunked_document,
            embedding=embedding_model,
            index_name=self.index_name,
            namespace=self.policies_namespace,
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

        logger.info("[b d]Running policies ingestion pipeline ...")

        document = self.policies_ingestor.load_document()
        chunked_document = self.policies_ingestor.split_document_into_chunks(
            document=document
        )
        embedding_model = self.policies_ingestor.get_embedding_model()

        logger.info(
            "[b d]Storing chunked documents and their embeddings into the vector store ..."
        )

        status_code: int = self.policies_ingestor.store_embeddings(
            chunked_document=chunked_document,
            embedding_model=embedding_model,
        )

        if status_code == 200:
            logger.info(
                f"[b d]Policies ingested successfully into the vector index: {self.policies_ingestor.index_name}"
            )


if __name__ == "__main__":

    dummy_ingestor = HRPoliciesIngestor()
    dummy_ingestion_pipeline = HRPoliciesIngestionPipeline(
        ingestor=dummy_ingestor,
    )

    dummy_ingestion_pipeline.run()
