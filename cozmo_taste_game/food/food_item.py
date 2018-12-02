from cozmo_taste_game.food.food_group import FoodGroup


class FoodItem:
    def __init__(self, tag: str, food_group: FoodGroup, name: str, taste: str):
        self.tag = tag
        self.food_group = food_group
        self.name = name
        self.taste = taste
