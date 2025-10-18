from abc import ABC, abstractmethod

from assistants.assistant import Assistant


class AssistantBuilder(ABC):

    @abstractmethod
    def build(self) -> Assistant:
        pass
