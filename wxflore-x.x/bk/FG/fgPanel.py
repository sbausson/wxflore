# -*- coding: utf-8 -*-

import os
import re
import wx
import wx.richtext
import wx.grid
#import bota
from common import *

class COLORS:
    normal = ["#ffffff","#101010"]
    selected = ["#ccff33","#707070"]

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
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class bkGrid(wx.grid.Grid):

    def __init__(self, parent, panel, bkHeader, items, index, options):

        print("wxgrid.py : filteredGrid.__init__ / start ...")

        #self.title = panel.title
        self.options = options
        self.panel = panel
        self.bkHeader = bkHeader
        self.items = items
        self.index = index
        self.colors = parent.colors

        # This was wrong ! wx.grid.Grid.__init__(self, panel, -1)
        wx.grid.Grid.__init__(self, parent, -1)
        self.SetGridLineColour(self.colors.normal[1])
        self.Fill()

        #self.SetSelection(index)

#        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,  self.OnMouse_LeftClick)
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

        s=""
        first = 1
        for line in self.bkHeader:
            if not first:
                s+="\n"

            s+=u"{}".format(line)
        row = ["",s]
        self.grid_data_t.append(row)
        self.color_t.append("")
        #self.color_t.append("#3399ff")


        for item in self.items:
            s=""
            s+=item["caract"]
            #s+=u"\n= {}".format(item["action"])
            row = [item["key"],s]
            self.grid_data_t.append(row)
            self.color_t.append("")
            i+=1

            # action
            s=""
            if re.match("[0-9]",item["action"]):
                s+=u"Voir #{}".format(item["action"])
                #self.color_t.append("#ff9900")
                self.color_t.append("#ffff66")
            else:
                s+=u"= {}".format(item["action"])
                self.color_t.append("#33cc33")
            row = ["",s]
            self.grid_data_t.append(row)
            i+=1

            # choro
            s=""
            if item["choro"] != "":
                s+=u"{}".format(item["choro"])
                row = ["",s]
            else:
                row = ["",""]
            self.grid_data_t.append(row)
            self.color_t.append("#999966")
            i+=1

            # note
            s=""
            if item["note"] != "":
                s+=u"Note: {}".format(item["note"])
                row = ["",s]
            else:
                row = ["",""]

            self.grid_data_t.append(row)
            self.color_t.append("#99ccff")
            i+=1

            row = [""," "]
            self.grid_data_t.append(row)
            self.color_t.append("")
            i+=1

        self.tableBase = HugeGrid(self.grid_data_t)
        self.SetTable(self.tableBase)

        #self.SetDefaultRenderer(wx.grid.GridCellAutoWrapStringRenderer())
        self.SetDefaultCellBackgroundColour(self.colors.normal[1])
        self.SetDefaultCellTextColour(self.colors.normal[0])

        self.SetRowLabelSize(0)
        self.SetColLabelSize(25)
        self.SetColLabelAlignment(wx.ALIGN_LEFT,wx.ALIGN_LEFT)

        self.SetDefaultRowSize(16)
        self.EnableEditing(False)

        self.SetLabelBackgroundColour('#303030')
  	self.SetLabelTextColour('#73e600')

        self.SetColLabelValue(0,"Seq.")
        self.SetColSize(0,40)

        self.SetColLabelValue(1,"Charact.")
        self.SetColSize(1,1400)


        for i in range(0,len(self.grid_data_t)):
            attr = wx.grid.GridCellAttr()

            if self.grid_data_t[i] == ["",""]:
                self.SetRowSize(i,0)

            elif self.color_t[i] != "":
                attr.SetTextColour(self.color_t[i])
                #self.AutoSizeRow(i)

            self.SetRowAttr(i, attr)
            #self.SetRowSize(i, 10)

