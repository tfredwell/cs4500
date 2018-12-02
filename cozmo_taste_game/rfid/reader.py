from abc import ABC, abstractmethod
from typing import Callable


class Reader(ABC):

    @abstractmethod
    def on_tag_read(self, callback: Callable[[str], None]) -> None:
        pass
