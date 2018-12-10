#!/usr/bin/env python3
import asyncio
import sys
from asyncio import get_event_loop
from optparse import OptionParser
from typing import List

import cozmo
from wxasync import WxAsyncApp
import traceback

from cozmo_taste_game import FoodItem, Reader, FakeReader, RfidReader, RealTasterBot, UserInterface, GameEngine
from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.food.food_group import FoodGroup
from cozmo_taste_game.robot import FakeCozmo
from cozmo_taste_game.user_interface.app import CozmoTasteGameInterface
import logging

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
root.addHandler(handler)

logger = logging.getLogger('cozmo_taste_game.main')


def create_reader(use_fake: bool, loop, items: List[FoodItem]) -> Reader:
    if use_fake:
        return FakeReader(loop, list(map(lambda item: item.tag, items)))
    return RfidReader(loop)


def create_robot(use_fake, loop):
    bot = RealTasterBot()
    if use_fake:

        fake = FakeCozmo(loop)
        bot.cozmo = fake
        bot.world = fake.world
        # asyncio.ensure_future(bot.start())
    else:
        bot = RealTasterBot()
        # noinspection PyBroadException
        try:
            conn = cozmo.connect_on_loop(loop)
            asyncio.ensure_future(bot.run(conn))
        except Exception:
            logger.error(traceback.format_exc())

        return bot


def main():
    loop = asyncio.get_event_loop()
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    root.addHandler(handler)

    food_manager = FoodManager("items.csv")
    food_manager.load_items()

    engine = GameEngine(food_manager, loop)

    robot = create_robot(False, loop)
    robot.connect(engine)
    game = CozmoTasteGameInterface(engine, food_manager)
    loop.run_until_complete(game.MainLoop())


main()
