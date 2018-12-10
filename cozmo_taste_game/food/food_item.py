from cozmo_taste_game.food.food_group import FoodGroup


class FoodItem:
    """
    A food item is the food group, name and taste of an food game piece
    """
    def __init__(self, tag: str, food_group: FoodGroup, name: str, taste: str) -> None:
        """
        creates a new instance of a food item
        :param tag: the RFID tag number
        :param food_group:  the :class:FoodGroup that the food item belongs to
        :param name: the name of the food item
        :param taste: what the item tastes like
        """
        self.tag = tag
        self.food_group = food_group
        self.name = name
        self.taste = taste
