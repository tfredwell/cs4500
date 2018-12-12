import asyncio
from random import choice

from cozmo_taste_game import FoodGroup, RealTasterBot
from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.game_engine.event_dispatcher import EventDispatcher
from cozmo_taste_game.game_engine.robot_connection import RobotConnection
from cozmo_taste_game.robot import EvtNewGameStarted, EvtUnknownTag, FoodItem, EvtCorrectFoodGroup, EvtWrongFoodGroup, \
    EvtNoRobotConnected, EvtRobotConnected, EvtRobotDisonnected


class GameEngine(EventDispatcher):
    def __init__(self, food_manager, robot: RealTasterBot):
        super().__init__()
        self.food_manager = food_manager
        self.robot_connection = RobotConnection()
        self.food_group = None
        self.robot = robot

    async def start_new_game(self):
        is_connected = await self.robot_connection.is_connected()
        if is_connected:
            self.food_group = self.get_next_food_group()
            await self.notify(EvtNewGameStarted, food_group=self.food_group)
        else:
            await self.notify(EvtNoRobotConnected)


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
            return

        item = self.food_manager.get_by_tag(tag)
        if item is not None:
            if item.food_group == self.food_group:
                await self.notify(EvtCorrectFoodGroup, food_item=item)
            else:
                await self.notify(EvtWrongFoodGroup, food_item=item, expected_food_group=self.food_group)
        else:
            await self.notify(EvtUnknownTag, tag=tag)

    async def add_food_item(self, item: FoodItem):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.food_manager.add_item(item))
        await task

    async def toggle_robot_connect(self):
        is_connected = await self.robot_connection.is_connected()
        if is_connected:
            await self.robot_connection.disconnect()
            self.robot.disconnect(self)
            await self.notify(EvtRobotDisonnected)
        else:
            cozmo = await self.robot_connection.connect()
            self.robot.connect(self, cozmo)
            await self.notify(EvtRobotConnected)





        # connector = FirstAvailableConnector()
        #
        # loop = asyncio.get_event_loop()
        # factory = functools.partial(conn_factory, loop=loop)
        #
        # async def conn_check(coz_conn):
        #     await coz_conn.wait_for(conn.EvtConnected, timeout=5)
        #
        # async def connect():
        #     return await connector.connect(loop, factory, conn_check)
        #
        # # noinspection PyBroadException
        # try:
        #     bot = RealTasterBot()
        #     bot.connect(self)
        #
        #     self.connected_robot = asyncio.ensure_future(bot.run(None))
        #
        # except cozmo.NoDevicesFound as e:
        #     self.connected_robot = None
        #     print(type(e))
        #     # logger.error(traceback.format_exc())
        #
