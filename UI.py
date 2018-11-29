import wx
import threading
import cozmo
import os
import shutil
from sys import argv
from time import sleep
from random import choice
import serial.tools.list_ports
from cozmo_taste_game import FakeRobot, CozmoRobot

# Application, frame, and frame are declared
app = wx.App(False)
frame = wx.Frame(None, title="Cozmo Taste Game", size = (10000, 10000))
panel = wx.Panel(frame)
global robot
# Event method to draw the the game UI
def on_paint(event):
    dc = wx.PaintDC(event.GetEventObject())
    dc.SetPen(wx.Pen("BLACK", 1))
    dc.DrawLine(0, 100, 100000000, 100) # Horizontal line
    dc.DrawLine(1000, 0, 1000, 100) # Line divider
    dc.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
    dc.DrawText("Cozmo Taste Game", 100, 30)

    dc.SetBrush(wx.Brush(wx.RED))
    dc.DrawLine(1050, 0, 1050, 100)  # Line divider
    dc.DrawCircle(1150, 50, 20) # Cozmo
    dc.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
    dc.DrawText("Cozmo", 1125, 75)

    dc.DrawLine(1250, 0, 1250, 100)  # Line divider
    dc.DrawCircle(1350, 50, 20) # RFID
    dc.DrawText("RFID", 1333, 75)

    # This shows the drawn picture
    dc.SetFont(wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
    dc.DrawText("SCANNED ITEM", 100, 200)
    img = wx.Bitmap("lemon.jpg")
    img.SetWidth(1000)
    img.SetHeight(1000)
    dc.DrawBitmap(img, 100, 300) # Display the image to the screen

def printTag(tagNumber):
    global robot
    if robot is not None:
        msg = f'I see tag {tagNumber}'
        print(f'Cozmo Says {msg}')

        robot.speak(msg)
    else:
        print('cozmo not here')
        print(tagNumber)
    print('done')

tagBuffer = []
def on_key(event):
    global tagBuffer
    keycode = event.GetKeyCode()
    tagBuffer.append(chr(keycode))
    if len(tagBuffer) == 10:
        printTag(''.join(tagBuffer))
        tagBuffer = []


# Draw the interface and display it on the screen
panel.Bind(wx.EVT_PAINT, on_paint)
panel.Bind(wx.EVT_KEY_DOWN, on_key)



def new_cozmo_pgm(czmo):
    frame.Show(True)
    global robot
    rbt =  CozmoRobot(czmo)
    robot = rbt
    app.MainLoop()
    print('exiting')

print('hi')
cozmo.run_program(new_cozmo_pgm)

