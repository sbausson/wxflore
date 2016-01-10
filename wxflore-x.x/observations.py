#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import wx
import wx.grid
import wx.calendar
import csv

class colors:

    cells = ['#2eb8b8','#101010']
    calendar_main = ['#2eb8b8','#101010']
    calendar_head = ['#bbff33','#308830']

    grid_lines = '#303030'
    names = ['#bbff33','#101010']
    labels = ['#bbff33','#303030']

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MainApp(wx.Frame):

    #-------------------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, title="Observations", size=(950, 550))
        self.SetBackgroundColour("#202020")

        self.colors = colors()

        # Grid
        #--------------------------------
        self.grid = wx.grid.Grid(self,-1)

        self.grid.SetDefaultCellBackgroundColour(self.colors.cells[1])
        self.grid.SetDefaultCellTextColour(self.colors.cells[0])
        self.grid.SetLabelBackgroundColour(self.colors.labels[1])
        self.grid.SetLabelTextColour(self.colors.labels[0])
        self.grid.SetGridLineColour(self.colors.grid_lines)

        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.onSelect)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE,self.onSelect)
        self.grid.CreateGrid(1,6)

        self.grid_col_list = ['Date','Dept.','Commune (CP)','Coord. GPS','Densité','Commentaire']

        self.grid.SetColLabelValue(0,"Date")
        self.grid.SetColSize(0,80)

        self.grid.SetColLabelValue(1,"Dept.")
        self.grid.SetColSize(1,60)

        self.grid.SetColLabelValue(2,"Commune")
        self.grid.SetColSize(2,140)

        self.grid.SetColLabelValue(3,"Coord. GPS")
        self.grid.SetColSize(3,100)

        self.grid.SetColLabelValue(4,"Densité")
        self.grid.SetColSize(4,100)

        self.grid.SetColLabelValue(5,"Commentaire")
        self.grid.SetColSize(5,350)

        #self.grid.AutoSizeColumns()

        self.grid_index = 0

        gridSizer = wx.GridSizer(7,2,6,0)

        st = wx.StaticText(self, -1, 'Date')
        st.SetForegroundColour(self.colors.names[0])
        self.dateInput = wx.TextCtrl(self, -1)
        self.dateInput.SetBackgroundColour(self.colors.cells[1])
        self.dateInput.SetForegroundColour(self.colors.cells[0])
        self.dateInput.Bind(wx.EVT_KEY_UP, self.checkValid)
        #self.dateInput.Bind(wx.EVT_LEFT_DCLICK,self.onCalendar)
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


        # Calendar
        #--------------------------------------------------------------------
        self.calendar = wx.calendar.CalendarCtrl(self,
                                                 -1,
                                                 wx.DateTime_Now(),
                                                 style=wx.calendar.CAL_MONDAY_FIRST)

        self.calendar.SetForegroundColour(self.colors.calendar_main[0])
        self.calendar.SetBackgroundColour(self.colors.calendar_main[1])
        self.calendar.SetHeaderColours(self.colors.calendar_head[0],self.colors.calendar_head[1])
        self.calendar.SetHighlightColours('#550000','#FF00FF')
        #self.calendar.SetOwnBackgroundColour('#000088')

        self.calendar.Bind(wx.calendar.EVT_CALENDAR, self.onCalendarSelect)
        self.calendar.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.onCalendarSelect)
        self.calendar.SetDate(wx.DateTime_Now())
        #print(dir(self.calendar))

        # Buttons
        #--------------------------------------------------------------------
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

        self.button_debug = wx.Button(self, label='Debug')
        self.Bind(wx.EVT_BUTTON,self.onButtonDebug,self.button_debug)
        self.button_debug.SetBackgroundColour("#000033")
        self.button_debug.SetForegroundColour("#303030")
        sizerButton.Add(self.button_debug,0,wx.ALL)

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
        self.grid.AppendRows(1)
        self.Layout()

#        s = self.dateInput.GetLineText(0)
#        print(s)
#        self.grid.SetCellValue(self.grid_index,0,s)
        self.grid_index += 1

    #-------------------------------------------------------------------------------
    def onButtonDone(self,evt):
        print("onButtonDone")

        with open('observation.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile,
                                    delimiter=';',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)


            csvwriter.writerow(self.grid_col_list)
            for i in range(0,self.grid.GetNumberRows()):
                row = []
                for j in range(0,self.grid.GetNumberCols()):
                    row.append(self.grid.GetCellValue(i,j))
                print(row)
                csvwriter.writerow(row)

        self.Destroy()

    #-------------------------------------------------------------------------------
    def onButtonDebug(self,evt):
        print("onButtonDebug")
        print("IsSelection",self.grid.IsSelection())
        print("GetSelectedCells",self.grid.GetSelectedCells())

    #-------------------------------------------------------------------------------
    def onCalendar(self,evt):
        print("onCalendar")
        self.cal = wx.calendar.CalendarCtrl(self, -1, wx.DateTime_Now())
        #self.cal.SetHeaderColours('#005500')
        #self.cal.SetHighlightColours('#550000')

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
        print(evt.GetRow(),evt.GetCol())

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
