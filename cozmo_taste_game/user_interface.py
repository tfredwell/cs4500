from typing import Callable

import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
import time

from cozmo_taste_game import FoodGroup


class UserInterface(wx.Frame):

    @staticmethod
    def scale_image(bitmap: wx.Bitmap, width, height) -> wx.Bitmap:
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    def __init__(self, parent=None):
        super(UserInterface, self).__init__(parent)
        self.tag_callback = None
        self.new_game_callback = None

        root_sizer = wx.BoxSizer(wx.VERTICAL)

        # top title
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_text = wx.StaticText(self, -1, 'Cozmo Taste Game', (20, 800))
        title_text.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        title_sizer.Add(title_text)

        # start game button
        start_game_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cozmo_bitmap = self.scale_image(wx.Bitmap("cozmo.jpg"), 64, 64)
        start_game_button = wx.BitmapButton (self, bitmap=cozmo_bitmap)
        start_game_button.SetLabel('Start')
        start_game_sizer.Add(start_game_button)
        AsyncBind(wx.EVT_BUTTON, self.start_new_game, start_game_button)

        # target food group
        food_group_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.food_group_text = wx.StaticText(self, -1, '', (20, 800))
        food_group_sizer.Add(self.food_group_text)

        # tag entry
        tag_entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tag_text_ctrl = wx.TextCtrl(self)
        AsyncBind(wx.EVT_TEXT_ENTER, self.txt_ctrl_date_entered, self.tag_text_ctrl)
        tag_entry_sizer.Add(self.tag_text_ctrl)
        self.last_read_tag = wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        tag_entry_sizer.Add(self.last_read_tag, 1, wx.EXPAND | wx.ALL)

        # set up the layout
        root_sizer.Add(title_sizer, 0, wx.CENTER)
        root_sizer.Add(wx.StaticLine(self,), 0, wx.ALL|wx.EXPAND, 5)
        root_sizer.Add(tag_entry_sizer, 0, wx.ALL|wx.EXPAND, 5)
        root_sizer.Add(start_game_sizer, 0, wx.ALL|wx.EXPAND, 5)
        root_sizer.Add(food_group_sizer, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(root_sizer)
        self.Layout()

    async def start_new_game(self, _):
        if self.new_game_callback:
            self.tag_text_ctrl.SetFocus()
            food_group = await self.new_game_callback()
            self.food_group_text.SetLabel(f'cozmo wants {food_group.name}')

    async def txt_ctrl_date_entered(self, _):
        tag = str(self.tag_text_ctrl.GetValue())
        self.tag_text_ctrl.Clear()
        self.last_read_tag.SetLabel(tag)
        if self.tag_callback:
            await self.tag_callback(tag)

    def on_tag_read(self, callback: Callable[[str], None]) -> None:
        self.tag_callback = callback

    def on_game_start(self, callback: Callable[[FoodGroup], None]) -> None:
        self.new_game_callback = callback

