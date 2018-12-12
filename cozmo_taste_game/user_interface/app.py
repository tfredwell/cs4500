import wx
from wxasync import WxAsyncApp

from cozmo_taste_game import GameEngine
from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.user_interface.cozmo_taste_game_ui import CozmoTasteGameUI


class CozmoTasteGame:
    """
    Boot straps a new instance of the CozmoTasteGame user interface
    """

    def __init__(self, game_engine: GameEngine, food_item_manager: FoodManager):
        self.game_engine = game_engine
        self.food_item_manager = food_item_manager

    async def main_loop(self):
        app = WxAsyncApp()
        interface = CozmoTasteGameUI(self.game_engine, self.food_item_manager, None, wx.ID_ANY, "")
        app.SetTopWindow(interface)
        interface.Show()
        await app.MainLoop()
