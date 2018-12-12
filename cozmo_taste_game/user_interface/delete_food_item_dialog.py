import wx

from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.user_interface import helpers


class DeleteFoodItemDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE

        if "food_manager" in kwds:
            self.food_manager:FoodManager = kwds.get("food_manager")
            del kwds["food_manager"]
        wx.Dialog.__init__(self, *args, **kwds)

        self.Bind(wx.EVT_CLOSE, self.on_cancel)
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_ctrl_2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.combo_box_1 = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.text_ctrl_3 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_1 = wx.Button(self, wx.ID_ANY, "button_1")

        self.__set_properties()
        self.__do_layout()

    # end wxGlade

    def __set_properties(self):
        # begin wxGlade: DeleteFoodItemDialog.__set_properties
        self.SetTitle("Delete Food Item")
        _icon = wx.NullIcon

        _icon.CopyFromBitmap(helpers.load_image("resources/cozmo.jpg"))
        self.SetIcon(_icon)

    # end wxGlade
    def on_cancel(self, _):
        self.Destroy()

    def __do_layout(self):
        # begin wxGlade: DeleteFoodItemDialog.__do_layout
        grid_sizer_1 = wx.GridSizer(0, 2, 5, 5)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Tag")
        grid_sizer_1.Add(label_2, 0, 0, 0)
        grid_sizer_1.Add(self.text_ctrl_1, 0, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "Name")
        grid_sizer_1.Add(label_3, 0, 0, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 0, 0, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "Group")
        grid_sizer_1.Add(label_4, 0, 0, 0)
        grid_sizer_1.Add(self.combo_box_1, 0, 0, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Taste")
        grid_sizer_1.Add(label_5, 0, 0, 0)
        grid_sizer_1.Add(self.text_ctrl_3, 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add(self.button_1, 0, 0, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self)
        self.Layout()
    # end wxGlade

# end of class DeleteFoodItemDialog
