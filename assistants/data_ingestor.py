from abc import ABC, abstractmethod
from typing import Any, List, Optional


class Ingestor(ABC):

    @abstractmethod
    def load_document(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def split_document_into_chunks(document: Any):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_document_embeddings(chunked_document: List[Any]):
        raise NotImplementedError

    @abstractmethod
    def store_embeddings(
        self, chunked_document: List[Any], embedding: Optional[Any] = None
    ) -> int:
        raise NotImplementedError


class IngestionPipeline(ABC):

    def __init__(self, ingestor: Ingestor):
        self.ingestor = ingestor

    @abstractmethod
    def run(self):
        raise NotImplementedError
