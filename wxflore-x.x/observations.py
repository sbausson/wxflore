#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import wx
import wx.grid
import wx.calendar
import csv
import wx.lib.newevent
import codecs

from common import *

class colors:

    cells = ['#2eb8b8','#101010']
    calendar_main = ['#2eb8b8','#101010']
    calendar_head = ['#bbff33','#308830']

    grid_lines = '#303030'
    names = ['#bbff33','#101010']
    #labels = ['#bbff33','#303030']
    labels = ['#bbff33','#101010']

col_label_size = {u'Date':80,
                  u'Dept.':60,
                  u'Commune':140,
                  u'Coord. GPS':100,
                  u'Densité':100,
                  u'Commentaire':500}

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Observations():

    #-------------------------------------------------------------------------------
    def __init__(self,parent,filename):

        self.parent = parent
        self.labels = []
        self.table = []
        self.filename = filename

        if os.path.exists(self.filename):

            with open(self.filename, 'rb') as f:
                csvreader = csv.reader(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                i = 0
                for row in csvreader:
                    row = [s.decode('utf-8') for s in row]
                    if i == 0:
                        self.labels = row
                    else:
                        self.table.append(row)
                    i+=1
        else:
            self.labels = [u'Date',u'Dept.',u'Commune',u'Coord. GPS',u'Densité',u'Commentaire']
            self.table = [['','','','','','']]

        print(self.labels)

    #-------------------------------------------------------------------------------
    def write(self,table):

        if len(table) == 1:
            if False not in [x == '' for x in table[0]]:
                print("## WARNING ## : Empty Oberservation, saving nothing ...")
                return

        with open(self.filename, 'wb') as f:
            print("Saving {} ...".format(self.filename))
            csvwriter = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow([s.encode('utf-8') for s in self.labels])
            for row in table:
                csvwriter.writerow([s.encode('utf-8') for s in row])

        nevent = ObsUpdateEvent()
        wx.PostEvent(self.parent,nevent)

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
class ObsPanel(wx.Panel):

    #-------------------------------------------------------------------------------
    def __init__(self,parent,struct, filename, obs_button):

        wx.Panel.__init__(self, parent) #size=(950, 550))

        self.SetBackgroundColour("#101010")
        self.colors = colors()

        self.Obs = Observations(parent,filename)

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


        self.edit = True
        self.grid.EnableEditing(0)

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

        mainSizer = wx.BoxSizer(wx.VERTICAL)


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
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.button_edit = wx.Button(self, label='Edit')
        self.Bind(wx.EVT_BUTTON,self.onButtonEdit,self.button_edit)
        self.button_edit.SetBackgroundColour("#d0d0d0")
        self.button_edit.SetForegroundColour("#00264d")
        self.buttonSizer.Add(self.button_edit,0,wx.ALL)

        self.button_new = wx.Button(self, label='New Observation')
        self.Bind(wx.EVT_BUTTON,self.onButtonNew,self.button_new)
        self.button_new.SetBackgroundColour("#2594FD")
        self.button_new.SetForegroundColour("#ffffff")
        self.buttonSizer.Add(self.button_new,0,wx.ALL)
        self.button_new.Hide()

        self.button_done = wx.Button(self, label='Done')
        self.Bind(wx.EVT_BUTTON,self.onButtonDone,self.button_done)
        self.button_done.SetBackgroundColour("#ccff33")
        self.button_done.SetForegroundColour("#303030")
        self.buttonSizer.Add(self.button_done,0,wx.ALL)
        self.button_done.Hide()

        self.button_debug = wx.Button(self, label='Debug')
        self.Bind(wx.EVT_BUTTON,self.onButtonDebug,self.button_debug)
        self.button_debug.SetBackgroundColour("#000033")
        self.button_debug.SetForegroundColour("#303030")
        self.buttonSizer.Add(self.button_debug,0,wx.ALL)
        self.button_debug.Hide()

        self.calendarSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.calendarSizer.Add((10,10))
        self.calendarSizer.Add(self.calendar,0,wx.ALL,10) #|wx.RESERVE_SPACE_EVEN_IF_HIDDEN,10)

        #------------------------------------------------
        mainSizer.Add(self.grid,1,wx.ALL|wx.EXPAND,10)
        mainSizer.Add(self.calendarSizer,0,wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN,10)
        mainSizer.Add(self.buttonSizer,0,wx.ALL,10)

        self.SetSizer(mainSizer)
        self.calendarSizer.Hide(1)
        self.Show()

    #-------------------------------------------------------------------------------
    def onButtonEdit(self,evt):
        print("onButtonEdit")
        self.button_new.Show()
        self.button_done.Show()
        #self.button_debug.Show()
        self.button_edit.Hide()

        self.edit = True
        self.grid.EnableEditing(1)

        self.Layout()

    #-------------------------------------------------------------------------------
    def onButtonNew(self,evt):
        print("onButtonNew")
        self.grid.AppendRows(1)
        self.Layout()

#        s = self.dateInput.GetLineText(0)
#        print(s)
#        self.grid.SetCellValue(self.grid_index,0,s)

    #-------------------------------------------------------------------------------
    def onButtonDone(self,evt):
        print("onButtonDone")

        table = []
        for i in range(0,self.grid.GetNumberRows()):
            row = []
            for j in range(0,self.grid.GetNumberCols()):
                print(type(self.grid.GetCellValue(i,j)))
                row.append(self.grid.GetCellValue(i,j))
            table.append(row)

        self.Obs.write(table)

        self.button_new.Hide()
        self.button_done.Hide()
        #self.button_debug.Hide()
        self.button_edit.Show()

        self.grid.EnableEditing(0)
        self.edit = 0

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
class ObsFrame(wx.Frame):

    #-------------------------------------------------------------------------------
    def __init__(self):

        #filename = 'observations.csv'
        filename = '/home/git/wxflore-meta/obs/Acanthus.mollis.csv'

        wx.Frame.__init__(self, None, title="Observations", size=(950, 550))
        self.SetBackgroundColour("#101010")
        ObsPanel(self, {}, filename, None)
        self.Show()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    app = wx.App(redirect=False)
    ObsFrame()
    app.MainLoop()
