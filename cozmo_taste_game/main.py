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
from cozmo_taste_game.food.FoodManager import FoodManager
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

def load_items(file_name: str) -> List[FoodItem]:
    items = []
    with open(file_name) as item_file:
        for line in item_file:
            line = line.strip()

            # skip commented out lines
            if line.startswith('#'):
                continue
            else:
                (tag, name, group, taste) = line.lower().split(',')
                items.append(FoodItem(tag.strip(), FoodGroup[group.strip()], name.strip(), taste.strip()))

    return items


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
        try:
            conn = cozmo.connect_on_loop(loop)
            asyncio.ensure_future(bot.run(conn))
        except Exception as e:
            logger.error(traceback.format_exc())

        return bot


def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-b", "--fakeRobot", action="store_true", dest="fake_robot",
                      help="Don't connect to the real cozmo")
    parser.add_option("-i", "--fakeReader", action="store_true", dest="fake_reader",
                      help="Don't connect to the real RFID reader")
    parser.add_option("-k", "--knownItemFile", dest="known_items_file", metavar="FILE",
                      help="the file where known items are stored",
                      default='items.csv')
    parser.add_option("-n", "--disableUI", action="store_true", dest="disable_ui",
                      help="disable the graphical interface")

    (options, _ignored_) = parser.parse_args()
    loop = asyncio.get_event_loop()

    item_list = load_items(options.known_items_file)

    if options.disable_ui:
        reader = create_reader(options.fake_reader, loop, item_list)
        create_robot(options.fake_robot, loop)
        loop.run_forever()
    else:

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
        game = CozmoTasteGameInterface(engine)
        loop.run_until_complete(game.MainLoop())


main()
