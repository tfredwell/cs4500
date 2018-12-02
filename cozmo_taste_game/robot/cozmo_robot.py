from asyncio import sleep
from random import choice

import cozmo
from cozmo.robot import Robot

from cozmo_taste_game.food.food_group import FoodGroup
from cozmo_taste_game.robot import EvtWrongFood, EvtTagRead, EvtStartNewGame, EvtCorrectFood,EvtTagFound, EvtUnknownTag


class RealTasterBot:
    def __init__(self, items):
        self.cozmo = None
        self.world = None
        self.items = dict((item.tag, item) for item in items)
        self.ready = False

    async def run(self, connection):
        try:
            self.cozmo = await connection.wait_for_robot()
            self.world = self.cozmo.world
            action = self.cozmo.say_text('hello')
            await action.wait_for_completed()
            await self.start()

            while True:
                await sleep(0.1)
        except KeyboardInterrupt:
            print("Exited.")

    async def send_tag(self, tag):
        await self.world.dispatch_event(EvtTagRead, tag=tag)

    async def async_send_tag(self, tag):
        await self.world.dispatch_event(EvtTagRead, tag=tag)

    async def start(self):
        self.world.add_event_handler(EvtTagRead, self.__tag_read)
        self.world.add_event_handler(EvtStartNewGame, self.__start_new_game)
        self.world.add_event_handler(EvtUnknownTag, self.__unknown_tag)
        self.world.add_event_handler(EvtTagFound, self.__tag_found)
        self.world.add_event_handler(EvtWrongFood, self.__wrong_food)
        self.world.add_event_handler(EvtCorrectFood, self.__correct_food)
        next_food_group = choice(list(FoodGroup))
        await self.world.dispatch_event(EvtStartNewGame, food_group=next_food_group)

    async def __start_new_game(self, evt: EvtStartNewGame, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        self.food_group = evt.food_group
        action = self.cozmo.say_text(f'I am hungry for some {self.food_group.name}')
        await action.wait_for_completed()
        self.ready = True

    async def __unknown_tag(self, evt: EvtUnknownTag, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        action = self.cozmo.say_text('Hmm, I do not know what that is!')
        await action.wait_for_completed()
        self.ready = True

    async def __tag_found(self, evt: EvtTagFound, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        if self.food_group == evt.food_item.food_group:
            await self.world.dispatch_event(EvtCorrectFood, food_item=evt.food_item)
        else:
            await self.world.dispatch_event(EvtWrongFood, food_item=evt.food_item, expected_food_group=self.food_group)

    async def __wrong_food(self, evt: EvtWrongFood, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        say = self.cozmo.say_text(f'A {evt.food_item.name} is not a {evt.expected_food_group.name}')
        await say.wait_for_completed()
        self.ready = True

    async def __correct_food(self, evt: EvtCorrectFood, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        next_food_group = choice(list(FoodGroup))
        msg = f'Yum! The {evt.food_item.food_group.name} {evt.food_item.name} is {evt.food_item.taste}'
        action = self.cozmo.say_text(msg, play_excited_animation=True)
        await action.wait_for_completed()
        await self.world.dispatch_event(EvtStartNewGame, food_group=next_food_group)

    async def __tag_read(self, evt: EvtTagRead, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        if self.ready:
            self.ready = False
            if evt.tag in self.items:
                await self.world.dispatch_event(EvtTagFound, food_item=self.items[evt.tag])
            else:
                await self.world.dispatch_event(EvtUnknownTag, tag=evt.tag)
        else:
            cozmo.logger.info(f'ignoring event {evt}')
