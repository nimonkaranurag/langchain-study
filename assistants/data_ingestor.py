from abc import ABC, abstractmethod
from typing import Any, List

from langchain_core.documents import Document


class Ingestor(ABC):

    @abstractmethod
    def load_document(self) -> Any:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def split_document_into_chunks(
        document: str, *args, **kwargs
    ) -> List[Document]:
        raise NotImplementedError

    @abstractmethod
    def store_embeddings(
        self,
        chunked_document: List[Document],
        embedding_model: Any,
    ) -> int:  # status code
        raise NotImplementedError


class IngestionPipeline(ABC):

    def __init__(self, ingestor: Ingestor):
        self.ingestor = ingestor

    @abstractmethod
    def run(self):
        raise NotImplementedError
