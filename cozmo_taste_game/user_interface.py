from typing import Callable

import wx
import wx.lib.buttons
from wxasync import AsyncBind

from cozmo_taste_game import FoodGroup, GameEngine
from cozmo_taste_game.robot import EvtNewGameStarted, EvtWrongFood, EvtUnknownTag, EvtCorrectFood


class UserInterface(wx.Frame):

    @staticmethod
    def scale_image(bitmap: wx.Bitmap, width, height) -> wx.Bitmap:
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    def create_looking_for_panel(self):

        looking_for_label = wx.StaticText(self, -1, 'Looking For:')
        looking_for_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                          wx.FONTWEIGHT_BOLD, False))

        self.looking_for_text = wx.StaticText(self, -1, '')
        self.looking_for_text.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                              wx.FONTWEIGHT_BOLD, False))

        looking_for_sizer = wx.BoxSizer(wx.HORIZONTAL)
        looking_for_sizer.Add(looking_for_label, 0, wx.ALL | wx.EXPAND, 5)
        looking_for_sizer.Add(self.looking_for_text, 0, wx.ALL | wx.EXPAND, 5)
        return looking_for_sizer

    def create_got_panel(self):
        got_food_name_label = wx.StaticText(self, -1, 'Name:')
        got_food_name_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                            wx.FONTWEIGHT_BOLD, False))

        self.got_food_name_value = wx.StaticText(self, -1, '', size=(160, 20))
        got_food_group_label = wx.StaticText(self, -1, 'Group:')
        got_food_group_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                             wx.FONTWEIGHT_BOLD, False))
        self.got_food_group_value = wx.StaticText(self, -1, '')

        got_food_name_group_sizer = wx.BoxSizer(wx.HORIZONTAL)
        got_food_name_group_sizer.Add(got_food_name_label, 0, wx.ALL | wx.EXPAND, 5)
        got_food_name_group_sizer.Add(self.got_food_name_value, 0, wx.ALL | wx.EXPAND, 5)
        got_food_name_group_sizer.Add(got_food_group_label, 0, wx.ALL | wx.EXPAND, 5)
        got_food_name_group_sizer.Add(self.got_food_group_value, 0, wx.ALL | wx.EXPAND, 5)
        return got_food_name_group_sizer

    def create_tag_entry_panel(self):

        tag_entry_label = wx.StaticText(self, -1, 'Tag Entry:')
        tag_entry_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                    wx.FONTWEIGHT_BOLD, False))
        self.tag_field = wx.TextCtrl(self)
        AsyncBind(wx.EVT_TEXT_ENTER, self.tag_entered, self.tag_field)
        tag_entry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tag_entry_sizer.Add(tag_entry_label, 0, wx.ALIGN_CENTER_VERTICAL)
        tag_entry_sizer.Add(self.tag_field, 1, wx.EXPAND | wx.ALL, 5)
        return tag_entry_sizer

    def create_start_button_panel(self):
        start_game_sizer = wx.BoxSizer(wx.VERTICAL)
        cozmo_bitmap = self.scale_image(wx.Bitmap("cozmo.jpg"), 64, 64)
        start_game_button = wx.lib.buttons.ThemedGenBitmapTextButton(self, -1, cozmo_bitmap, size=(128, 128))
        start_game_sizer.Add(start_game_button, 0, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        start_game_sizer.Add(wx.StaticText(self, -1, 'Start New Game'), 0, wx.CENTER)
        AsyncBind(wx.EVT_BUTTON, self.start_new_game, start_game_button)
        return start_game_sizer

    def create_status_panel(self):

        looking_for = self.create_looking_for_panel()
        got_label = wx.StaticText(self, -1, 'Got:')
        got_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                                  False))
        got = self.create_got_panel()
        panel = wx.BoxSizer(wx.VERTICAL)
        panel.Add(looking_for, 1)
        panel.Add(wx.StaticLine(self), 0, wx.EXPAND, 5)
        panel.Add(got_label, 1)
        panel.Add(got, 1)
        return panel



    def create_game_control_panel(self):

        start_button = self.create_start_button_panel()
        status = self.create_status_panel()
        game_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
        game_ctrl_sizer.Add(start_button, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 20)
        game_ctrl_sizer.Add(status, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 20)
        return game_ctrl_sizer

    def __init__(self, parent=None):
        super(UserInterface, self).__init__(parent)
        self.engine: GameEngine = None



        # top title
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_text = wx.StaticText(self, -1, 'Cozmo Taste Game')
        title_text.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        title_sizer.Add(title_text, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 20)


        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(title_sizer, 0, wx.CENTER)
        root_sizer.Add(wx.StaticLine(self, ), 0, wx.ALL | wx.EXPAND, 5)
        root_sizer.Add(self.create_tag_entry_panel(), 0, wx.ALL | wx.EXPAND, 5)
        root_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND, 5)
        root_sizer.Add(self.create_game_control_panel(), 0, wx.ALL | wx.EXPAND, 5)

        #
        # # game control
        # game_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # root_sizer.Add(game_ctrl_sizer, 0, wx.EXPAND)
        #
        # # start game button
        #
        #
        # # game status sizer
        # game_status_sizer = wx.BoxSizer(wx.VERTICAL)
        # game_ctrl_sizer.Add(game_status_sizer, 0, wx.ALL | wx.EXPAND, 5)
        #
        # looking_for_panel = self.create_looking_for_panel()
        # got_label = wx.StaticText(self, -1, 'Got:')
        # got_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
        #                           False))
        # got_panel = self.create_got_panel()
        #
        # # Looking For:
        #
        # # break
        # game_status_sizer.Add(wx.StaticLine(self, ), 0, wx.ALL | wx.EXPAND, 5)
        #
        # # Got
        # got_label = wx.StaticText(self, -1, 'Got:')
        # got_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
        #                           False))
        # game_status_sizer.Add(got_label, 0, wx.ALL | wx.EXPAND, 5)
        #
        # got_food_name_group_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # game_status_sizer.Add(got_food_name_group_sizer, 0, wx.ALL | wx.EXPAND, 5)
        #
        # got_food_name_label = wx.StaticText(self, -1, 'Name:')
        # got_food_name_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
        #                                     wx.FONTWEIGHT_BOLD, False))
        #
        # self.got_food_name_value = wx.StaticText(self, -1, '')
        # got_food_group_label = wx.StaticText(self, -1, 'Group:')
        # got_food_group_label.SetFont(wx.Font(wx.FONTSIZE_MEDIUM, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
        #                                      wx.FONTWEIGHT_BOLD, False))
        # self.got_food_group_value = wx.StaticText(self, -1, '')
        # #
        # got_food_name_group_sizer.Add(got_food_name_label, 0, wx.ALL | wx.EXPAND, 5)
        # got_food_name_group_sizer.Add(self.got_food_name_value, 0, wx.ALL | wx.EXPAND, 5)
        # got_food_name_group_sizer.Add(got_food_group_label, 0, wx.ALL | wx.EXPAND, 5)
        # got_food_name_group_sizer.Add(self.got_food_group_value, 0, wx.ALL | wx.EXPAND, 5)
        # game_status_sizer.Add(got_food_name_group_sizer, 0, wx.ALL | wx.EXPAND, 5)

        root_sizer.SetSizeHints(self)
        self.SetSizer(root_sizer)
        self.Layout()

    async def start_new_game(self, _):
        await self.engine.start_new_game()

    async def on_new_game(self, event: EvtNewGameStarted):
        self.looking_for_text.SetLabel(f'cozmo wants {event.food_group.name}')

    async def tag_entered(self, _):
        tag = str(self.tag_field.GetValue())
        self.tag_field.Clear()
        await self.engine.tag_read(tag)

    async def on_tag_scanned(self, event):
        if event.event_name == 'EvtWrongFood' or event.event_name == 'EvtCorrectFood':
            self.got_food_name_value.SetLabel(event.food_item.name)
            self.got_food_group_value.SetLabel(event.food_item.food_group.name)

        if event.event_name == 'EvtUnknownTag':
            self.got_food_name_value.SetLabel('Unknown')
            self.got_food_group_value.SetLabel('Unknown')

    def connect(self, engine: GameEngine):
        self.engine = engine
        # Add Handlers
        engine.add_event_hander(EvtNewGameStarted, self.on_new_game)
        engine.add_event_hander(EvtWrongFood, self.on_tag_scanned)
        engine.add_event_hander(EvtUnknownTag, self.on_tag_scanned)
        engine.add_event_hander(EvtCorrectFood, self.on_tag_scanned)
