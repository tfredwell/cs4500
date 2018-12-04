from typing import Optional

from cozmo_taste_game import FoodItem, FoodGroup
from os import path


class FoodManager:

    def __init__(self, file_name):
        self.food_file_path = path.abspath(path.join(path.dirname(path.dirname(__file__)), file_name))
        self.foods = dict()

    def load_items(self):
        if path.isfile(self.food_file_path):
            with open(self.food_file_path) as item_file:
                for line in item_file:
                    line = line.strip()
                    if line.startswith('#'):
                        continue
                    else:
                        (tag, name, group, taste) = line.lower().split(',')

                        item = FoodItem(tag=tag, name=name, food_group=FoodGroup[group.strip()], taste=taste.strip())
                        self.foods[item.tag] = item

    async def add_item(self, item: FoodItem):
        with open(self.food_file_path, 'a+') as file:  # Use file to refer to the file object
            line = f'\n{item.tag},{item.name},{item.food_group.name},{item.taste}'
            file.write(line)
        self.foods[item.tag] = item

    async def delete_item(self, item: FoodItem):
        if item.tag in self.foods:
            del self.foods[item.tag]
            self.rewrite_file()

    async def edit_item(self, old_item: FoodItem, new_item: FoodItem):
        if old_item.tag in self.foods:
            del self.foods[old_item.tag]
            self.foods[new_item.tag] = new_item
            self.rewrite_file()

    async def rewrite_file(self):
        with open(self.food_file_path, 'r') as file:  # Use file to refer to the file object
            for item in self.foods:
                line = f'\n{item.tag},{item.name},{item.food_group.name},{item.taste}'
                file.write(line)

    def get_by_tag(self, tag: str) -> Optional[FoodItem]:
        if tag in self.foods:
            return self.foods[tag]
        return None
