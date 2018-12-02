from typing import Callable
from threading import Timer
from .reader import Reader


class FakeReader(Reader):
    def __init__(self, tags):
        self.tags = tags
        self.tag_index = 0
        self.tag_read_callback = None

    def on_tag_read(self, callback: Callable[[str], None]) -> None:
        self.tag_read_callback = callback
        Timer(.3, self.__take_tag).start()

    def __take_tag(self):
        print('taking tag')
        if self.tag_index >= len(self.tags):
            self.tag_index = 0
        tag = self.tags[self.tag_index]
        self.tag_read_callback(tag)
        self.tag_index += 1
        Timer(.3, self.__take_tag).start()
