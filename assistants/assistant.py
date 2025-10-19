from abc import ABC, abstractmethod
from typing import Any


class Assistant(ABC):

    @abstractmethod
    def query(self, user_input: str) -> Any:
        raise NotImplementedError
