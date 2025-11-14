import os
from pathlib import Path
from typing import Any, List, Optional, Union

from langchain_core.documents import Document
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

LANGCHAIN_NOTES_PATH = Path(
    os.path.join(
        __root_dir__,
        "study_assistant",
        "resources",
    )
)
PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
)
PINECONE_INDEX_NOTES_NAMESPACE = "study-assistant"


class LangChainNotesIngestor(Ingestor):

    def __init__(
        self,
        langchain_notes_path: Optional[Union[str, Path]] = LANGCHAIN_NOTES_PATH,
        index_name: Optional[str] = PINECONE_INDEX_NAME,
        notes_namespace: Optional[str] = PINECONE_INDEX_NOTES_NAMESPACE,
    ):
        if not isinstance(langchain_notes_path, Path):
            langchain_notes_path = Path(langchain_notes_path)

        self.langchain_notes_path = langchain_notes_path

        self.index_name = index_name
        if not self.index_name:
            raise ValueError(
                "Please set `PINECONE_INDEX_NAME` to the name of the pinecone vector store in the `.env` file"
            )
        self.notes_namespace = notes_namespace

    def load_document(self):

        notes_extensions = [
            "*.md",
            "*.txt",
        ]

        for note_extension in notes_extensions:
            for notes_path in self.langchain_notes_path.rglob(note_extension):
                with open(notes_path, "r") as f:
                    yield f.read()

    @staticmethod
    def split_document_into_chunks(document: Any) -> List[Document]:

        document_split_by_headers = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "TITLE"),
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

        return chunked_document

    @staticmethod
    def get_embedding_model() -> PineconeEmbeddings:
        return PineconeEmbeddings(model="llama-text-embed-v2")

    def store_embeddings(
        self,
        chunked_document: List[Document],
        embedding_model: PineconeEmbeddings,
    ) -> int:

        try:
            PineconeVectorStore.from_documents(
                index_name=self.index_name,
                embedding=embedding_model,
                namespace=self.notes_namespace,
                documents=chunked_document,
            )
        except Exception as e:
            logger.error(
                f"Could not ingest embeddings into vectorstore: {e}",
                exc_info=True,
                stack_info=True,
            )
            return 500

        return 200


class LangChainNotesIngestionPipeline(IngestionPipeline):

    def __init__(self, ingestor: LangChainNotesIngestor):
        super().__init__(ingestor)

    def run(self):

        logger.info("[b d]Beginning ingestion pipeline")

        documents = self.ingestor.load_document()
        embedding_model = LangChainNotesIngestor.get_embedding_model()

        for count, document in enumerate(documents):

            chunked_document = self.ingestor.split_document_into_chunks(
                document=document,
            )

            status_code = self.ingestor.store_embeddings(
                chunked_document=chunked_document,
                embedding_model=embedding_model,
            )

            if status_code != 200:
                logger.error(
                    f"[b d]Failed to store embeddings for a document, it is being skipped"
                )
                continue

            logger.info(f"[b d]Ingested {count} documents")

        logger.info(f"[b d]Ingestion pipeline run is completed")


if __name__ == "__main__":

    dummy_ingestor = LangChainNotesIngestor()
    dummy_ingestion_pipeline = LangChainNotesIngestionPipeline(
        ingestor=dummy_ingestor,
    )

    dummy_ingestion_pipeline.run()