#
#        attr = wx.grid.GridCellAttr()
#        attr.SetBackgroundColour(self.panel.colors.selected[1])
#        attr.SetTextColour(self.color_t[self.index])
#        self.SetRowAttr(self.index, attr)

        colors_t = {"blanc":["white","black"],
                    "bleu":["blue","white"],
                    "rose":["pink","black"],
                    "vert":["green","black"],
                    "jaune":["yellow","black"],
        }


#        for i in range(0,len(self.struct_list)):
#            color = "none"
#            try:
#                color = self.struct_list[i]["baseflor"]["FL.col"].split(",")[0].strip()
#                self.SetCellBackgroundColour(i,3,colors_t[color][0])
#                self.SetCellTextColour(i,3,colors_t[color][1])
#
#                #print("COLOR SET")
#            except:
#                print("## WARNING ## color: {}".format(color))
#                pass



        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        if font.SetFaceName("Liberation Mono"):
            print 'Set "Liberation Mono"'
            self.SetDefaultCellFont(font)
        else:
            font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.SetDefaultCellFont(font)

        self.AutoSizeRows(True)
        #self.Refresh()

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
        attr.SetBackgroundColour(self.colors.normal[1])
        #attr.SetTextColour(self.panel.colors.normal[0])
#        attr.SetTextColour(self.color_t[self.index])
#        self.SetRowAttr(self.index, attr)

        print("SetSelection OLD={}  NEW={}".format(self.index,row))
        self.index = row
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(self.colors.selected[1])
        #attr.SetTextColour(self.panel.colors.selected[0])
#        attr.SetTextColour(self.color_t[self.index]) #panel.colors.selected[0])
#        self.SetRowAttr(self.index, attr)
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
#        s = ""
#        if event.GetId() == self.popupID_FILTER_GENDER:
#            pass
#
#        elif event.GetId() == self.popupID_EXPORT_ID_TELA:
#            for struct in self.struct_list:
#                s+="{}\n".format(struct["ID.tela"])
#
#        elif event.GetId() == self.popupID_EXPORT_NL:
#            for struct in self.struct_list:
#                s+=u"{:60}\n".format(struct["NL"].replace("["," ").replace("]",""))
#
#        elif event.GetId() == self.popupID_EXPORT_NL_NV:
#            for struct in self.struct_list:
#                s+=u"{:60}{:60}\n".format(struct["NL"].replace("["," ").replace("]",""),
#                                          struct["NV"].replace(";",","))
#
#        elif event.GetId() == self.popupID_EXPORT_FA_NL_NV:
#            for struct in self.struct_list:
#                s+=u"{:30}{:60}{:60}\n".format(struct["FA"],
#                                               struct["NL"].replace("["," ").replace("]",""),
#                                               struct["NV"].replace(";",","))
#
#        elif event.GetId() == self.popupID_UNSELECT_ALL:
#            self.panel.apps.marker_table[self.panel.apps.marker_index] = []
#            self.Fill()
#
#        elif event.GetId() == self.popupID_PICT_GALLERY:
#            print("popupID_PICT_GALLERY")
#            nevent = PictGalleryEvent(struct_list = self.struct_list,
#                                      name = self.panel.name)
#            wx.PostEvent(self.panel.apps,nevent)
#
#        if s != "":
#            TextFrame(s,self.panel)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#class bkRichText(wx.RichText):
#
#    #-------------------------------------------------------------------------------
#    def __init__(self, parent, panel, bkHeader, data_t, options):
#
#        self.colors = COLORS()
#        self.title = "Title"
#        wx.TextCtrl.__init__(self,parent=parent)
#        self.AppendText("toto")
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class bkPanel(wx.Panel):

    #-------------------------------------------------------------------------------
    def __init__(self, parent, panel, bkHeader, items, options):

        self.colors = COLORS()
        self.title = "Title"
        self.bkHeader = bkHeader
        self.items = items

        wx.Panel.__init__(self,parent=parent)

        index = 0
        #self.grid = bkRichText(self,panel,bkHeader,data_t,options)
        #self.grid.SetSelection(index)
        self.RTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER) #|wx.TE_MULTILINE)
        #self.RTC.SetEditable(False)
        #self.RTC.Freeze()
        #self.RTC.BeginSuppressUndo()
        self.RTC.BeginParagraphSpacing(0, 20)


        self.RTC.SetBackgroundColour(self.colors.normal[1])
        #self.RTC.SetForegroundColour(self.colors.normal[0])

        self.RTC.BeginTextColour(self.colors.normal[0])

        # Botanical Key header
        #----------------------
        s=""
        first = 1
        for line in self.bkHeader:
            if first:
                self.RTC.BeginFontSize(14)
                self.RTC.WriteText(line)
                self.RTC.EndFontSize()
                self.RTC.BeginFontSize(10)
                first = 0
            else:

                self.RTC.WriteText(line)

        self.RTC.WriteText("\n\n")

        # Key items
        #-----------
        for item in self.items:

            # key + caract
            s=u""
            s+=u"{} — {}\n".format(item["key"],item["caract"])
            self.RTC.WriteText(s)

            # action
            s=u""
            if re.match("[0-9]",item["action"]):
                #self.color_t.append("")
                #self.color_t.append("#ffff66")
                self.RTC.BeginTextColour("#ff9900")
                self.RTC.WriteText(u"Voir #{}".format(item["action"]))
                self.RTC.EndTextColour()

            else:
                #print(item["action"])
                re_names = re.match(u"(.*)(\[.*\])",item["action"])

                if re_names:
                    l = re_names.groups()

                else:
                    l = [item["action"]]

                print(l[0])
                if re.match(".* subsp\.? ",l[0]):
                    ll = re.match("([A-Z][a-z\. ]+)([\(\)A-Z].*) subsp\.? ([a-z]+) (.*)",l[0]).groups()
                    print(ll)
                else:
                    ll = re.match("([A-Z][a-z\. ]+)([\(\)A-Z].*)",l[0]).groups()

                self.RTC.BeginTextColour("#33cc33")
                self.RTC.BeginBold()
                self.RTC.BeginItalic()
                self.RTC.WriteText(u"= {}".format(ll[0]))
                self.RTC.EndItalic()
                self.RTC.EndBold()
                if len(ll) == 2:
                    self.RTC.WriteText(u"{}".format(ll[1]))

