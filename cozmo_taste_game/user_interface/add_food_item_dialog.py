import wx
from wxasync import AsyncBind
from cozmo_taste_game import FoodItem, FoodGroup
from cozmo_taste_game.food.food_manager import FoodManager
from cozmo_taste_game.user_interface import helpers


class AddOrEditFoodItemDialog(wx.Dialog):
    """
    The user interface for adding or editing a food item
    """

    def __init__(self, *args, **kwds):

        food_groups = []
        for group in list(FoodGroup):
            food_groups.append(group.name)

        if "food_manager" in kwds:
            self.food_manager:FoodManager = kwds.get("food_manager")
            del kwds["food_manager"]

        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)

        self.Bind(wx.EVT_CLOSE, self.on_cancel)

        self.tag_text_control = wx.TextCtrl(self, wx.ID_ANY, "")
        self.name_text_control = wx.TextCtrl(self, wx.ID_ANY, "")
        self.food_group_combo = wx.ComboBox(self, wx.ID_ANY, choices=self.food_manager.get_food_group_names(), style=wx.CB_READONLY)
        self.taste_text_control = wx.TextCtrl(self, wx.ID_ANY, "")

        self.add_button = wx.Button(self, wx.ID_ANY, "Add")
        self.cancel_button = wx.Button(self, wx.ID_ANY, "Cancel")

        AsyncBind(wx.EVT_BUTTON, self.on_save, self.add_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_button)
        self.__set_properties()
        self.__do_layout()
        self.save_callback = None

    # end wxGlade
    def connect(self, save_callback):
        self.save_callback = save_callback

    def __set_properties(self):
        self.SetTitle("Add Food Item")
        self.cozmo_bitmap = helpers.load_image("resources/cozmo.jpg")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(self.cozmo_bitmap)
        self.SetIcon(_icon)

    # end wxGlade

    def __do_layout(self):

        sz = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Add new item"), wx.HORIZONTAL)

        sizer = wx.GridBagSizer(hgap=5, vgap=5)

        tag_label = wx.StaticText(self, wx.ID_ANY, "Tag")
        sizer.Add(tag_label, pos=(0, 0), border=5)
        sizer.Add(self.tag_text_control, pos=(0, 1), border=5)

        name_label = wx.StaticText(self, wx.ID_ANY, "Name")
        sizer.Add(name_label, pos=(1, 0), border=5)
        sizer.Add(self.name_text_control, pos=(1, 1), border=5)

        group_label = wx.StaticText(self, wx.ID_ANY, "Group")
        sizer.Add(group_label, pos=(2, 0), border=5)
        sizer.Add(self.food_group_combo, pos=(2, 1), border=5)

        taste_label = wx.StaticText(self, wx.ID_ANY, "Taste")
        sizer.Add(taste_label, pos=(3, 0), border=5)
        sizer.Add(self.taste_text_control, pos=(3, 1), border=5)

        sizer.Add(self.cancel_button, pos=(4, 0), border=5)
        sizer.Add(self.add_button, pos=(4, 1), border=5)

        sz.Add(sizer, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        self.SetSizer(sz)
        sz.Fit(self)
        self.Layout()

    def on_cancel(self, _):
        self.Destroy()

    @staticmethod
    def extract_value(control):
        return str(control.GetValue()).lower().strip()

    async def on_save(self, _) -> None:
        """
        Handles a save event for the FoodItem
        :param _: ignored event params
        :return: None
        """
        print('saving')
        if self.can_save():
            tag = self.extract_value(self.tag_text_control)
            name = self.extract_value(self.name_text_control)
            group = self.extract_value(self.food_group_combo)
            taste = self.extract_value(self.taste_text_control)

            new_item = FoodItem(tag=tag, name=name, food_group=FoodGroup[group], taste=taste)
            added_item = await self.food_manager.add_item(new_item)
            print(added_item)
            if added_item:
                wx.MessageBox(f'{name} was successfully saved', parent=self)
                self.Destroy()
            else:
                wx.MessageBox(f'{name} was not saved', parent=self)
        else:
            wx.MessageBox('All fields must be entered', parent=self)

    def has_text(self, control):
        return len(self.extract_value(control)) > 1

    def can_save(self) -> bool:
        controls = [self.tag_text_control, self.taste_text_control, self.food_group_combo, self.name_text_control]
        return all(self.has_text(ctrl) for ctrl in controls)
