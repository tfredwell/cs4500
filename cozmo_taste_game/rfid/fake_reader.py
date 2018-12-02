import asyncio
import inspect
from typing import Callable

from .reader import Reader


class FakeReader(Reader):
    def __init__(self, loop, tags):
        self.tags = tags
        self.tag_index = 0
        self.loop = loop

    def on_tag_read(self, callback: Callable[[str], None]) -> None:
        self.loop.call_soon(self.take_tag, callback)

    def take_tag(self, callback):
        if self.tag_index >= len(self.tags):
            self.tag_index = 0

        tag = self.tags[self.tag_index]
        self.tag_index+=1
        asyncio.run_coroutine_threadsafe(callback(tag), self.loop)
        self.loop.call_later(1, self.take_tag, callback)
