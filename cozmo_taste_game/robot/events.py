from cozmo.event import Event

from cozmo_taste_game import FoodItem
from cozmo_taste_game.food.food_group import FoodGroup


class EvtTagRead(Event):
    """
    An event signifying that a RFID tag has been read
    """
    tag: str = ''


class EvtNewGameStarted(Event):
    """
    The event sent when a new game is started
    """
    food_group: FoodGroup = None


class EvtUnknownTag(Event):
    """The event sent when an tag that has been scanned is unknown"""
    tag: str = ''


class EvtWrongFoodGroup(Event):
    """An event signifying that the scanned tag was not in the food group expected"""
    expected_food_group: FoodGroup = None
    food_item: FoodItem = None


class EvtCorrectFoodGroup(Event):
    """An event signifying that the scanned tag was in the food group expected"""
    food_item: FoodItem = None


class EvtNoRobotConnected(Event):
    """An event that occurs when an attempt is made to manipulate a robot that is not connected"""


class EvtRobotConnected(Event):
    """An event that occurs when a robot is connected"""


class EvtRobotDisonnected(Event):
    """An event that occurs when a robot is disconnected"""
