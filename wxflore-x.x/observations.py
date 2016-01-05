#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import wx
import wx.grid
import wx.calendar

class colors:

    cells = ['#2eb8b8','#101010']
    names = ['#bbff33','#101010']
    labels = ['#bbff33','#303030']

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MainApp(wx.Frame):

    #-------------------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, title="Observations", size=(850, 500))
        self.SetBackgroundColour("#202020")

        self.colors = colors()
        self.grid = wx.grid.Grid(self,-1)

        self.grid.SetDefaultCellBackgroundColour(self.colors.cells[1])
        self.grid.SetDefaultCellTextColour(self.colors.cells[0])
        self.grid.SetLabelBackgroundColour(self.colors.labels[1])
        self.grid.SetLabelTextColour(self.colors.labels[0])

        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.onSelect)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE,self.onSelect)
        self.grid.CreateGrid(6,6)
        self.grid.SetColLabelValue(0,"Date")
        self.grid.SetColLabelValue(1,"Departement")
        self.grid.SetColLabelValue(2,"Commune (CP)")
        self.grid.SetColLabelValue(3,"Coord. GPS")
        self.grid.SetColLabelValue(4,"Densité")
        self.grid.SetColLabelValue(5,"Commentaire")
        self.grid.AutoSizeColumns()

        gridSizer = wx.GridSizer(7,2,6,0)

        st = wx.StaticText(self, -1, 'Date')
        st.SetForegroundColour(self.colors.names[0])
        self.dateInput = wx.TextCtrl(self, -1)
        self.dateInput.SetBackgroundColour(self.colors.cells[1])
        self.dateInput.SetForegroundColour(self.colors.cells[0])
        self.dateInput.Bind(wx.EVT_KEY_UP, self.checkValid)
        self.dateInput.Bind(wx.EVT_LEFT_DCLICK,self.onCalendar)
        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.dateInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)

        st = wx.StaticText(self, -1, 'Departement')
        st.SetForegroundColour(self.colors.names[0])
        self.firstInput = wx.TextCtrl(self, -1)
        self.firstInput.SetBackgroundColour(self.colors.cells[1])
        self.firstInput.SetForegroundColour(self.colors.cells[0])
        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)

        st = wx.StaticText(self, -1, 'Commune (CP)')
        st.SetForegroundColour(self.colors.names[0])
        self.firstInput = wx.TextCtrl(self, -1)
        self.firstInput.SetBackgroundColour(self.colors.cells[1])
        self.firstInput.SetForegroundColour(self.colors.cells[0])
        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)

        st = wx.StaticText(self, -1, 'Coord. GPS')
        st.SetForegroundColour(self.colors.names[0])
        self.firstInput = wx.TextCtrl(self, -1)
        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
        self.firstInput.SetBackgroundColour(self.colors.cells[1])
        self.firstInput.SetForegroundColour(self.colors.cells[0])
        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)

        st = wx.StaticText(self, -1, 'Densité')
        st.SetForegroundColour(self.colors.names[0])
        self.firstInput = wx.TextCtrl(self, -1)
        self.firstInput.SetBackgroundColour(self.colors.cells[1])
        self.firstInput.SetForegroundColour(self.colors.cells[0])
        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)

        st = wx.StaticText(self, -1, 'Commentaire')
        st.SetForegroundColour(self.colors.names[0])
        self.firstInput = wx.TextCtrl(self, size=(200,-1))
        self.firstInput.SetBackgroundColour(self.colors.cells[1])
        self.firstInput.SetForegroundColour(self.colors.cells[0])
        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.calendar = wx.calendar.CalendarCtrl(self, -1, wx.DateTime_Now())
        self.calendar.Bind(wx.calendar.EVT_CALENDAR, self.onCalendarSelect)
        self.calendar.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.onCalendarSelect)

        sizerButton = wx.BoxSizer(wx.HORIZONTAL)

        self.button_add = wx.Button(self, label='Add to List')
        self.Bind(wx.EVT_BUTTON,self.onButtonAddToList,self.button_add)
        self.button_add.SetBackgroundColour("#2594FD")
        self.button_add.SetForegroundColour("#ffffff")
        sizerButton.Add(self.button_add,0,wx.ALL)

        self.button_done = wx.Button(self, label='Done')
        self.Bind(wx.EVT_BUTTON,self.onButtonDone,self.button_done)
        self.button_done.SetBackgroundColour("#ccff33")
        self.button_done.SetForegroundColour("#303030")
        sizerButton.Add(self.button_done,0,wx.ALL)

        sizer2.Add(gridSizer,0,wx.ALL,10)
        sizer2.Add(self.calendar,0,wx.ALL,10)

        sizer1.Add(self.grid,0,wx.ALL,10)
        sizer1.Add(sizer2,0,wx.ALL,10)
        #sizer2.Add(vsizer,0,wx.ALL,10)

        sizer1.Add(sizerButton,0,wx.ALL,10)

        self.SetSizer(sizer1)
        self.Show()

    #-------------------------------------------------------------------------------
    def onButtonAddToList(self,evt):
        print("onButtonAddToList")

    #-------------------------------------------------------------------------------
    def onButtonDone(self,evt):
        print("onButtonDone")

    #-------------------------------------------------------------------------------
    def onCalendar(self,evt):
        print("onCalendar")
        self.cal = wx.calendar.CalendarCtrl(self, -1, wx.DateTime_Now())

    #-------------------------------------------------------------------------------
    def onCalendarSelect(self,evt):
        print("onCalendarSelect")
        y = evt.GetDate().GetYear()
        m = evt.GetDate().GetMonth()+1
        d = evt.GetDate().GetDay()
        date = "{:4}.{:02}.{:02}".format(y,m,d)
        self.dateInput.Clear()
        self.dateInput.AppendText(date)



    #-------------------------------------------------------------------------------
    def onSelect(self,evt):
        print("onSelect")

    #-------------------------------------------------------------------------------
    def checkValid(self,evt):
        print("checkValid")

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
app = wx.App(redirect=False)
MainApp()
app.MainLoop()


self.Show()
