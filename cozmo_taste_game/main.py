#!/usr/bin/env python3

from optparse import OptionParser
from typing import List

from cozmo_taste_game import *
from cozmo_taste_game.food.food_group import FoodGroup
from cozmo_taste_game.game_engine import CozmoGame


def create_robot(use_fake: bool) -> Robot:
    if use_fake:
        return FakeRobot()
    return CozmoRobot()


def create_reader(use_fake: bool, tags: List[str]) -> Reader:
    if use_fake:
        return FakeReader(tags)
    return RfidReader()


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


def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-b", "--fakeRobot", action="store_true", dest="useFakeRobot",
                      help="Don't connect to the real cozmo")
    parser.add_option("-i", "--fakeReader", action="store_true", dest="useFakeReader",
                      help="Don't connect to the real RFID reader")
    parser.add_option("-k", "--knownItemFile", dest="knownItemsFile", metavar="FILE",
                      help="the file where known items are stored",
                      default='items.csv')

    (options, _ignored_) = parser.parse_args()

    items = load_items(options.knownItemsFile)
    reader = create_reader(options.useFakeReader, list(map(lambda food_item: food_item.tag, items)))
    game_robot = create_robot(options.useFakeRobot)

    game = CozmoGame(game_robot, reader, items)
    game.play()


main()
input('press any key to exit....')