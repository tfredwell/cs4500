#!/usr/bin/env python3
import asyncio
from asyncio import sleep, run
from optparse import OptionParser
from typing import List

import cozmo

from cozmo_taste_game import FoodItem, Reader, FakeReader, RfidReader, RealTasterBot
from cozmo_taste_game.food.food_group import FoodGroup
from cozmo_taste_game.robot import FakeCozmo


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

def create_robot(use_fake, loop, items, reader):
    bot = RealTasterBot(items)
    if use_fake:
        fake = FakeCozmo(loop)
        bot.cozmo = fake
        bot.world = fake.world
        reader.on_tag_read(bot.send_tag)
        asyncio.ensure_future(bot.start())
    else:
        class Factory(cozmo.robot.Robot):
            async def run(self, cozmo_connection: object) -> object:
                await bot.run(cozmo_connection)

        cozmo.conn.CozmoConnection.robot_factory = Factory
        cozmo.connect_on_loop(loop)

#


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

    loop = asyncio.get_event_loop()
    (options, _ignored_) = parser.parse_args()
    item_list = load_items(options.known_items_file)
    reader = create_reader(options.fake_reader, loop, item_list)
    robot = create_robot(options.fake_robot, loop, item_list, reader)
    loop.run_forever()
    # (options, _ignored_) = parser.parse_args()
    # item_list = load_items(options.known_items_file)
    # reader = create_reader(options.fake_reader, item_list)
    # await create_robot(options.fake_robot, item_list, reader)


main()
