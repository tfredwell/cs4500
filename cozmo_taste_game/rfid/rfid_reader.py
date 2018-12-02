from typing import Callable
from threading import Thread
from cozmo_taste_game.rfid import Reader


class RfidReader(Reader):
    def __init__(self, loop):
        self.tag_read_callback = None
        t = Thread(target=self.__take_tag)
        t.daemon = True
        t.start()

    def on_tag_read(self, callback: Callable[[str], None]) -> None:
        self.tag_read_callback = callback

    def __take_tag(self):
        while True:
            tag = input()
            if self.tag_read_callback is not None:
                self.tag_read_callback(tag)
