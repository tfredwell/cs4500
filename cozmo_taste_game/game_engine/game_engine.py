from random import choice

from cozmo_taste_game import FoodGroup
from cozmo_taste_game.game_engine.event_dispatcher import EventDispatcher
from cozmo_taste_game.robot import EvtNewGameStarted, EvtUnknownTag, FoodItem, EvtCorrectFood, EvtWrongFood


class GameEngine(EventDispatcher):
    def __init__(self, item_list):
        super().__init__()
        self.item_list = dict((item.tag, item) for item in item_list)

        self.game_running = False
        self.food_group = None

    async def start_new_game(self):
        # noinspection PyTypeChecker
        self.food_group = choice(list(FoodGroup))
        self.game_running = True
        await self.notify(EvtNewGameStarted, food_group=self.food_group)

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
