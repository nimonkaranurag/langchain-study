from abc import ABC, abstractmethod
from typing import Any


class Assistant(ABC):

    @abstractmethod
    def query(sel, user_input: str) -> Any:
        pass
