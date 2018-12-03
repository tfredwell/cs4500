from typing import Callable

import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
import time

class UserInterface(wx.Frame):

    def __init__(self, parent=None):
        super(UserInterface, self).__init__(parent)
        self.tag_callback = None
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.tag_text_ctrl = wx.TextCtrl(self)
        AsyncBind(wx.EVT_TEXT_ENTER, self.txt_ctrl_date_entered, self.tag_text_ctrl)
        vbox.Add(self.tag_text_ctrl)
        self.last_read_tag = wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        vbox.Add(self.last_read_tag, 1, wx.EXPAND | wx.ALL)
        #
        # button1 =  wx.Button(self, label="Submit")
        # self.edit =  wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        # self.edit_timer =  wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_NO_AUTORESIZE)
        # vbox.Add(button1, 2, wx.EXPAND|wx.ALL)
        # vbox.AddStretchSpacer(1)
        # vbox.Add(self.edit, 1, wx.EXPAND|wx.ALL)
        # vbox.Add(self.edit_timer, 1, wx.EXPAND|wx.ALL)

        self.SetSizer(vbox)
        self.Layout()
        # AsyncBind(wx.EVT_BUTTON, self.async_callback, button1)
        # StartCoroutine(self.update_clock, self)

    async def async_callback(self, event):
        self.edit.SetLabel("Button clicked")
        await asyncio.sleep(1)
        self.edit.SetLabel("Working")
        await asyncio.sleep(1)
        self.edit.SetLabel("Completed")

    async def update_clock(self):
        while True:
            self.edit_timer.SetLabel(time.strftime('%H:%M:%S'))
            await asyncio.sleep(0.5)

    async def txt_ctrl_date_entered(self, event):
        tag = str(self.tag_text_ctrl.GetValue())
        self.tag_text_ctrl.Clear()
        self.last_read_tag.SetLabel(tag)
        if self.tag_callback:
            await self.tag_callback(tag)

    def on_tag_read(self, callback: Callable[[str], None]) -> None:
        self.tag_callback = callback

# class UserInterface:
#     def __init__(self, coz, loop):
#         self.cozmo = coz
#         self.loop = loop
#         self.app = wx.App(False)
#         self.frame = wx.Frame(None, title="Cozmo Taste Game", size=(10000, 10000))
#         self.panel = wx.Panel(self.frame)
#
#     def start(self):
#         self.panel.Bind(wx.EVT_PAINT, self.on_paint)
#         self.frame.Show(True)
#         self.app.MainLoop()
#
#     def on_paint(self, event):
#         dc = wx.PaintDC(event.GetEventObject())
#         dc.SetPen(wx.Pen("BLACK", 1))
#         dc.DrawLine(0, 100, 100000000, 100)  # Horizontal line
#         dc.DrawLine(1000, 0, 1000, 100)  # Line divider
#         dc.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
#         dc.DrawText("Cozmo Taste Game", 100, 30)
#
#         dc.SetBrush(wx.Brush(wx.RED))
#         dc.DrawLine(1050, 0, 1050, 100)  # Line divider
#         dc.DrawCircle(1150, 50, 20)  # Cozmo
#         dc.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
#         dc.DrawText("Cozmo", 1125, 75)
#
#         dc.DrawLine(1250, 0, 1250, 100)  # Line divider
#         dc.DrawCircle(1350, 50, 20)  # RFID
#         dc.DrawText("RFID", 1333, 75)
#
#         # This shows the drawn picture
#         dc.SetFont(wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
#         dc.DrawText("SCANNED ITEM", 100, 200)
#         img = wx.Bitmap("lemon.jpg")
#         img.SetWidth(1000)
#         img.SetHeight(1000)
#         dc.DrawBitmap(img, 100, 300)  # Display the image to the screen
#
#     desc = wx.StaticText(panel, -1, "Cozmo Status", pos=(1050, 430))
# font = wx.Font(35, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
# desc.SetFont(font)
#
# # Cozmo Status Textbox
# status = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(400, 30), pos=(1000, 500))
# status.SetBackgroundColour("white")
# status.SetMaxLength(15)
# font = wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
# status.SetFont(font)
#
# # Botton to restart game
# btn = wx.Button(panel, -1, "Restart Game", size=(300, 100), pos=(1050, 560))
# btn.Bind(wx.EVT_BUTTON, OnClicked)
#
#
# def printTag(tagNumber):
#     global robot
#     if robot is not None:
#         msg = f'I see tag {tagNumber}'
#         print(f'Cozmo Says {msg}')
#
#         robot.speak(msg)
#     else:
#         print('cozmo not here')
#         print(tagNumber)
#     print('done')
#
#
# tagBuffer = []
#
#
# def on_key(event):
#     global tagBuffer
#     keycode = event.GetKeyCode()
#     tagBuffer.append(chr(keycode))
#     if len(tagBuffer) == 10:
#         printTag(''.join(tagBuffer))
#         tagBuffer = []
#
#
# # Draw the interface and display it on the screen
# panel.Bind(wx.EVT_PAINT, on_paint)
# panel.Bind(wx.EVT_KEY_DOWN, on_key)
#
#
# def new_cozmo_pgm():
#     frame.Show(True)
#
#     # Cozmo status label
#     desc = wx.StaticText(panel, -1, "Cozmo Status", pos=(1050, 430))
#     font = wx.Font(35, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
#     desc.SetFont(font)
#
#     # Cozmo Status Textbox
#     status = wx.TextCtrl(panel, style=wx.TE_READONLY, size=(400, 30), pos=(1000, 500))
#     status.SetBackgroundColour("white")
#     status.SetMaxLength(15)
#     font = wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
#     status.SetFont(font)
#
#     # Botton to restart game
#     btn = wx.Button(panel, -1, "Restart Game", size=(300, 100), pos=(1050, 560))
#     btn.Bind(wx.EVT_BUTTON, OnClicked)
#
#     # Function that gets cozmos status
#     cozmo_status(status)
#     #
#     # global robot
#     # rbt =  RealTasterBot(czmo)
#     # robot = rbt
#     app.MainLoop()
#
#     print('exiting')
#
#
# # Starts a new game
# def OnClicked(event):
#     print("New Game")
#     cozmo.run_program(new_cozmo_pgm)
#
#
# def cozmo_status(status):
#     # Gets status value from cozom
#     status.SetValue("Test")
#
#
# new_cozmo_pgm()
