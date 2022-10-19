from .abstract import AbstractEngine


class FileEngine(AbstractEngine):
    def __init__(self, filename: str):
        self.file = open(filename, "rb")

    def read(self, number_of_bytes: int) -> bytes:
        return self.file.read(number_of_bytes)

