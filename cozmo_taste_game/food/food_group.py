from enum import Enum


class FoodGroup(Enum):
    """
    A classification of food according to https://www.choosemyplate.gov/MyPlate
    """
    protein = 0
    fruit = 1
    vegetable = 2
    grain = 3
    dairy = 4
    oil = 5
