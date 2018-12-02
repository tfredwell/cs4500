from abc import ABC, abstractmethod


class TasterBot(ABC):
    """Abstract robot interface."""
    @abstractmethod
    def speak(self, text) -> None:
        pass
