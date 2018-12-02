from typing import Callable

from cozmo_taste_game.rfid import Reader


class RfidReader(Reader):
    def __init__(self):
        pass

    def on_tag_read(self, callback: Callable[[str], None]) -> None:
        pass
