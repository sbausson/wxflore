#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import wx
import wx.richtext
import sys

s= u"Hello, This is a test .... \néèàï"
#s2 = "Hello éèàç\n{}\n{}".format(sys.version,wx.__version__)

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(350,200))

        sizer=wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(self, -1, s)
        sizer.Add(text,1,wx.ALL,10)
        
        text = wx.StaticText(self, -1, "Python version: {}\nwxPython version: {}".format(sys.version,wx.__version__))
        sizer.Add(text,1,wx.ALL,10)

#        self.headerRTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
#        self.headerRTC.WriteText("{}".format(s1.encode("utf8")).decode("utf8")) #.decode("utf8"))
#
#        #self.Add(self.headerRTC,1,wx.EXPAND)
#        sizer.Add(self.headerRTC,1,wx.EXPAND)
#
        self.SetSizer(sizer)
        self.Layout()
        self.Show()

app = wx.App(redirect=False)
Frame("Hello World")
app.MainLoop()
