"""This is the module contents for cozmo_taste_game."""

from .food import FoodProp, get_food, FoodItem
from .rfid import Reader, FakeReader, RfidReader
from .robot import FakeCozmo, RealTasterBot
from .plate import ColorfulPlate
