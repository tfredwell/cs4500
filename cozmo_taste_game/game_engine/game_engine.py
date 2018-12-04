import asyncio
from random import choice

import cozmo

from cozmo_taste_game import FoodGroup
from cozmo_taste_game.game_engine.event_dispatcher import EventDispatcher
from cozmo_taste_game.robot import EvtNewGameStarted, EvtUnknownTag, FoodItem, EvtCorrectFood, EvtWrongFood


class GameEngine(EventDispatcher):
    def __init__(self, item_list, loop):
        super().__init__()
        self.item_list = dict((item.tag, item) for item in item_list)
        self.loop = loop
        self.game_running = False
        self.food_group = None
        self.robot_connected = False


    async def start_new_game(self):
        # noinspection PyTypeChecker
        self.food_group = self.get_next_food_group()
        self.game_running = True
        await self.notify(EvtNewGameStarted, food_group=self.food_group)


    def get_next_food_group(self):
        """Take the next food item, in a loop so we dont pick the same one multiple times"""
        next = None
        while next is None:
            next = choice(list(FoodGroup))
            if next == self.food_group:
                next = None

        return next
    async def tag_read(self, tag):
        if tag in self.item_list:
            item: FoodItem = self.item_list[tag]
            if item.food_group == self.food_group:
                await self.notify(EvtCorrectFood, food_item=item)
            else:
                await self.notify(EvtWrongFood, food_item=item, expected_food_group=self.food_group)
        else:
            await self.notify(EvtUnknownTag, tag=tag)

    def add_food_item(self, item: FoodItem):
        if item.tag not in self.item_list:
            self.item_list[item.tag] = item
            asyncio.create_task(self.write_item_to_file(item))


    async def toggle_robot_connect(self):
        if self.robot_connected:
            pass
        else:
            pass


    async def write_item_to_file(self, item):
        from os import path
        resource_path =  path.abspath(path.join(path.dirname(path.dirname(__file__)), "items.csv"))
        with open(resource_path, 'a+') as file:  # Use file to refer to the file object
            # tag, name, group taste
            line = f'\n{item.tag},{item.name},{item.food_group.name},{item.taste}'
            file.write(line)
        await asyncio.sleep(.1)
