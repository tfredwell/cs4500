import asyncio
from cozmo.event import Dispatcher


class FakeWorld(Dispatcher):
    def __init__(self, loop, *a, **kw):
        super().__init__(*a, loop=loop, **kw)


class FakeWaitable:
    async def wait_for_completed(self):
        await asyncio.sleep(.1)


class FakeCozmo(Dispatcher):
    def __init__(self, loop, *a, **kw):
        super().__init__(*a, loop=loop, **kw)
        self.world = FakeWorld(loop)

    def say_text(self, text, play_excited_animation=False):
        if play_excited_animation:
            print(f'!!! {text} !!!')
        else:
            print(f'{text}')
        return FakeWaitable()
