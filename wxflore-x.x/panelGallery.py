#!/usr/bin/env python2

import os
import re
import wx
import functools

#import bota
#import mkthumb


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#class Panel(wx.lib.scrolledpanel.ScrolledPanel):
class Panel(wx.Panel):

    #-------------------------------------------------------------------------------
    def __init__(self,parent,pictList,options):

        self.options = options
        self.parent = parent

        wx.Panel.__init__(self,parent,size=(-1,-1))

        gridSizer =  wx.GridSizer(rows=4, cols=4, hgap=5, vgap=5)
        for i in range(0, len(pictList)):
            img = wx.Image(pictList[i][0], wx.BITMAP_TYPE_ANY)
            bmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
            text = wx.StaticText(self, -1, pictList[i][1])

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(bmp,0,wx.CENTER,0)
            sizer.Add(text,0,wx.CENTER,0)

            gridSizer.Add(sizer, 0, wx.ALIGN_CENTER, 8)

#        mainSizer = wx.BoxSizer(wx.VERTICAL)
#        rowSizer = wx.BoxSizer(wx.HORIZONTAL)
#
#        for i in range(0, len(pictList)):
#            img = wx.Image(pictList[i][0], wx.BITMAP_TYPE_ANY)
#            bmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
#
#            rowSizer.Add(bmp, 0, wx.ALL|wx.EXPAND, 8)
#            if i % 4 == 0:
#                mainSizer.Add(rowSizer,0,wx.ALL,8)
#
#        if i % 4 != 0:
#            mainSizer.Add(rowSizer,0,wx.ALL,8)
#
        self.SetSizer(gridSizer)


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class ViewerFrame(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, parent, pictList, options):

        wx.Frame.__init__(self, parent, title="Image Viewer", size=(1000,800))
        #self.SetBackgroundColour("#004000")
        self.options = options

        panel = Panel(self,pictList,options)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Show()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    class options:
        pass

    app = wx.App(redirect=False)
    ViewerFrame(None, [["/tmp/toto.png","a"],
                       ["/tmp/toto.png","b"],
                       ["/tmp/toto.png","c"],
                       ["/tmp/toto.png","d"],
                       ["/tmp/toto.png","e"],
                       ["/tmp/toto.png","f"],
                       ["/tmp/toto.png","g"],
                       ["/tmp/toto.png","h"],
                       ["/tmp/toto.png","i"],
                       ["/tmp/toto.png","j"],
                       ["/tmp/toto.png","k"],
                       ["/tmp/toto.png","l"],
                       ["/tmp/toto.png","m"],
                       ["/tmp/toto.png","n"]],
                options)
    app.MainLoop()

    self.Show()
