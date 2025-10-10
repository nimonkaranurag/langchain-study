from abc import ABC, abstractmethod


class Assistant(ABC):

    @abstractmethod
    def query(self):
        pass
