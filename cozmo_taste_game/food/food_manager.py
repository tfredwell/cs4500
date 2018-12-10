from typing import Optional, Mapping, List
from copy import deepcopy
from cozmo_taste_game import FoodItem, FoodGroup
from os import path


class FoodManager:
    """
    A class for managing food items that are stored in a csv database file.
    """

    def __init__(self, file_name: str) -> None:
        """
        Creates a new instance of the __name__ class
        :param file_name: the name of the file to open
        """
        self.food_file_path = path.abspath(path.join(path.dirname(path.dirname(__file__)), file_name))
        self.foods = dict()

    def load_items(self) -> None:
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

    async def add_item(self, item: FoodItem) -> None:
        """
        adds an item to the food manager
        :param item: the item to add
        """
        with open(self.food_file_path, 'a+') as file:  # Use file to refer to the file object
            line = f'\n{item.tag},{item.name},{item.food_group.name},{item.taste}'
            file.write(line)
        self.foods[item.tag] = item

    def get_items(self) -> Mapping[str, FoodItem]:
        """
        Retrieves a copy of all the registered food items where the key is a tag and the value is :class:FoodItem
        This is a deep copied object, modifications to the returned will _NOT_ be reflected in the manager
        :return: Mapping[str, FoodItem] of all items known to the manager
        """
        return deepcopy(self.foods)

    async def delete_item(self, item: FoodItem) -> None:
        """
        Deletes an item from the manager if it exists. If the item does not exist then the item is just ignored.
        :param item: :class:FoodItem to be deleted
        """
        if item.tag in self.foods:
            del self.foods[item.tag]
            await self.__rewrite_file()

    async def edit_item(self, old_item: FoodItem, new_item: FoodItem) -> None:
        """
        Edits an item from the food manager it it exists. If the item does not exist it will be added
        :param old_item: The old :class:FoodItem to be edited
        :param new_item: The new :class:FoodItem with updated values
        """
        if old_item.tag in self.foods:
            del self.foods[old_item.tag]
            self.foods[new_item.tag] = new_item
            await self.__rewrite_file()
        else:
            await self.add_item(new_item)

    async def __rewrite_file(self) -> None:
        """
        Rewrites the database file with all of the FoodItems currently in memory.
        """
        with open(self.food_file_path, 'r') as file:  # Use file to refer to the file object
            for item in self.foods:
                line = f'\n{item.tag},{item.name},{item.food_group.name},{item.taste}'
                file.write(line)

    def get_by_tag(self, tag: str) -> Optional[FoodItem]:
        """
        Retrieves a food item based on its tag
        :param tag: The tag associated with the :class:FoodItem
        :return: a food item if the tag is known, None otherwise.
        """
        if tag in self.foods:
            return self.foods[tag]
        return None

    @staticmethod
    def get_food_group_names() -> List[str]:
        """
        Helper function to get a list of all known food items
        :return: a list of all known food types
        """
        return [group.name for group_name, group in FoodGroup.__members__.items()]
