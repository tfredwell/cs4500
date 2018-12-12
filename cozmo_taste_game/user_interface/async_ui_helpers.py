from asyncio.events import get_event_loop
import asyncio
import wx
import warnings
from asyncio.futures import CancelledError
from collections import defaultdict
import platform
from asyncio.locks import Event

from asyncio.coroutines import iscoroutinefunction

from wxasync import WxAsyncApp, AsyncBind


def AsyncBindParams(event_binder, async_callback, object, id=wx.ID_ANY, id2=wx.ID_ANY):


    """Bind a coroutine to a wx Event. Note that when wx object is destroyed, any coroutine still running will be cancelled automatically.
    """
    app = wx.App.Get()
    if type(app) is not WxAsyncApp:
        raise Exception("Create a 'WxAsyncApp' first")

    if not iscoroutinefunction(async_callback):
        raise Exception("async_callback is not a coroutine function")
    if object not in app.BoundObjects:
        app.BoundObjects[object] = defaultdict(list)
        object.Bind(wx.EVT_WINDOW_DESTROY, lambda event: app.OnDestroy(event, object))
    app.BoundObjects[object][event_binder.typeId].append(async_callback)
    object.Bind(event_binder, lambda event: app.OnEvent(event, object, event_binder.typeId), id=id, id2=id2)

async def AsyncShowDialog(dlg):
    closed = Event()

    def end_dialog(return_code):
        dlg.SetReturnCode(return_code)
        dlg.Hide()
        closed.set()

    async def on_button(event):
        # Same code as in wxwidgets:/src/common/dlgcmn.cpp:OnButton
        # to automatically handle OK, CANCEL, APPLY,... buttons
        id = event.GetId()
        if id == dlg.GetAffirmativeId():
            if dlg.Validate() and dlg.TransferDataFromWindow():
                end_dialog(id)
        elif id == wx.ID_APPLY:
            if dlg.Validate():
                dlg.TransferDataFromWindow()
        elif id == dlg.GetEscapeId() or (id == wx.ID_CANCEL and dlg.GetEscapeId() == wx.ID_ANY):
            end_dialog(wx.ID_CANCEL)
        else:
            event.Skip()

    async def on_close(event):
        closed.set()
        dlg.Hide()

    AsyncBind(wx.EVT_CLOSE, on_close, dlg)
    AsyncBind(wx.EVT_BUTTON, on_button, dlg)
    dlg.Show()
    await closed.wait()
    return dlg.GetReturnCode()
