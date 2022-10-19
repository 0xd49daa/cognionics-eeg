from abc import ABC, abstractmethod


class AbstractEngine(ABC):
    @abstractmethod
    def read(self, number_of_bytes: int) -> bytes:
        pass
