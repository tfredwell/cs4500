from cozmo.event import Event

from cozmo_taste_game import FoodItem
from cozmo_taste_game.food.food_group import FoodGroup


class EvtTagRead(Event):
    """The event sent when a tag has been read"""
    tag: str = ''


class EvtStartNewGame(Event):
    """The event sent when a new game is started"""
    food_group: FoodGroup = None


class EvtUnknownTag(Event):
    """The event sent when a new game is started"""
    tag: str = ''


class EvtTagFound(Event):
    """The event sent when a new game is started"""
    food_item: FoodItem = None


class EvtWrongFood(Event):
    """The event sent when a new game is started"""
    expected_food_group: FoodGroup = None
    food_item: FoodItem = None


class EvtCorrectFood(Event):
    """The event sent when a new game is started"""
    food_item: FoodItem = None
