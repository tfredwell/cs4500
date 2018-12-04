import wx
from wxasync import AsyncBind
import wx.lib.buttons
from cozmo_taste_game.robot import EvtNewGameStarted, EvtWrongFood, EvtUnknownTag, EvtCorrectFood
from cozmo_taste_game.user_interface import helpers
from cozmo_taste_game.user_interface.AddFoodItemDialog import AddFoodItemDialog
from cozmo_taste_game.user_interface.DeleteFoodItemDialog import DeleteFoodItemDialog
from cozmo_taste_game.user_interface.EditFoodItemDialog import EditFoodItemDialog
from cozmo_taste_game.user_interface.LogPanel import LogPanel


class UserInterface(wx.Frame):
    def __init__(self, game_engine, *args, **kwds):
        # begin wxGlade: UserInterface.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        self.game_engine = game_engine
        wx.Frame.__init__(self, *args, **kwds)
        self.cozmo_bitmap = helpers.load_image("cozmo.jpg")
        self.connected_bitmap = helpers.scale_image(helpers.load_image("disconnected.jpg"), 64)
        self.disconnected_bitmap =  helpers.scale_image(helpers.load_image("connected.jpg"), 64)

        self.game_engine.add_event_hander(EvtNewGameStarted, self.on_new_game)
        self.game_engine.add_event_hander(EvtWrongFood, self.on_tag_scanned)
        self.game_engine.add_event_hander(EvtUnknownTag, self.on_tag_scanned)
        self.game_engine.add_event_hander(EvtCorrectFood, self.on_tag_scanned)

        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        food_management_menu = wx.Menu()
        new_item = food_management_menu.Append(wx.ID_NEW, "New", "Click to add a new food item")
        edit_item = food_management_menu.Append(wx.ID_EDIT, "Edit", "Click to add a new food item")
        delete_item = food_management_menu.Append(wx.ID_DELETE, "Delete", "Click to remove a food item")

        self.Bind(wx.EVT_MENU, self.show_add_new_food, id=new_item.GetId())
        self.Bind(wx.EVT_MENU, self.show_edit_food, id=edit_item.GetId())
        self.Bind(wx.EVT_MENU, self.show_remove_food, id=delete_item.GetId())
        self.frame_menubar.Append(food_management_menu, "&Manage Food")





        info_menu = wx.Menu()
        item = info_menu.Append(wx.ID_ANY, "Show Log", "Click to display logging information")
        self.Bind(wx.EVT_MENU, self.show_logs, id=item.GetId())

        self.frame_menubar.Append(info_menu, "Information")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end


        self.connect_toggle = wx.lib.buttons.ThemedGenBitmapTextButton(self, -1, self.disconnected_bitmap, size=(72, 72))
        self.connected_label_text = wx.StaticText(self, wx.ID_ANY, "Connect", style=wx.ALIGN_CENTER)
        self.text_tag_entry = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)


        cozmo_bitmap = helpers.scale_image(self.cozmo_bitmap, 118)


        self.start_game_button =start_game_button = wx.lib.buttons.ThemedGenBitmapTextButton(self, -1, cozmo_bitmap, size=(128, 128))
        self.food_group_looking_for = wx.StaticText(self, wx.ID_ANY, "")
        self.received_label = wx.StaticText(self, wx.ID_ANY, "")

        self.__set_properties()
        self.__do_layout()

        AsyncBind(wx.EVT_BUTTON, self.connect_toggle_clicked, self.connect_toggle)
        AsyncBind(wx.EVT_TEXT_ENTER, self.on_tag_entered, self.text_tag_entry)
        AsyncBind(wx.EVT_BUTTON, self.start_game_clicked, self.start_game_button)

    def __set_properties(self):
        # begin wxGlade: UserInterface.__set_properties
        self.SetTitle("Cozmo Taste Game")


        _icon = wx.NullIcon
        _icon.CopyFromBitmap(self.cozmo_bitmap)
        self.SetIcon(_icon)
        self.SetFocus()
        self.text_tag_entry.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.text_tag_entry.SetFocus()
        self.start_game_button.SetMinSize((128, 128))
        self.food_group_looking_for.SetForegroundColour(wx.Colour(255, 255, 0))
        self.food_group_looking_for.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.received_label.SetForegroundColour(wx.Colour(255, 255, 0))
        self.received_label.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.child = None

    # end wxGlade

    def __do_layout(self):
        # begin wxGlade: UserInterface.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Game Controls"), wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Game Piece Entry"), wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        game_title = wx.StaticText(self, wx.ID_ANY, "Cozmo Taste Game", style=wx.ALIGN_CENTER)
        game_title.SetFont(wx.Font(50, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_6.Add(game_title, 10, 0, 0)
        sizer_7.Add(self.connect_toggle, 4, 0, 0)
        sizer_7.Add(self.connected_label_text, 1, wx.ALIGN_CENTER, 0)
        sizer_6.Add(sizer_7, 1, wx.ALL | wx.EXPAND, 6)
        sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        tag_entry_label = wx.StaticText(self, wx.ID_ANY, "Tag:", style=wx.ALIGN_CENTER)
        tag_entry_label.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_5.Add(tag_entry_label, 0, 0, 0)
        sizer_5.Add(self.text_tag_entry, 6, wx.ALL | wx.EXPAND, 1)
        sizer_1.Add(sizer_5, 1, wx.ALL | wx.EXPAND, 5)
        sizer_4.Add(self.start_game_button, 0, 0, 0)
        start_game_label = wx.StaticText(self, wx.ID_ANY, "Start Game", style=wx.ALIGN_CENTER)
        sizer_4.Add(start_game_label, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)
        sizer_2.Add(static_line_1, 0, wx.EXPAND, 0)
        looking_for_label = wx.StaticText(self, wx.ID_ANY, "Looking For")
        looking_for_label.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_3.Add(looking_for_label, 0, 0, 0)
        sizer_3.Add(self.food_group_looking_for, 0, 0, 0)
        control_seperator = wx.StaticLine(self, wx.ID_ANY)
        sizer_3.Add(control_seperator, 0, wx.EXPAND, 0)
        label_got = wx.StaticText(self, wx.ID_ANY, "Received")
        label_got.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_3.Add(label_got, 0, 0, 0)
        sizer_3.Add(self.received_label, 0, 0, 0)
        sizer_2.Add(sizer_3, 6, wx.ALL | wx.EXPAND, 5)
        sizer_1.Add(sizer_2, 2, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

    # end wxGlade

    def save_new_item(self, item):
        self.game_engine.add_food_item(item)


    def show_add_new_food(self, event):  # wxGlade: UserInterface.<event_handler>
        if not self.child:
            child = AddFoodItemDialog(self)
            child.save_callback = self.save_new_item
            self.child = child
            self.child.Show()

    def show_edit_food(self, event):  # wxGlade: UserInterface.<event_handler>
        self.child = EditFoodItemDialog(self)
        self.child.Show()

    def show_remove_food(self, event):  # wxGlade: UserInterface.<event_handler>
        self.child = DeleteFoodItemDialog(self)
        self.child.Show()

    def show_logs(self, event):  # wxGlade: UserInterface.<event_handler>
        self.child = LogPanel(self)
        self.child.Show()

    async def connect_toggle_clicked(self, event):  # wxGlade: UserInterface.<event_handler>
        await self.game_engine.toggle_robot_connect()


    async def start_game_clicked(self, event):  # wxGlade: UserInterface.<event_handler>
        print('starting game')
        await self.game_engine.start_new_game()

    async def on_new_game(self, event: EvtNewGameStarted):
        self.food_group_looking_for.SetLabel(f'cozmo wants {event.food_group.name}')
        self.received_label.SetLabel('')
        self.text_tag_entry.SetFocus()

    async def on_tag_entered(self, _):
        tag = str(self.text_tag_entry.GetValue())

        self.text_tag_entry.Clear()
        await self.game_engine.tag_read(tag)

    async def on_tag_scanned(self, event):
        food_name = 'Unknown'
        food_group = 'Unknown'

        if event.event_name == 'EvtWrongFood' or event.event_name == 'EvtCorrectFood':
            food_name = event.food_item.name
            food_group = event.food_item.food_group.name

        self.received_label.SetLabel(f'{food_name} - {food_group}')

    async  def handle_menu(self, event):
        print(event)
        event.skip()
# end of class UserInterface
