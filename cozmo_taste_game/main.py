#!/usr/bin/env python3

import asyncio
import logging
import sys
import traceback

import cozmo

from cozmo_taste_game import RealTasterBot, GameEngine
from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.user_interface.app import CozmoTasteGame

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
root.addHandler(handler)

logger = logging.getLogger('cozmo_taste_game.main')



def main() -> None:

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    root.addHandler(handler)

    food_manager = FoodManager("items.csv")
    food_manager.load_items()

    loop = asyncio.get_event_loop()
    engine = GameEngine(food_manager, RealTasterBot())

    game = CozmoTasteGame(engine, food_manager)

    loop.run_until_complete(game.main_loop())

main()
