import wx
from wxasync import AsyncBind

from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.user_interface import helpers


class DeleteFoodItemDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE

        if "food_manager" in kwds:
            self.food_manager: FoodManager = kwds.get("food_manager")
            del kwds["food_manager"]
        wx.Dialog.__init__(self, *args, **kwds)

        self.Bind(wx.EVT_CLOSE, self.on_cancel)
        self.tag_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.name_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.group_combo = wx.ComboBox(self, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.taste_text = wx.TextCtrl(self, wx.ID_ANY, "")
        self.delete_button = wx.Button(self, wx.ID_ANY, "Delete Item")
        AsyncBind(wx.EVT_TEXT_ENTER, self.on_tag_entered, self.tag_text)
        AsyncBind(wx.EVT_BUTTON, self.on_delete, self.delete_button)
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("Delete Food Item")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(helpers.load_image("resources/cozmo.jpg"))
        self.SetIcon(_icon)
        self.name_text.Disable()
        self.group_combo.Disable()
        self.taste_text.Disable()

    # end wxGlade
    def on_cancel(self, _):
        self.Destroy()

    async def on_delete(self, _):
        tag = str(self.tag_text.GetValue())
        item = self.food_manager.get_by_tag(tag)
        print(item)
        await self.food_manager.delete_item(item)
        wx.MessageBox("The item was deleted!")
        self.Destroy()

    async def on_tag_entered(self, _):
        tag = str(self.tag_text.GetValue())
        item = self.food_manager.get_by_tag(tag)
        if item is not None:
            self.taste_text.SetLabel(item.taste)
            self.name_text.SetLabel(item.name)
            self.group_combo.SetValue(item.food_group.name)
            self.delete_button.Enable()
        else:
            wx.MessageBox("No item exists for that tag!")
            self.delete_button.Disable()

    def __do_layout(self):
        # begin wxGlade: DeleteFoodItemDialog.__do_layout
        sz = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Delete item"), wx.HORIZONTAL)

        sizer = wx.GridBagSizer(hgap=5, vgap=5)

        tag_label = wx.StaticText(self, wx.ID_ANY, "Tag")
        sizer.Add(tag_label, pos=(0, 0), border=5)
        sizer.Add(self.tag_text, pos=(0, 1), border=5)

        name_label = wx.StaticText(self, wx.ID_ANY, "Name")
        sizer.Add(name_label, pos=(1, 0), border=5)
        sizer.Add(self.name_text, pos=(1, 1), border=5)

        group_label = wx.StaticText(self, wx.ID_ANY, "Group")
        sizer.Add(group_label, pos=(2, 0), border=5)
        sizer.Add(self.group_combo, pos=(2, 1), border=5)

        taste_label = wx.StaticText(self, wx.ID_ANY, "Taste")
        sizer.Add(taste_label, pos=(3, 0), border=5)
        sizer.Add(self.taste_text, pos=(3, 1), border=5)
        sizer.Add(self.delete_button, pos=(4, 1), border=5)
        sz.Add(sizer, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        self.SetSizer(sz)
        sz.Fit(self)
        self.Layout()
    # end wxGlade

# end of class DeleteFoodItemDialog
