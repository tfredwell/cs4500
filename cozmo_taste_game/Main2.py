#!/usr/bin/env python3

from optparse import OptionParser
from time import sleep
from typing import List

from cozmo.anim import Triggers

from cozmo_taste_game import *
from cozmo_taste_game.food.food_group import FoodGroup
from cozmo_taste_game.game_engine import CozmoGame

import sys
import asyncio
from time import sleep
from random import choice
import cozmo


class EvtTagRead(cozmo.event.Event):
    """The event sent when a tag has been read"""
    tag: str = ''


class EvtStartNewGame(cozmo.event.Event):
    """The event sent when a new game is started"""
    food_group: FoodGroup = None


class EvtUnknownTag(cozmo.event.Event):
    """The event sent when a new game is started"""
    tag: str = ''


class EvtTagFound(cozmo.event.Event):
    """The event sent when a new game is started"""
    food_item: FoodItem = None


class EvtWrongFood(cozmo.event.Event):
    """The event sent when a new game is started"""
    expected_food_group: FoodGroup = None
    food_item: FoodItem = None


class EvtCorrectFood(cozmo.event.Event):
    """The event sent when a new game is started"""
    food_item: FoodItem = None


class TasterBot(cozmo.robot.Robot):

    async def start(self, items):
        self.ready = False
        self.items = items
        self.world.add_event_handler(EvtTagRead, self.__tag_read)
        self.world.add_event_handler(EvtStartNewGame, self.__start_new_game)
        self.world.add_event_handler(EvtUnknownTag, self.__unknown_tag)
        self.world.add_event_handler(EvtTagFound, self.__tag_found)
        self.world.add_event_handler(EvtWrongFood, self.__wrong_food)
        self.world.add_event_handler(EvtCorrectFood, self.__correct_food)
        next_food_group = choice(list(FoodGroup))
        await self.dispatch_event(EvtStartNewGame, food_group=next_food_group)

    async def __start_new_game(self, evt: EvtStartNewGame, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        self.food_group = evt.food_group
        action = self.say_text(f'I am hungry for some {self.food_group.name}')
        await action.wait_for_completed()
        self.ready = True

    async def __unknown_tag(self, evt: EvtUnknownTag, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        action = self.say_text('Hmm, I do not know what that is!')
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
        say = self.say_text(f'A {evt.food_item.name} is not a {evt.expected_food_group.name}', in_parallel=True)
        animate = self.play_anim('BlockReact', in_parallel=True)


        await animate.wait_for_completed()
        await say.wait_for_completed()
        self.ready = True

    async def __correct_food(self, evt: EvtCorrectFood, **kw) -> None:
        cozmo.logger.info(f'recv event {evt}')
        next_food_group = choice(list(FoodGroup))
        msg = f'Yum! The {evt.food_item.food_group.name} {evt.food_item.name} is {evt.food_item.taste}'
        action = self.say_text(msg, play_excited_animation=True)
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


def create_reader(use_fake: bool, tags: List[str]) -> Reader:
    if use_fake:
        return FakeReader(tags)
    return RfidReader()


global coz


async def run(sdk_conn):
    global items
    global coz

    try:
        rbt = await sdk_conn.wait_for_robot()
        action = rbt.say_text('hello')
        await action.wait_for_completed()

        coz = rbt

        def send_tag_read(tag):
            rbt.world.dispatch_event(EvtTagRead, tag=tag)

        await coz.start(items)
        reader.on_tag_read(send_tag_read)

        # Busy wait until you want your program to exit
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("Exited.")


global reader
global items


def main():
    # usage = "usage: %prog [options]"
    # parser = OptionParser(usage=usage)
    # # parser.add_option("-b", "--fakeRobot", action="store_true", dest="useFakeRobot",
    # #                   help="Don't connect to the real cozmo")
    # # parser.add_option("-i", "--fakeReader", action="store_true", dest="useFakeReader",
    # #                   help="Don't connect to the real RFID reader")
    # parser.add_option("-k", "--knownItemFile", dest="knownItemsFile", metavar="FILE",
    #                   help="the file where known items are stored",
    #                   default='items.csv')
    #
    # (options, _ignored_) = parser.parse_args()
    global reader, items
    item_list = load_items('items.csv')
    reader = create_reader(False, list(map(lambda food_item: food_item.tag, item_list)))
    items = dict((item.tag, item) for item in item_list)

    cozmo.setup_basic_logging()

    cozmo.conn.CozmoConnection.robot_factory = TasterBot
    try:
        print('hi')
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: {0}".format(e))


main()
