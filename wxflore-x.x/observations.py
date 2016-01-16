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

col_label_size = {"Date":80,
                  "Dept.":60,
                  "Commune":140,
                  "Coord. GPS":100,
                  "Densité":100,
                  "Commentaire":350}


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Observations():

    #-------------------------------------------------------------------------------
    def __init__(self,filename):

        self.labels = []
        self.table = []
        self.filename = filename

        with open(self.filename, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            i = 0
            for row in csvreader:
                if i == 0:
                    self.labels = row
                else:
                    self.table.append(row)
                i+=1

    #-------------------------------------------------------------------------------
    def write(self,table):

        with open(self.filename, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(self.labels)
            for row in table:
                csvwriter.writerow(row)

    #-------------------------------------------------------------------------------
    def __repr__(self):
        s=""
        fmt="{:12} {:8} {:20} {:15} {:15} {:40}\n"
        s+=fmt.format(*self.labels)
        s+="-"*100+"\n"
        for row in self.obs:
            s+=fmt.format(*row)
        return(s)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MainApp(wx.Frame):

    #-------------------------------------------------------------------------------
    def __init__(self):

        wx.Frame.__init__(self, None, title="Observations", size=(950, 550))
        self.SetBackgroundColour("#202020")
        self.colors = colors()

        self.Obs = Observations('observations.csv')

        # Grid
        #--------------------------------
        self.grid = wx.grid.Grid(self,-1)

        self.grid.SetDefaultCellBackgroundColour(self.colors.cells[1])
        self.grid.SetDefaultCellTextColour(self.colors.cells[0])
        self.grid.SetLabelBackgroundColour(self.colors.labels[1])
        self.grid.SetLabelTextColour(self.colors.labels[0])
        self.grid.SetGridLineColour(self.colors.grid_lines)

        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.onSelect)
        #self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE,self.onSelect)
        #self.grid.Bind(wx.EVT_KILL_FOCUS,self.onFocusLost)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.onLeftDClick)
        self.grid.CreateGrid(len(self.Obs.table),len(self.Obs.table[0]))


        self.grid.SetCellHighlightColour('#94b8b8')
        #self.grid_col_list = ['Date','Dept.','Commune (CP)','Coord. GPS','Densité','Commentaire']

        for i in range(0,len(self.Obs.labels)):
            self.grid.SetColLabelValue(i,self.Obs.labels[i])
            self.grid.SetColSize(i,col_label_size[self.Obs.labels[i]])


        for row in range(0,len(self.Obs.table)):
            for col in range(0,len(self.Obs.table[row])):
                self.grid.SetCellValue(row,col,self.Obs.table[row][col])


        self.grid_index = 0

        #gridSizer = wx.GridSizer(7,2,6,0)

#        st = wx.StaticText(self, -1, 'Date')
#        st.SetForegroundColour(self.colors.names[0])
#        self.dateInput = wx.TextCtrl(self, -1)
#        self.dateInput.SetBackgroundColour(self.colors.cells[1])
#        self.dateInput.SetForegroundColour(self.colors.cells[0])
#        self.dateInput.Bind(wx.EVT_KEY_UP, self.checkValid)
#        #self.dateInput.Bind(wx.EVT_LEFT_DCLICK,self.onCalendar)
#        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
#        gridSizer.Add(self.dateInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
#
#        st = wx.StaticText(self, -1, 'Departement')
#        st.SetForegroundColour(self.colors.names[0])
#        self.firstInput = wx.TextCtrl(self, -1)
#        self.firstInput.SetBackgroundColour(self.colors.cells[1])
#        self.firstInput.SetForegroundColour(self.colors.cells[0])
#        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
#        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
#        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
#
#        st = wx.StaticText(self, -1, 'Commune (CP)')
#        st.SetForegroundColour(self.colors.names[0])
#        self.firstInput = wx.TextCtrl(self, -1)
#        self.firstInput.SetBackgroundColour(self.colors.cells[1])
#        self.firstInput.SetForegroundColour(self.colors.cells[0])
#        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
#        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
#        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
#
#        st = wx.StaticText(self, -1, 'Coord. GPS')
#        st.SetForegroundColour(self.colors.names[0])
#        self.firstInput = wx.TextCtrl(self, -1)
#        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
#        self.firstInput.SetBackgroundColour(self.colors.cells[1])
#        self.firstInput.SetForegroundColour(self.colors.cells[0])
#        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
#        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
#
#        st = wx.StaticText(self, -1, 'Densité')
#        st.SetForegroundColour(self.colors.names[0])
#        self.firstInput = wx.TextCtrl(self, -1)
#        self.firstInput.SetBackgroundColour(self.colors.cells[1])
#        self.firstInput.SetForegroundColour(self.colors.cells[0])
#        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
#        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
#        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
#
#        st = wx.StaticText(self, -1, 'Commentaire')
#        st.SetForegroundColour(self.colors.names[0])
#        self.firstInput = wx.TextCtrl(self, size=(200,-1))
#        self.firstInput.SetBackgroundColour(self.colors.cells[1])
#        self.firstInput.SetForegroundColour(self.colors.cells[0])
#        self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
#        gridSizer.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
#        gridSizer.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)

        sizer1 = wx.BoxSizer(wx.VERTICAL)


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
        #self.calendar.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.onCalendarSelect)
        self.calendar.Bind(wx.EVT_KILL_FOCUS,self.onCalendarFocusLost)

        self.calendar.SetDate(wx.DateTime_Now())
        self.calendar.SetFocus()
        #print(dir(self.calendar))

        # Buttons
        #--------------------------------------------------------------------
        sizerButton = wx.BoxSizer(wx.HORIZONTAL)

        self.button_add = wx.Button(self, label='New Observation')
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

        self.calendarSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.calendarSizer.Add((10,10))
        self.calendarSizer.Add(self.calendar,0,wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN,10)

        # calendarSizer
        #------------------------------------------------
        sizer1.Add(self.grid,0,wx.ALL,10)
        sizer1.Add(self.calendarSizer,0,wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN,10)
        self.calendarSizer.Hide(1)

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

        table = []
        for i in range(0,self.grid.GetNumberRows()):
            row = []
            for j in range(0,self.grid.GetNumberCols()):
                row.append(self.grid.GetCellValue(i,j))
            table.append(row)

        self.Obs.write(table)
        self.Destroy()

    #-------------------------------------------------------------------------------
    def onButtonDebug(self,evt):
        print("onButtonDebug")
        print("IsSelection",self.grid.IsSelection())
        print("GetSelectedCells",self.grid.GetSelectedCells())

    #-------------------------------------------------------------------------------
    def onCalendarFocusLost(self,evt):
        print("onCalendarFocusLost")
        self.calendarSizer.Hide(1)
        self.Layout()

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
        print(date)
        self.calendarSizer.Hide(1)
        self.Layout()
        self.grid.SetCellValue(self.date_edit_row,0,date)

    #-------------------------------------------------------------------------------
    def onSelect(self,evt):
        print("onSelect")
        #self.last_select = (evt.GetRow(),evt.GetCol())
        #print(self.last_select)

    #-------------------------------------------------------------------------------
    def onLeftDClick(self,evt):
        print("onLeftDClick")

        if evt.GetCol() == 0:
            self.date_edit_row = evt.GetRow()
            self.calendarSizer.Show(1)
            self.calendar.SetFocus()
            self.Layout()
        else:
            self.date_edit_row = -1

    #-------------------------------------------------------------------------------
    def onFocusLost(self,evt):
        print("onLostFocus")
        self.last_select = (-1,-1)
        print(self.last_select)

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
