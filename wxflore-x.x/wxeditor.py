import wx
import os
import codecs
import re

ID_ABOUT=101
ID_OPEN=102
ID_SAVE=103
ID_BUTTON1=300
ID_EXIT=200

#class MainWindow(wx.Frame):

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MainWindow(wx.Dialog):
    def __init__(self,parent,title,filename,colors):

        self.filename=filename

        wx.Dialog.__init__(self, None, title=title)

        #wx.Frame.__init__(self,parent,wx.ID_ANY, title)

        self.TC = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE, size=(700, 500))
        self.TC.SetBackgroundColour(colors.normal[1])
        self.TC.SetForegroundColour(colors.normal[0])
        #self.CreateStatusBar()

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons=[]

        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.TC,1,wx.EXPAND)
        self.sizer.Add(self.sizer2,0,wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.Show(1)

        if os.path.exists(self.filename):
            self.TC.LoadFile(self.filename)

#        f = codecs.open(self.filename, "r", "utf-8")
#        self.TC.WriteText("".join(f.readlines()))

    def onCloseWindow(self,event):
        print("onCloseWindow")
        #        f = codecs.open(self.filename, "w", "utf-8")
        #        self.TC.WriteText("".join(f.readlines()))
        text = self.TC.GetValue()

        text_is_empty = 1
        for line in text:
            if not re.match("\s*$",line):
                text_is_empty = 0


        if text_is_empty:
            if os.path.exists(self.filename):
                print("## WARNING ## : Removing 'empty Note' file = {}".format(self.filename))
                os.remove(self.filename)
        else:
            self.TC.SaveFile(self.filename)

        event.Skip()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # Set up a window based app, and create a main window in it
    app = wx.PySimpleApp()
    view = MainWindow(None, "Sample editor")
    # Enter event loop
    app.MainLoop()
