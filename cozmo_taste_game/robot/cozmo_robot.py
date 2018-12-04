import asyncio
from asyncio import sleep
from typing import List

import cozmo

from cozmo_taste_game.robot import EvtWrongFood, EvtCorrectFood, EvtUnknownTag, EvtNewGameStarted
import logging

logger = logging.getLogger('cozmo_taste_game.robot')



class RealTasterBot:

    def __init__(self):

        self.cozmo = None
        self.world = None

    async def run(self, connection):
        try:
            self.cozmo = await connection.wait_for_robot()
            self.world = self.cozmo.world
            while True:
                await sleep(0.1)
        except KeyboardInterrupt:
            print("Exited.")

    async def __start_new_game(self, evt: EvtNewGameStarted, **kw) -> None:
        logger.info(f'recv event {evt}')
        await self.__safe_say_text(f'I am hungry for some {evt.food_group.name}')

    async def __unknown_tag(self, evt: EvtUnknownTag, **kw) -> None:
        logger.info(f'recv event {evt}')
        await self.__safe_say_text('Hmm, I do not know what that is!')

    async def __wrong_food(self, evt: EvtWrongFood, **kw) -> None:
        logger.info(f'recv event {evt}')
        await self.__safe_say_text(f'A {evt.food_item.name} is not a {evt.expected_food_group.name}')

    async def __correct_food(self, evt: EvtCorrectFood, **kw) -> None:
        logger.info(f'recv event {evt}')
        msg = f'Yum! The {evt.food_item.food_group.name} {evt.food_item.name} is {evt.food_item.taste}'
        await self.__safe_say_text(msg, in_parallel=True)

    async def __safe_say_text(self, text, animations: List[object] = None, **kwargs):
        if self.cozmo:
            action = self.cozmo.say_text(text, kwargs)
            await action.wait_for_completed()
        else:
            logger.info(f'cozmo is not connected, not saying {text}')
            await asyncio.sleep(.1)

    def connect(self, engine):
        engine.add_event_hander(EvtNewGameStarted, self.__start_new_game)
        engine.add_event_hander(EvtUnknownTag, self.__unknown_tag)
        engine.add_event_hander(EvtWrongFood, self.__wrong_food)
        engine.add_event_hander(EvtCorrectFood, self.__correct_food)