#                elif len(ll) == 3:
#                    self.RTC.WriteText(u"{} subsp. ".format(ll[1]))
#                    self.RTC.BeginBold()
#                    self.RTC.BeginItalic()
#                    print(" {}".format(ll[2]))
#                    self.RTC.EndItalic()
#                    self.RTC.EndBold()

                elif len(ll) == 4:
                    print(ll)
                    self.RTC.WriteText(u"{} subsp. ".format(ll[1]))
                    self.RTC.BeginBold()
                    self.RTC.BeginItalic()
                    self.RTC.WriteText(" {}".format(ll[2]))
                    self.RTC.EndItalic()
                    self.RTC.EndBold()
                    self.RTC.WriteText(" {}".format(ll[3]))

                self.RTC.EndTextColour()

                if len(l) > 1:
                    self.RTC.BeginTextColour("white")
                    self.RTC.WriteText(u"  {}".format(l[1]))
                    self.RTC.EndTextColour()

            self.RTC.WriteText("\n")

            # chorologie
            #------------
            if item["choro"] != "":
                self.RTC.BeginTextColour("#999966")
                self.RTC.WriteText(u"{}\n".format(item["choro"]))
                self.RTC.EndTextColour()
                #self.RTC.WriteText("\n")

            # note
            #------
            if item["note"] != "":
                self.RTC.BeginTextColour("#99ccff")
                self.RTC.WriteText(u"Note: {}\n".format(item["note"]))
                self.RTC.EndTextColour()

            self.RTC.WriteText("\n")


        self.RTC.EndTextColour()
        #self.RTC.Thaw()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.RTC, 1, wx.EXPAND)
        self.SetSizer(sizer)

    #-------------------------------------------------------------------------------
    def UpdateGrid(self, apps, data_t, index):

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
