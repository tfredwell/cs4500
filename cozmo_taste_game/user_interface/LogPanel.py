# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.3 on Mon Dec  3 11:51:41 2018
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class LogPanel(wx.ScrolledWindow):
				def __init__(self, *args, **kwds):
								# begin wxGlade: LogPanel.__init__
								kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
								wx.ScrolledWindow.__init__(self, *args, **kwds)

								self.__set_properties()
								self.__do_layout()
								# end wxGlade

				def __set_properties(self):
								# begin wxGlade: LogPanel.__set_properties
								self.SetScrollRate(10, 10)
								# end wxGlade

				def __do_layout(self):
								# begin wxGlade: LogPanel.__do_layout
								self.Layout()
								# end wxGlade

# end of class LogPanel
