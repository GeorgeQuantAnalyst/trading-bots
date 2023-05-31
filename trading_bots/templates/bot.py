from abc import ABC, abstractmethod


class Bot(ABC):

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def run(self) -> None:
        pass
