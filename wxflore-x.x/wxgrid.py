import os
import wx
import wx.grid
import bota
from common import *

#class colors:
#    selected = ["#cc3399","#99ff33"]
#    normal = ["#000000","#ffffff"]
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class TextFrame(wx.Frame):

    def __init__(self, text, panel, title=None,size=None):
        wx.Frame.__init__(self, None,size=(1400,700))
        style = wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY #|wx.TE_RICH2
        txt = wx.TextCtrl(self, -1,
                          pos=(10, 270),
                          style=style)# ,size=(800,500))

        txt.SetBackgroundColour(panel.colors.normal[1])
        #txt.SetForegroundColour(panel.colors.normal[0])
        txt.SetForegroundColour("#f0f0f0")

        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Liberation Mono')

        txt.SetFont(font)
        if title != None:
            self.SetTitle(title)
        if size != None:
            self.SetSize(size)

        txt.AppendText(text+"\n")
        self.Show()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class HugeGrid(wx.grid.PyGridTableBase):

    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = [""]*len(self.data)
        self.colLabels = [""]*len(self.data[0])
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()

    #-------------------------------------------------------------------------------
    def GetNumberRows(self):
        return len(self.data)

    #-------------------------------------------------------------------------------
    def GetNumberCols(self):
        return len(self.data[0])

    #-------------------------------------------------------------------------------
    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]

    #-------------------------------------------------------------------------------
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]

    #-------------------------------------------------------------------------------
    def SetColLabelValue(self, col, labels):
        self.colLabels[col] = labels

    #-------------------------------------------------------------------------------
    def SetRowLabelValue(self, row, labels):
        self.rowLabels[row] = labels

    #-------------------------------------------------------------------------------
    def IsEmptyCell(self, row, col):
        return False

    #-------------------------------------------------------------------------------
    def GetValue(self, row, col):
        return self.data[row][col]

    #-------------------------------------------------------------------------------
    def _SetRowAttr(self, row, attr):
        print "SetRowAttr"
        self.SetRowAttr(row, attr)

    #-------------------------------------------------------------------------------
    def SetValue(self, row, col, value):
        pass

    #-------------------------------------------------------------------------------
    def ResetView(self, grid):
 	"""
 	(Grid) -> Reset the grid view. Call this to
 	update the grid if rows and columns have been added or deleted
 	"""
 	grid.BeginBatch()

 	for current, new, delmsg, addmsg in [
                (self._rows, self.GetNumberRows(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
                (self._cols, self.GetNumberCols(), wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
 	]:

            if new < current:
                msg = wx.grid.GridTableMessage(self,delmsg,new,current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = wx.grid.GridTableMessage(self,addmsg,new-current)
                grid.ProcessTableMessage(msg)
                self.UpdateValues(grid)

 	grid.EndBatch()

 	self._rows = self.GetNumberRows()
 	self._cols = self.GetNumberCols()
 	# update the column rendering plugins
# 	self._updateColAttrs(grid)

 	# update the scrollbars and the displayed part of the grid
 	grid.AdjustScrollbars()
 	grid.ForceRefresh()


    #-------------------------------------------------------------------------------
    def UpdateValues(self, grid):
 	"""Update all displayed values"""
 	# This sends an event to the grid table to update all of the values
 	msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
 	grid.ProcessTableMessage(msg)

    #-------------------------------------------------------------------------------
    def SetData(self, data):
        print("SetData")
        self.data = data

#        self.rowLabels = [""]*len(data)
#        self.colLabels = [""]*len(self.data[0])
#
#    def ResetView(self, grid):
#        """
#        (Grid) -> Reset the grid view.   Call this to
#        update the grid if rows and columns have been added or deleted
#        """
#        grid.BeginBatch()
#
#        for current, new, delmsg, addmsg in [
#            (self._rows, self.GetNumberRows(), Grid.GRIDTABLE_NOTIFY_ROWS_DELETED, Grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
#            (self._cols, self.GetNumberCols(), Grid.GRIDTABLE_NOTIFY_COLS_DELETED, Grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
#        ]:
#
#            if new < current:
#                msg = Grid.GridTableMessage(self,delmsg,new,current-new)
#                grid.ProcessTableMessage(msg)
#            elif new > current:
#                msg = Grid.GridTableMessage(self,addmsg,new-current)
#                grid.ProcessTableMessage(msg)
#                self.UpdateValues(grid)
#
#        grid.EndBatch()
#
#        self._rows = self.GetNumberRows()
#        self._cols = self.GetNumberCols()
#        # update the column rendering plugins
#        self._updateColAttrs(grid)
#
#        # update the scrollbars and the displayed part of the grid
#        grid.AdjustScrollbars()
#        grid.ForceRefresh()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class filteredGrid(wx.grid.Grid):

    def __init__(self, parent, panel, struct_list, index, attrib_list):

        print("wxgrid.py : filteredGrid.__init__ / start ...")

        #self.title = panel.title
        self.options = panel.options
        self.panel = panel
        self.struct_list = struct_list
        self.index = index
        self.attrib_list = attrib_list

        # This was wrong ! wx.grid.Grid.__init__(self, panel, -1)
        wx.grid.Grid.__init__(self, parent, -1)
        self.Fill()

        #self.SetSelection(index)

        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,  self.OnMouse_LeftClick)
        #self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnSelectCell, self)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.RightClick)
        self.Bind(wx.EVT_KEY_DOWN,                   self.onKey)

#        self.Refresh()

        print("wxgrid.py : Vgrid.__init__ / done ...")

    #-------------------------------------------------------------------------------
    def Fill(self):

        print("filteredGrid.Fill()")

        self.data_t = []
        self.grid_data_t = []
        self.color_t = []
        self.bg_t = []

        i=0
        for struct in self.struct_list:
            mark = ""
            first = 1
            for k in range(0,len(self.panel.apps.marker_table)):
                if struct["NL"] in self.panel.apps.marker_table[k]:
                    if first:
                        first = 0
                        mark = "m"
                    mark += "{}".format(k+1)
                    #break

            if i < len(self.attrib_list) and self.attrib_list[i] != "":
                bg = self.attrib_list[i]
            else:
                bg = ""


            if mark == "":
                color = self.panel.colors.normal[0]
            else:
                color = "#ff9933"

            self.color_t.append(color)
            self.bg_t.append(bg)

            name_reduced = bota.ReduceName(struct["NL"])
            if os.path.exists(os.path.join(self.options.paths.img,"photos",name_reduced)):
                if os.path.exists(os.path.join(self.options.paths.img,"photos",name_reduced,"{}.00.jpg".format(name_reduced))):
                    photo_pres = ""
                else:
                    photo_pres = "o"
            else:
                photo_pres = "X"

            row = [i+1,mark,struct["FA"],photo_pres,struct["NL"]]
            self.grid_data_t.append(row)

            self.data_t.append(struct["NL"])
            i+=1

        self.tableBase = HugeGrid(self.grid_data_t)
        self.SetTable(self.tableBase)

        self.SetDefaultCellBackgroundColour(self.panel.colors.normal[1])
        self.SetDefaultCellTextColour(self.panel.colors.normal[0])

        self.SetRowLabelSize(0)
        self.SetColLabelSize(25)
        self.SetColLabelAlignment(wx.ALIGN_LEFT,wx.ALIGN_LEFT)

        self.SetDefaultRowSize(18)
        self.EnableEditing(False)

        self.SetLabelBackgroundColour('#303030')
  	self.SetLabelTextColour('#73e600')

        self.SetColLabelValue(0,"No")
        self.SetColSize(0,40)

        self.SetColLabelValue(1,"Mk")
        self.SetColSize(1,30)

        self.SetColLabelValue(2,"Famille")
        self.SetColSize(2,150)

        self.SetColLabelValue(3,"X")
        self.SetColSize(3,15)

        self.SetColLabelValue(4,"Plante")
        self.SetColSize(4,400)


        for i in range(0,len(self.grid_data_t)):
            attr = wx.grid.GridCellAttr()
            attr.SetTextColour(self.color_t[i])
            if self.bg_t[i] != "":
                attr.SetBackgroundColour(self.bg_t[i])

            self.SetRowAttr(i, attr)

        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(self.panel.colors.selected[1])
        attr.SetTextColour(self.color_t[self.index])
        self.SetRowAttr(self.index, attr)

        colors_t = {"blanc":["white","black"],
                    "bleu":["blue","white"],
                    "rose":["pink","black"],
                    "vert":["green","black"],
                    "jaune":["yellow","black"],
        }


        for i in range(0,len(self.struct_list)):
            color = "none"
            try:
                #color = self.struct_list[i]["baseflor"]["FL.col"].split(",")[0].strip()
                color = self.struct_list[i]["FL.col"].split(",")[0].strip()
                self.SetCellBackgroundColour(i,3,colors_t[color][0])
                self.SetCellTextColour(i,3,colors_t[color][1])

                #print("COLOR SET")
            except:
                print("## WARNING ## color: {}".format(color))
                pass



        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        if font.SetFaceName("Liberation Mono"):
            print 'Set "Liberation Mono"'
            self.SetDefaultCellFont(font)
        else:
            font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.SetDefaultCellFont(font)

    #-------------------------------------------------------------------------------
    def onKey(self,event):
        code = event.GetKeyCode()
        print "onKey",code

        update=0
        if code == 315 and self.index > 0:
            row = self.index-1
            update=1
        elif code == 317 and self.index < (len(self.grid_data_t) - 1):
            row = self.index+1
            update=1

        if update:
            self.SetSelection(row)
            self.panel.Update(self.index)

            # // a
            self.SetGridCursor(row, 0)
            wx.CallAfter(self.MakeCellVisible, row, 0)

            # // a
            self.SetGridCursor(row, 0)
            self.MakeCellVisible(row, 0)

            self.SetFocus()
            print("filterdGrid.onkey SetFocus")

        # //a
        event.Skip()

    #-------------------------------------------------------------------------------
    def UpdateGrid(self,panel,grid_data_t,index):

        print("Upgrade Grid #{}".format(index))
        self.grid_data_t = grid_data_t

        self.tableBase.SetData(data)
        self.tableBase.ResetView(self)
        self.SetSelection(index)

    #-------------------------------------------------------------------------------
    def SetSelection(self,row):

        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(self.panel.colors.normal[1])
        #attr.SetTextColour(self.panel.colors.normal[0])
        attr.SetTextColour(self.color_t[self.index])
        self.SetRowAttr(self.index, attr)

        print("SetSelection OLD={}  NEW={}".format(self.index,row))
        self.index = row
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(self.panel.colors.selected[1])
        #attr.SetTextColour(self.panel.colors.selected[0])
        attr.SetTextColour(self.color_t[self.index]) #panel.colors.selected[0])
        self.SetRowAttr(self.index, attr)
        self.Refresh()


    #-------------------------------------------------------------------------------
    def OnMouse_LeftClick(self, evt):
    #def OnSelectCell(self, evt):

        print("wxgrid.py : Vgrid.OnMouse_LeftClick()")

        row = evt.Row
        state = wx.GetMouseState()
        print(evt.Row,self.grid_data_t[row])

        # Row selection
        if state.ControlDown():
            print("State Control+Down",self.panel.apps.marker_index)
            spe_name = self.data_t[row]

            if spe_name in self.panel.apps.marker_table[self.panel.apps.marker_index]:
                self.panel.apps.marker_table[self.panel.apps.marker_index].remove(spe_name)
            else:
                self.panel.apps.marker_table[self.panel.apps.marker_index].append(spe_name)

            self.Fill()
            print self.panel.apps.marker_table
        else:
            self.SetSelection(row)

        self.panel.Update(self.index)
        #evt.Skip()

    #-------------------------------------------------------------------------------
    def RightClick(self, event):
        print "OnRighClick"

        self.row = event.GetRow()
        self.popupCol = event.GetCol()
        menu = wx.Menu()

        self.popupID_FILTER_GENDER = wx.NewId()
        self.popupID_EXPORT_ID_TELA = wx.NewId()
        self.popupID_EXPORT_NL = wx.NewId()
        self.popupID_EXPORT_NL_NV = wx.NewId()
        self.popupID_EXPORT_FA_NL_NV = wx.NewId()
        self.popupID_UNSELECT_ALL = wx.NewId()
        self.popupID_PICT_GALLERY = wx.NewId()
        self.popupID_PICT_LIST = wx.NewId()

        self.popupID_TEST = wx.NewId()

        self.current_gender = self.data_t[self.row].split()[0]
        menu.Append(self.popupID_FILTER_GENDER, "Filter \"{}\"".format(self.current_gender))
        menu.AppendSeparator()
        menu.Append(self.popupID_EXPORT_ID_TELA, "Export list of Tela IDs")
        menu.Append(self.popupID_EXPORT_NL, "Export list of NL")
        menu.Append(self.popupID_EXPORT_NL_NV, "Export list of NL + NV")
        menu.Append(self.popupID_EXPORT_FA_NL_NV, "Export list of FA + NL + NV")
        menu.AppendSeparator()
        menu.Append(self.popupID_UNSELECT_ALL, "Unselect All")
        menu.AppendSeparator()
        menu.Append(self.popupID_PICT_GALLERY, "Display Gallery")
        menu.Append(self.popupID_PICT_LIST, "Not Implemented ...")
        menu.AppendSeparator()
        menu.Append(self.popupID_TEST, "to be done")


        self.Bind(wx.EVT_MENU, self.RightClickMenu)

        self.PopupMenu(menu)
        menu.Destroy()

    #-------------------------------------------------------------------------------
    def RightClickMenu(self,event):
        print("RightClickMenu")
        s = ""
        if event.GetId() == self.popupID_FILTER_GENDER:
            pass

        elif event.GetId() == self.popupID_EXPORT_ID_TELA:
            for struct in self.struct_list:
                s+="{}\n".format(struct["ID.tela"])

        elif event.GetId() == self.popupID_EXPORT_NL:
            for struct in self.struct_list:
                s+=u"{:60}\n".format(struct["NL"].replace("["," ").replace("]",""))

        elif event.GetId() == self.popupID_EXPORT_NL_NV:
            for struct in self.struct_list:
                s+=u"{:60}{:60}\n".format(struct["NL"].replace("["," ").replace("]",""),
                                          struct["NV"].replace(";",","))

        elif event.GetId() == self.popupID_EXPORT_FA_NL_NV:
            for struct in self.struct_list:
                s+=u"{:30}{:60}{:60}\n".format(struct["FA"],
                                               struct["NL"].replace("["," ").replace("]",""),
                                               struct["NV"].replace(";",","))

        elif event.GetId() == self.popupID_UNSELECT_ALL:
            self.panel.apps.marker_table[self.panel.apps.marker_index] = []
            self.Fill()

        elif event.GetId() == self.popupID_PICT_GALLERY:
            print("popupID_PICT_GALLERY")
            nevent = PictGalleryEvent(struct_list = self.struct_list,
                                      name = self.panel.name)
            wx.PostEvent(self.panel.apps,nevent)

        if s != "":
            TextFrame(s,self.panel)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Vgrid(wx.grid.Grid):

    def __init__(self, vpanel, panel, data_t, data_string_t): #, index):

        print("wxgrid.py : Vgrid.__init__ / start ...")

        self.title = vpanel.title
        self.data_string_t = data_string_t
        self.data_t = data_t

        self.index = -1 #index
        self.num = vpanel.num
        self.panel = panel

        wx.grid.Grid.__init__(self, vpanel, -1)
        self.SetDefaultCellBackgroundColour(self.panel.colors.normal[1])
        self.SetDefaultCellTextColour(self.panel.colors.normal[0])

        self.Fill()
        #self.SetTable(self.tableBase)

#        # Highlight Selected Row
#        #------------------------
#        attr = wx.grid.GridCellAttr()
#        attr.SetBackgroundColour(self.panel.colors.selected[1])
#        attr.SetTextColour(self.color_t[self.index])
#        self.SetRowAttr(self.index, attr)

        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        if font.SetFaceName("Liberation Mono"):
            print 'Set "Liberation Mono"'
            self.SetDefaultCellFont(font)
        else:
            font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.SetDefaultCellFont(font)

        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnMouse_LeftClick)
        if self.num == 3:
            self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.RightClick)

        self.Bind(wx.EVT_KEY_DOWN, self.onKey)

        print("wxgrid.py : Vgrid.__init__ / done ...")

    #-------------------------------------------------------------------------------
    def Fill(self):
        self.grid_data_t = []
        self.color_t = []

        markers_detected = 0
        if self.data_t == []:
            self.grid_data_t = [[""]]
        else:
            for i in range(0,len(self.data_t)):
                if self.num == 3:
                    mark = ""
                    for k in range(0,len(self.panel.apps.marker_table)):
                        if self.data_t[i] in self.panel.apps.marker_table[k]:
                            mark = "m{}".format(k+1)
                            break

                    row = [mark,self.data_t[i]]
                    if mark == "":
                        color = self.panel.colors.normal[0]
                    else:
                        color = "#ff9933"
                        markers_detected = 1
                else:
                    row = ["",self.data_string_t[i]]
                    color = self.panel.colors.normal[0]
                self.grid_data_t.append(row)
                self.color_t.append(color)

        if markers_detected:
            self.col_label_t=[[25,"m"],[250,self.title]]
        else:
            self.col_label_t=[[0,"m"],[250,self.title]]

        self.tableBase = HugeGrid(self.grid_data_t)
        self.SetTable(self.tableBase)

        self.SetRowLabelSize(0)
        self.SetColLabelSize(25)
        self.SetColLabelAlignment(wx.ALIGN_LEFT,wx.ALIGN_LEFT)
        self.SetDefaultRowSize(18)
        self.EnableEditing(False)
        self.SetLabelBackgroundColour('#303030')
  	self.SetLabelTextColour('#73e600')

        for i in range(0,len(self.col_label_t)):
            self.SetColLabelValue(i,self.col_label_t[i][1])
            self.SetColSize(i,self.col_label_t[i][0])

        #print self.color_t
        # Set Text Color for each row ...
        #--------------------------------
        for i in range(0,len(self.data_t)):
            attr = wx.grid.GridCellAttr()
            attr.SetTextColour(self.color_t[i])
            self.SetRowAttr(i, attr)
        #print self.color_t

    #-------------------------------------------------------------------------------
    def onKey(self,event):
        code = event.GetKeyCode()
        print "onKey",code

        update=0
        if code == 315 and self.index > 0:
            row = self.index-1
            update=1
        elif code == 317 and self.index < (len(self.grid_data_t) - 1):
            row = self.index+1
            update=1

        if update:
            self.SetSelection(row)
            self.panel.Update(self.num,self.index)

            #self.SetGridCursor(row, 0)
            #wx.CallAfter(self.MakeCellVisible, row, 0)
            self.SetFocus()
            print("VGrid.onkey SetFocus")


    #-------------------------------------------------------------------------------
    def UpdateGrid(self,vpanel, data_t, data_string_t, index):

        print("Upgrade Grid #{}".format(index))
        self.data_string_t = data_string_t
        self.data_t = data_t
        self.index = -1
        #self.tableBase.SetData(self.grid_data_t)
        self.Fill()
        #self.tableBase.ResetView(self)

        self.SetSelection(index)

    #-------------------------------------------------------------------------------
    def SetSelection(self,row):

        #print("self.NUM",self.num)
        #print("self.INDEX",self.index)
        #print("self.COLOR_t",self.color_t)

        if self.index != -1:
            attr = wx.grid.GridCellAttr()
            attr.SetBackgroundColour(self.panel.colors.normal[1])
            attr.SetTextColour(self.color_t[self.index])
            self.SetRowAttr(self.index, attr)

        print("SetSelection OLD={}  NEW={}".format(self.index,row))
        self.index = row
        #attr = wx.grid.GetRowAttr(index)
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(self.panel.colors.selected[1])
        #attr.SetTextColour(self.panel.colors.selected[0])
        attr.SetTextColour(self.color_t[self.index])
        self.SetRowAttr(self.index, attr)
        self.Refresh()


    #-------------------------------------------------------------------------------
    def OnMouse_LeftClick(self, evt):

        print("")
        print("wxgrid.py : Vgrid.OnMouse_LeftClick()")

        state = wx.GetMouseState()
        print(evt.Row,self.grid_data_t[evt.Row])
        self.SetSelection(evt.Row)

        # Row selection
        if state.ControlDown():
            print("State Control+Down",self.index)
            if self.num == 3:
                row = evt.Row

                print(row,self.data_t)

                spe_name = self.data_t[row]

                if spe_name in self.panel.apps.marker_table[self.panel.apps.marker_index]:
                    self.panel.apps.marker_table[self.panel.apps.marker_index].remove(spe_name)
                else:
                    self.panel.apps.marker_table[self.panel.apps.marker_index].append(spe_name)

                #self.Fill()
                print self.panel.apps.marker_table
                self.Fill()

        self.panel.Update(self.num,self.index)
        #evt.Skip()

    #-------------------------------------------------------------------------------
    def RightClick(self,event):

        self.popupRow = event.GetRow()
        self.popupCol = event.GetCol()
        menu = wx.Menu()

        self.popupID_EXPORT = wx.NewId()
        self.popupID_TEST = wx.NewId()


        menu.Append(self.popupID_EXPORT, "Export to TXT")
        menu.Append(self.popupID_TEST, "Test")

        self.Bind(wx.EVT_MENU, self.RightClickMenu)

        self.PopupMenu(menu)
        menu.Destroy()

    #-------------------------------------------------------------------------------
    def RightClickMenu(self,event):
        print("RightClickMenu")

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Vpanel(wx.Panel):

    #-------------------------------------------------------------------------------
    def __init__(self, parent, panel, num, data_t, data_string_t, index):

        self.num = num

        self.title = {0:"Division",
                      1:"Famille",
                      2:"Genre",
                      3:"Espece"}[num]

        wx.Panel.__init__(self,parent=parent)

        self.grid = Vgrid(self, panel, data_t, data_string_t)
        self.grid.SetSelection(index)

        #self.colors = apps.colors

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)

    #-------------------------------------------------------------------------------
    def UpdateGrid(self, apps, data_t, data_string_t, index):

        self.grid.UpdateGrid(apps, data_t, data_string_t, index)
        #self.Refresh()
        self.Layout()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
