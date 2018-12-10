import asyncio
import logging
from random import choice

from cozmo_taste_game import FoodGroup
from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.game_engine.event_dispatcher import EventDispatcher
from cozmo_taste_game.robot import EvtNewGameStarted, EvtUnknownTag, FoodItem, EvtCorrectFoodGroup, EvtWrongFoodGroup

logger = logging.getLogger('cozmo_taste_game.game_engine')


class GameEngine(EventDispatcher):
    def __init__(self, food_manager, loop):
        super().__init__()

        self.food_manager = food_manager
        self.loop = loop
        self.game_running = False
        self.food_group = None
        self.robot_connected = False

    async def start_new_game(self):
        # noinspection PyTypeChecker
        self.food_group = self.get_next_food_group()
        self.game_running = True
        await self.notify(EvtNewGameStarted, food_group=self.food_group)

    def get_next_food_group(self) -> FoodGroup:
        """Take the next food item, in a loop so we dont pick the same one multiple times"""
        next_food_group_name = None
        while next_food_group_name is None:
            next_food_group_name = choice(FoodManager.get_food_group_names())
            if next_food_group_name == self.food_group:
                next_food_group_name = None

        return FoodGroup[next_food_group_name]

    async def tag_read(self, tag):
        # if the food_group isn't set we arent in a running game
        if self.food_group is None:
            logger.info('Skipping tag scan, food group is None')
            return

        item = self.food_manager.get_by_tag(tag)
        if item is not None:
            if item.food_group == self.food_group:
                await self.notify(EvtCorrectFoodGroup, food_item=item)
            else:
                await self.notify(EvtWrongFoodGroup, food_item=item, expected_food_group=self.food_group)
        else:
            await self.notify(EvtUnknownTag, tag=tag)

    def add_food_item(self, item: FoodItem):
        asyncio.create_task(self.food_manager.add_item(item))

    async def toggle_robot_connect(self):
        if self.robot_connected:
            pass
        else:
            pass
