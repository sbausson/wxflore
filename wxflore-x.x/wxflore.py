#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import wx
import re
import functools
import codecs
import wx.lib.newevent
import importlib

# AUI
import wx.lib.agw.aui as aui
import wx.aui
from wx.lib.splitter import MultiSplitterWindow
import wx.richtext

import wxgrid
import observations
import fldb
import wxeditor
import bota
import config
import mkthumb

import panelThumb
import panelMain
import panelDesc

from common import *

ID_HELP_ABOUT = 300
ID_HELP_CREDITS = 301

class colors:
    # [FG,BG]
    #selected = ["#cc3399","#99ff33"]
    #selected = ["#ccff66","#808080"]
    selected = ["#ccff33","#707070"]
    selection = ["#ff9933","#202020"]

    #normal = ["#000000","#ffffff"]
    normal = ["#ffffff","#101010"]
    #nl = ["#ffffff","#202020"]
    nl = ["#ffffff","#202020"]

    #nv = ["#3333CC","#202020"]
    nv = ["#3399ff","#202020"]

    #fa = ["#990033","#202020"]
    fa = ["#ff5c5c","#202020"]

    class button:
        #default = [None,'#DDDDDD'] #5cd65c'
        default = ['#adff2f','#303030']
        obs =     ['#1905AE','#ffcc00']
        note =    ['#1905AE','#00BFFF']

    flower = {"blanc":["#ffffff",None],
              "bleu" :["#4d4dff",None],
              "jaune":["#ffff00",None],
              "rose" :["#ff6699",None],
              "vert" :["#00ff00",None],
    }


format_url_tela = "http://www.tela-botanica.org/bdtfx-nn-{}-synthese\n"
format_url_inpn = "http://inpn.mnhn.fr/espece/cd_nom/{}\n"
format_url_fcnb = "http://siflore.fcbn.fr/?cd_ref={}&r=metro\n"


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def build_text_to_export(struct,markdown=False):

    #-------------------------------------------------------------------------------
    def fill_string(format_string,struct,field_name,field):

        s_res = ""

        if field not in struct and field not in ['FCBN','COSTE']:
            print("====",field)
            return s_res

        if field == 'NL':
            nl1, nl2 = re.findall("(.*)\[(.*)\]",struct['NL'])[0]
            nl1 = nl1.strip()
            nl2 = nl2.strip()
            if markdown:
                s_res = u"***{}***  {}  /  **{}**\n\n".format(nl1,nl2,struct["FA"])
            else:
                s_res = u"{}  {}  /  {}".format(nl1,nl2,struct["FA"])

        elif field in ["NV","N.UK","N.IT","N.DE","N.ES","N.NL","ZO","FL","HB","REF.wiki.fr"]:
            s = struct[field].replace(";",",") #.encode("utf-8")
            s_res+=format_string.format(field_name,s) #.encode("utf-8"))

        elif field in ["SY","DS"]:
            s_res+="\n**{}:**\n".format(field_name)
            for item in struct[field]:
                s_res+=format_string.format(item) #.encode("utf-8"))
            s_res+='\n'

        elif field in ["ID.tela","ID.inpn"]:
            s = struct[field]
            s_res+=format_string.format(field_name,s,s)

        elif field in ["FCBN"]:
            print "FCBN"
            s = struct["ID.inpn"]
            s_res+=format_string.format(field_name,s)

        elif field == 'COSTE':
            s=''
            if "ID.coste" in struct.keys():
                if struct["ID.coste"] != "":
                    s +=u"N°{}".format(struct["ID.coste"])
            if "N.coste" in struct.keys():
                s +=u"  -  {}".format(struct["N.coste"])
            s_res+=format_string.format(field_name,s)

        else:
            s = struct[field] #.encode("utf-8")
            s_res+=format_string.format(field_name,s) #.encode("utf-8"))

        return s_res

    #-------------------------------------------------------------------------------
    s = ""
    if markdown:
        format_string = u'**{}**  :  {}\n'
        format_tela = u'**{}**  :  N°{}  http://www.tela-botanica.org/bdtfx-nn-{}-synthese\n'
        format_inpn = u'**{}**  :  N°{}  http://inpn.mnhn.fr/espece/cd_nom/{}\n'
        format_fcbn = u'**{}**  :  http://siflore.fcbn.fr/?cd_ref={}&r=metro\n'
    else:
        format_string = u'{:25} : {}\n'
        format_tela = u'{:25} : N°{}  http://www.tela-botanica.org/bdtfx-nn-{}-synthese\n'
        format_inpn = u'{:25} : N°{}  http://inpn.mnhn.fr/espece/cd_nom/{}\n'
        format_fcbn = u'{:25} : http://siflore.fcbn.fr/?cd_ref={}&r=metro\n'

    format_list = u'    - {}\n'

    s+=fill_string(format_string,struct,u'Nom latin',"NL")
    #s+=fill_string(format_string,struct,"Famille","FA")
    s+=fill_string(format_string,struct,u'Nom(s) français(s)',"NV")
    s+=fill_string(format_string,struct,u'English',"N.UK")
    s+=fill_string(format_string,struct,u'Nederlands',"N.NL")
    s+=fill_string(format_string,struct,u'Italiano',"N.IT")
    s+=fill_string(format_string,struct,u'Español',"N.ES")
    s+=fill_string(format_string,struct,u'Deutsch',"N.DE")
    if not markdown:
        s+=fill_string(format_list,struct,"Synonymes","SY")
    s+=fill_string(format_list,struct,u'Description',"DS")
    s+=fill_string(format_string,struct,u'Habitat',"HB")
    s+=fill_string(format_string,struct,u'Zone Géographique',"ZO")
    s+=fill_string(format_string,struct,u'Floraison',"FL")
    s+=fill_string(format_string,struct,u'Ref. Coste',"COSTE")
    s+=fill_string(format_string,struct,u'Usage',"US")
    s+=fill_string(format_tela,struct,u'Ref. Tela',"ID.tela")
    s+=fill_string(format_inpn,struct,u'Ref. INPN',"ID.inpn")
    s+=fill_string(format_fcbn,struct,u'Répartition FCBN',"FCBN")
    s+=fill_string(format_string,struct,u'Wiki.Fr',"REF.wiki.fr")

    s+='\n'
    s+='#botanique '
    s+='#botany '
    s+='#botanik '
    s+='#fleur '
    s+='#bloemen '
    s+='#plantes '
    s+='#plants '
    s+='#planten '
    s+='#nature '
    s+='#wild '
    s+='#{} '.format(struct['NL'].split()[0].lower())
    s+='#{} '.format(struct['FA'].lower())
    s+='\n'

    return s

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
        txt.SetForegroundColour("#99ccff")

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
def IsNotebookPageAlreadyExist(notebook,name):
    exist = 0
    for i in range(0,notebook.GetPageCount()):
        if name == notebook.GetPageText(i):
            exist = 1
            break
    if exist:
        return i+1
    else:
        return 0

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def build_baseveg_string(struct,options,markdown=False):

    s=''
    if 'ID.cat' in struct['baseflor'] and struct['baseflor']['ID.cat'] != '':
        st = options.baseveg.table[struct['baseflor']['ID.cat']]
        if markdown:
            fmt = u' - **{}**  :  {}\n'
        else:
            fmt = u' {:35s}  :  {}\n'

        if markdown:
            s+=u'**Baseveg:**\n'
            s+=u'*Index phytosociologique synonymique de la végétation de la France Version [{}]\n'.format(options.baseveg.version)
            s+=u'P. Julve, 1998 ff. Programme Catminat. http://perso.wanadoo.fr/philippe.julve/catminat.htm*\n\n'

        s+=fmt.format(u'Syntaxon',st['SYNTAXON'].decode('utf-8'))
        s+=fmt.format(u'Dénomination écologique',st['ECO.name'].decode('utf-8'))
        s+=fmt.format(u'Chorologie mondiale',st['choro.world'].decode('utf-8'))
        s+=fmt.format(u'Répartition connue en France',st['REP.fr'].decode('utf-8'))
        s+=fmt.format(u'Physionmie',st['C.physio'].decode('utf-8'))
        s+=fmt.format(u'Etages altitudinaux (altitude)',st['C.alti'].decode('utf-8'))
        s+=fmt.format(u'Latitude',st['C.lat'].decode('utf-8'))
        s+=fmt.format(u'Océanité',st['C.ocea'].decode('utf-8'))
        s+=fmt.format(u'Température',st['C.temp'].decode('utf-8'))
        s+=fmt.format(u'Lumière',st['C.lum'].decode('utf-8'))
        s+=fmt.format(u'Exposition, pente',st['C.exp'].decode('utf-8'))
        s+=fmt.format(u'Optimum de développement',st['C.opt'].decode('utf-8'))
        s+=fmt.format(u'Humidité atmosphérique',st['C.humi.nat'].decode('utf-8'))
        s+=fmt.format(u"Types de sol et d'humus",st['C.humus'].decode('utf-8'))
        s+=fmt.format(u'Humidité édaphique',st['C.humi.ned'].decode('utf-8'))
        s+=fmt.format(u'Texture du sol',st['C.tex'].decode('utf-8'))
        s+=fmt.format(u'Niveau trophique',st['C.niv.troph'].decode('utf-8'))
        s+=fmt.format(u'pH du sol',st['C.pH'].decode('utf-8'))
        s+=fmt.format(u'Salinité',st['C.sal'].decode('utf-8'))
        s+=fmt.format(u'Dynamique',st['C.dyn'].decode('utf-8'))
        s+=fmt.format(u'Influences anthropozoogènes',st['C.infl'].decode('utf-8'))

    return s

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Panel_baseveg(wx.Panel):

    def __init__(self, parent, struct, button, options):
        print("Panel_baseveg")
        self.parent = parent
        self.struct = struct
        self.button = button
        self.options = options

        wx.Panel.__init__(self, parent, -1)
        self.SetAutoLayout(1)

        self.RTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.TE_MULTILINE)

        #font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL) #MODERN
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, 'Monospace')

        self.RTC.BeginFont(font)

        self.RTC.SetBackgroundColour(self.parent.colors.normal[1])
        self.RTC.SetForegroundColour(self.parent.colors.normal[0])
        self.RTC.SetEditable(False)
        #self.RTC.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)

        self.RTC.BeginTextColour(parent.colors.normal[0])

        s = build_baseveg_string(struct,self.options)
        if s!= '':
            self.RTC.SetValue(s)


        self.RTC.GetCaret().Hide()

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.RTC,1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(sizer)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Panel_NOTES(wx.Panel):

    def __init__(self, parent, struct, filename, button):
        print("Panel_NOTES")
        self.parent = parent
        self.struct = struct
        self.button = button
        self.fn = filename
        wx.Panel.__init__(self, parent, -1)
        self.SetAutoLayout(1)

        self.RTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.TE_MULTILINE)
        #self.RTC = wx.TextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.RTC.SetBackgroundColour(self.parent.colors.normal[1])
        self.RTC.SetForegroundColour(self.parent.colors.normal[0])
        #self.RTC.SelectNone()
        self.RTC.SetEditable(False)
        self.RTC.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)

        self.RTC.BeginTextColour(parent.colors.normal[0])

        self.ReadNotes()

        self.RTC.GetCaret().Hide()

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.RTC,1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(sizer)

    #-------------------------------------------------------------------------------
    def RightClick(self,event):

        menu = wx.Menu()
        self.popupID_EDIT = wx.NewId()
        menu.Append(self.popupID_EDIT, "Edit this Note")
        self.Bind(wx.EVT_MENU, self.RightClickMenu)
        self.PopupMenu(menu)
        menu.Destroy()

    #-------------------------------------------------------------------------------
    def RightClickMenu(self,event):

        print("RightClickMenu")

        if event.GetId() == self.popupID_EDIT:
            ed = wxeditor.MainWindow(self,
                                     u"Note : {}".format(self.struct["nl"]),
                                     self.fn,
                                     self.parent.colors)
            ed.ShowModal()
            self.ReadNotes()
            nevent = NoteUpdateEvent()
            wx.PostEvent(self.parent,nevent)


    #-------------------------------------------------------------------------------
    def ReadNotes(self):

        print("ReadNotes",self.fn)

        try:
            f = codecs.open(self.fn, "r", "utf-8")
            text = ''.join(f.readlines())
            f.close()
        except:
            text = ""

        self.RTC.SetValue(text)
        print(text)
        #self.Refresh()


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class PanelSYN(wx.Panel):

    def __init__(self, parent, struct):
        print("PanelSYN")
        self.parent = parent
        wx.Panel.__init__(self, parent, -1)
        self.SetAutoLayout(1)

        self.RTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
        self.RTC.SetBackgroundColour(self.parent.colors.normal[1])
        self.RTC.SetForegroundColour(self.parent.colors.normal[0])
        self.RTC.SelectNone()
        self.RTC.SetEditable(False)

        s = ""
        self.RTC.BeginTextColour(parent.colors.normal[0])

        for syn in struct["SY"]:
            syn = syn.replace("["," ").replace("]","")
            s+=u"- {}\n".format(syn)

        print(s)
        self.RTC.WriteText(s)
        self.RTC.GetCaret().Hide()

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.RTC,1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(sizer)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class AdvancedSearchPanel(wx.Panel):

    def __init__(self, apps):

        id = 100
        print("AdvancedSearchPanel")

        wx.Panel.__init__(self, apps, -1)
        self.apps = apps

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topicSizer = wx.BoxSizer(wx.HORIZONTAL)
        toolbarSizer = wx.BoxSizer(wx.HORIZONTAL)
        catSizer = wx.BoxSizer(wx.VERTICAL)

        for cat in self.apps.button_config["cat"]["colors"].keys():
            button = wx.Button(self, id, u"{}".format(cat), wx.DefaultPosition, (-1,-1)) #, style=wx.BU_EXACTFIT)

            if self.apps.button_config["cat"]["colors"][cat][0] != -1:
                button.SetForegroundColour(self.apps.button_config["cat"]["colors"][cat][0])

            if self.apps.button_config["cat"]["colors"][cat][1] != -1:
                button.SetBackgroundColour(self.apps.button_config["cat"]["colors"][cat][1])
#            else:
#                button.SetBackgroundColour("#53566E")
            catSizer.Add(button,0,wx.ALIGN_LEFT) #wx.ALL)
            wx.EVT_BUTTON( self, id, functools.partial(self.onCat,cat))
            id+=1

            print("CATEGORY {}".format(cat))

        deptSizer = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(self, -1, "Departements:")
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)
        text.SetForegroundColour("#f3f3f3")

        deptSizer.Add( text,0,wx.TOP|wx.CENTER)

        deptGridSizer = wx.GridSizer(10, 10, 5, 5)

        grid = []
        self.selectDept = [0]*100
        grid.append((wx.StaticText(self), wx.ALIGN_LEFT))
        self.dept_button_t = [None]*100
        for i in range(1,95):
            button = wx.Button(self, label='{}'.format(i),size=(40,-1))
            button.SetForegroundColour("#101010")
            button.SetBackgroundColour("#D0D0D0")
            grid.append((button, 0, wx.ALIGN_LEFT))
            #wx.EVT_BUTTON( self, id, functools.partial(self.onDept,i))
            self.Bind(wx.EVT_BUTTON,functools.partial(self.onDept,i),button)
            self.dept_button_t[i] = button
            id+=1

        deptGridSizer.AddMany(grid)

        deptSizer.Add(deptGridSizer,0,wx.ALL)
        topicSizer.Add(deptSizer,0,wx.ALIGN_LEFT)
        topicSizer.Add(catSizer)
        mainSizer.Add(topicSizer)

        # Toolbar
        button = wx.Button(self, label='SEARCH')
        self.Bind(wx.EVT_BUTTON,self.onAdvancedSearch,button)
#        button.SetForegroundColour("#4610A3")
#        button.SetForegroundColour("#4610A3")

        button.SetBackgroundColour("#2594FD") ##33F62D")
        button.SetForegroundColour("#ffffff")
        toolbarSizer.Add(button,0,wx.ALIGN_LEFT)

        mainSizer.Add(toolbarSizer)

        self.SetSizer(mainSizer)
        self.Layout()

    #-------------------------------------------------------------------------------
    def onCat(self,cat,event):
        pass

    #-------------------------------------------------------------------------------
    def onDept(self,num,event):
        print(num)
        if self.selectDept[num] == 0:
            self.selectDept[num] = 1
            self.dept_button_t[num].SetForegroundColour("#101010")
            #self.dept_button_t[num].SetBackgroundColour("#FFFFFF")
            self.dept_button_t[num].SetBackgroundColour("#F4FE8B") #"#F4FFD6")

        else:
            self.selectDept[num] = 0
            self.dept_button_t[num].SetForegroundColour("#101010")
            self.dept_button_t[num].SetBackgroundColour("#D0D0D0")

        print self.selectDept

        #self.SetAutoLayout(1)

    #-------------------------------------------------------------------------------
    def onAdvancedSearch(self,event):
        print("onAdvancedSearch")


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class FilteredPanel(wx.Panel):

    def __init__(self, apps, filtered_struct_list, attrib_list = []):

        wx.Panel.__init__(self, apps, -1) # size=(1700, 1000))
        #self.mainPanel = wx.Panel(self, -1)
        #self.mainPanel.SetBackgroundColour(wx.RED)

        self.div_data = apps.div_data
        self.div_data_s = apps.div_data_s

        self.apps = apps
        self.tree = apps.tree
        self.content = apps.content
        self.options = apps.options
        self.colors = apps.colors

        self.grids_splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        self.index = 0

        self.grid = wxgrid.filteredGrid(self.grids_splitter, self, filtered_struct_list, self.index, attrib_list)
        #self.grid.SetSelection(self.index)

#        self.grid.Bind(wx.EVT_SET_FOCUS, self.onFocus)
#        self.grid.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

        # iiiiiiiii self.descPanel = DescriptionPanel(self.grids_splitter, self.apps, self.options, colors)
        self.descPanel = panelDesc.Panel(self, self.apps, self.options, colors)

        self.grids_splitter.AppendWindow(self.grid,500)
        self.grids_splitter.AppendWindow(self.descPanel,500)

        mainPanelSizer = wx.BoxSizer(wx.VERTICAL)

#        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
#
#        button = wx.Button(self, wx.ID_ANY, "TOTO", wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
#        button.SetForegroundColour("#600060")
#        button.SetBackgroundColour("#6699ff")
#        self.buttonSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
#
#        mainPanelSizer.Add(self.buttonSizer, 0, wx.EXPAND) #|wx.EXPAND)

        mainPanelSizer.Add(self.grids_splitter, 1, wx.EXPAND)
        self.thumbPanel = panelThumb.Panel(self,self.options)
        self.UpdateDesc()

        mainPanelSizer.Add(self.thumbPanel, 0, wx.EXPAND) #|wx.EXPAND)
        self.SetSizer(mainPanelSizer)


        #mainPanelSizer.Add(self.thumbPanel, 1, wx.ALL|wx.EXPAND)
        #self.grid.SetFocus()
        #self.Layout()

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    def onFocus(self, event):
        #self.grid.SetFocus()
        print "FilteredPanel received focus!"

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    def onKillFocus(self, event):
        print "FilteredPanel lost focus!"

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    def UpdateDesc(self):

        if options.debug:
            print("FilteredPanel.UpdateDesc()")

        struct = self.content[self.grid.data_t[self.index]]

        self.descPanel.UpdateDesc(struct)
        self.thumbPanel.Update(struct)
        self.grid.SetFocus()

        # This cause troules on left click (do not uncomment)

        #        for window in self.grid.GetChildren():
        #            print("+")
        #            window.SetFocus()

        print("FilteredPanel.UpdateDesc > SetFocus")

    #-------------------------------------------------------------------------------
    def Update(self,index):

        if options.debug:
            print("wxflore.py FilteredPanel.Update() / index={}".format(index))

        self.index = index

        if options.debug:
            print("FilteredPanel.Update() call to self.UpdateDesc()")

        #iiiiii
        #self.content[struct["NL"]] = struct
        self.UpdateDesc()

        if options.debug:
            print("FilteredPanel.Update() return from self.UpdateDesc()")

        self.Layout()

    #-------------------------------------------------------------------------------
    def Refresh(self,struct=None):

        if struct != None:
            self.content[struct["NL"]] = struct

        self.UpdateDesc()
        self.Layout()


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MyDialog ( wx.Dialog ):

    def __init__( self, parent, msg ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString,
                             pos = wx.DefaultPosition,
                             #size = wx.Size(-1,-1),
                             style = wx.DEFAULT_DIALOG_STYLE )

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel( self, wx.ID_ANY,
                               wx.DefaultPosition,
                               wx.DefaultSize)

        self.m_staticText = wx.StaticText( self.panel, wx.ID_ANY, u"test",
                                           wx.DefaultPosition,
                                           wx.DefaultSize,
                                           0 )
        mainSizer.Add( self.panel, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_sdbSizerOK = wx.Button( self, wx.ID_OK, size=(-1,50) )
        mainSizer.Add( self.m_sdbSizerOK, 1, wx.ALL|wx.CENTER, 5 )
        self.SetSizer( mainSizer )
        self.m_staticText.SetLabel(msg)
        self.Fit()


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MainApp(wx.Frame):

    def build_tables(self,base_flore_path):

        #print("base_flore_path",base_flore_path)

        struct_table  = fldb.python_table(base_flore_path,self.options)

        res_table = {}
        res_table_content = {}
        class stats:
            fam_list = []
            gen_list = []
            spe_list = []
            gen_count = {}
            fam_count = {}

        #for struct in [struct_table[key] for key in struct_table.keys()]:
        for key in struct_table.keys():

            struct = struct_table[key]
            #print(struct["NL"])

            #print key
            #gen = struct["NL"].split()[0]
            fam = struct["FA"]

            #print struct["NL"]
            x, gen, spe = re.findall("(× )?([A-Z][a-z]+)\s+(.*)",struct["NL"])[0]

#            if struct["NL"] in res_table[fam][gen]:
#                error()

            if fam in res_table.keys():
                if gen in res_table[fam].keys():
                    res_table[fam][gen].append(struct["NL"])
                else:
                    res_table[fam][gen] = [struct["NL"]]
            else:
                res_table[fam] = {}
                res_table[fam][gen] = [struct["NL"]]

            if not fam in stats.fam_list:
                stats.fam_list.append(fam)
            if not gen in stats.gen_list:
                 stats.gen_list.append(gen)
            if not struct["NL"] in stats.spe_list:
                stats.spe_list.append(struct["NL"])

            if fam in stats.fam_count.keys():
                stats.fam_count[fam]+=1
            else:
                stats.fam_count[fam]=1

            if gen in stats.gen_count.keys():
                stats.gen_count[gen]+=1
            else:
                stats.gen_count[gen]=1

            #struct["REF"] = key
            #print("[ {} ]".format(struct["REF"]))
            res_table_content[struct["NL"]] = struct


        print len(stats.fam_list), len(stats.gen_list), len(stats.spe_list)

        #print stats.fam_count
        #print stats.gen_count

        self.stats = stats()
        self.table = res_table
        self.content = res_table_content

    def __init__(self, options):


        import classification

        xMaxDisplaySize, yMaxDisplaySize = wx.GetDisplaySize()

        self.size = {}
        if options.wxga or yMaxDisplaySize < 1000 :
            size = (1366,768)
            self.size["FONT.BIG"] = 11
            self.size["FONT.SMALL"] = 8
            self.size["THUMB.XMAX"] = 160
            self.size["THUMB.YMAX"] = 200
        else:
            size = (1700, 1100)
            self.size["FONT.BIG"] = 14
            self.size["FONT.SMALL"] = 10
            self.size["THUMB.XMAX"] = 240
            self.size["THUMB.YMAX"] = 300


        self.button_config = {"cat":{
            "colors":{
                u"Alpine":["#D1F5FA","#9D96A1"],
                u"Aquatique":["#f0f0f0","#3399ff"],
                u"Foret":["#002900","#00cc00"],
                u"Fougere":["#0C5A10","#A4D765"],
                u"Ligneuse":[-1,-1],
                u"Littoral":["#117BA7","#E9D27C"],
                u"Mediterranee":["#101010","#80ffff"], #,"#F0F0F0"],
                u"Montagne":["#701FE5","#D1ED4A"],
                u"Sous-arbrisseau":[-1,-1],
                },
            "names":{
                "Alpine":u"Alpine",
                "Aquatique":u"Aquatique",
                "Foret":u"Forêt",
                "Fougere":u"Fougère",
                "Ligneuse":u"Ligneuse",
                "Littoral":u"Littoral",
                "Mediterranee":u"Méditerranée",
                "Montagne":u"Montagne",
                "Sous-arbrisseau":u"Sous-arbrisseau",
            }
            },

        "redlist":{"colors":
                       {"RE":["#e0e0e0","#6600cc"],
                        "CR":["#600060","red"],
                        "EN":["#600060","orange"],
                        "VU":["#600060","yellow"],
                        "NT":["#600060","grey"],
                        "LC":["#600060","green"],
                        "DD":["yellow","grey"]},
                   "names":{"RE":u"Disparue en Métropole",
                            "CR":u"En danger critique",
                            "EN":u"En danger",
                            "VU":u"Vulnérable",
                            "NT":u"Quasi menacée",
                            "LC":u"Précaution mineure",
                            "DD":u"Données insufisantes"}
                   }
            }

        self.button_list = {"cat":[]}

        wx.Frame.__init__(self, None, title="MainFrame", size=size)
        self.SetBackgroundColour("#202020")


        #locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        #self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,  self.OnMouse_LeftClick)

        #self.options = aplog.OPTIONS()
        #self.options.history_file = "wxap.conf"
        #self.options.color_file = "wxap.colors"
        title = "wxFlore"
        try:
            title+=" ({})".format(classification.title)
        except:
            pass

        self.SetTitle(title)
        self.title = "Famille"
        self.options = options
        self.colors = colors

        self.marker_index=0
        self.s_buttons = []
        self.n_s_buttons = 3
        self.marker_table = [[] for i in range(0,self.n_s_buttons)]
        self.selection_panels = [None]*self.n_s_buttons

        self.LoadMarkers()
        self.build_tables(options.paths.db)

        # Application Menu
        #------------------
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT,'&Quit\tCtrl+Q')
        fileMenu.Append(wx.ID_OPEN, '&Open')

        fileMenu.AppendSeparator()
        fileMenu.AppendItem(qmi)

        helpMenu.Append(ID_HELP_CREDITS,"Credits")
        helpMenu.Append(ID_HELP_ABOUT,"About")

        self.Bind(wx.EVT_MENU, self.onQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onOpenFile, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.onHelpCredits, id=ID_HELP_CREDITS)
        self.Bind(wx.EVT_MENU, self.onHelpAbout, id=ID_HELP_ABOUT)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindows)

        menubar.Append(fileMenu, '&File')
        menubar.Append(helpMenu, '&Help')

        self.SetMenuBar(menubar)

        # Toolbar
        #---------
#        toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
#                                  wx.TB_FLAT | wx.TB_NODIVIDER)
#
#        toolbar.Realize()

        id = 40

        # StatusBar
        #-----------
        #self.statusbar = wx.StatusBar(self, -1)
        #self.statusbar = self.CreateStatusBar()
        #statusbar_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #sep = "    "
        #self.statusbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
        #                            wx.TB_FLAT | wx.TB_NODIVIDER)


        self.statusbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.statusbar = wx.Panel(self,size=(-1,35))

        self.statusbar.SetBackgroundColour(self.colors.normal[1])
        self.statusbar.SetForegroundColour(self.colors.normal[0])

        self.statusbar_sizer.Add((10,-1))
        statictext = wx.StaticText(self.statusbar, -1, "Familles: {}".format(len(self.stats.fam_list)))
        self.statusbar_sizer.Add(statictext, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=0)
        self.statusbar_sizer.Add((20,-1))
        #self.statusbar_sizer.AddControl(statictext)

        statictext = wx.StaticText(self.statusbar, -1, "Genres: {}".format(len(self.stats.gen_list)))
        self.statusbar_sizer.Add(statictext, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=0)
        self.statusbar_sizer.Add((20,-1))
        #self.statusbar.AddControl(statictext)

        statictext = wx.StaticText(self.statusbar, -1, "Especes: {}".format(len(self.stats.spe_list)))
        self.statusbar_sizer.Add(statictext, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=0)
        self.statusbar_sizer.Add((20,-1))
        #self.statusbar.AddControl(statictext)

        button = wx.Button(self.statusbar, id, "m1", wx.DefaultPosition, (35,-1))
        button.selection = 0
        self.statusbar_sizer.Add(button,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        #self.statusbar.AddControl(button)
        self.s_buttons.append(button)
        wx.EVT_BUTTON( self, id, self.Button_MARKER)
        id+=1

        button = wx.Button(self.statusbar, id, "m2", wx.DefaultPosition, (35,-1))
        button.selection = 1
        self.statusbar_sizer.Add(button,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        #self.statusbar.AddControl(button)
        self.s_buttons.append(button)
        wx.EVT_BUTTON( self, id, self.Button_MARKER)
        id+=1

        button = wx.Button(self.statusbar, id, "m3", wx.DefaultPosition, (35,-1))
        button.selection = 2
        self.statusbar_sizer.Add(button,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        #self.statusbar.AddControl(button)
        self.s_buttons.append(button)
        wx.EVT_BUTTON( self, id, self.Button_MARKER)
        id+=1

        self.select_button(self.marker_index)

        #self.statusbar.AddControl(wx.StaticText(self.statusbar, -1, sep))
        statictext = wx.StaticText(self.statusbar, label=" Search")
        self.statusbar_sizer.Add(statictext ,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=0)

        self.filter_cb = wx.ComboBox(self.statusbar,  wx.CB_DROPDOWN,
                                     style=wx.TE_PROCESS_ENTER, pos=(25,25), size=(400,28))
        self.filter_cb.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.filter_cb.SetBackgroundColour("#99ff66") ##ccff99")
        #self.filter_cb.SetBackgroundColour("#008888") ##ccff99")
        self.filter_cb.SetForegroundColour("#050505") ##ccff99")

        self.filter_cb.Clear()
        self.statusbar_sizer.Add(self.filter_cb, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        #self.statusbar.AddControl(self.filter_cb)
        #self.statusbar.SetSizer(statusbar_sizer)
        self.Bind(wx.EVT_TEXT_ENTER, self.onFilterTextEnter, self.filter_cb)
        self.Bind(wx.EVT_LEFT_DOWN, self.onCbSelect, self.filter_cb)
        self.Bind(wx.EVT_TEXT, self.onTextEntered, self.filter_cb)
        self.filter_cb.Bind(wx.EVT_LEFT_DOWN, self.onCbSelect)


        # Advanced Search
        #-----------------
        button = wx.Button(self.statusbar, id, u" Advanced Search ", wx.DefaultPosition, (-1,-1)) #, style=wx.BU_EXACTFIT)
        button.SetForegroundColour("#D1DEFA")
        button.SetBackgroundColour("#53566E")
        self.statusbar_sizer.Add(button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        wx.EVT_BUTTON( self, id, self.onAdvancedSearch)
        id+=1


        # Refresh
        #-----------------
        button = wx.Button(self.statusbar, id, u" Refresh ", wx.DefaultPosition, (-1,-1))
        button.SetForegroundColour("#003366")
        button.SetBackgroundColour("#999966")
        self.statusbar_sizer.Add(button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
        wx.EVT_BUTTON( self, id, self.onRefresh)
        id+=1

        self.div_data = [[x[0]] for x in classification.divisions]
        self.div_data += [["Other"]]
        self.div_data += [["All"]]

        self.statusbar.SetSizer(self.statusbar_sizer)
        #self.statusbar.Realize()

        self.tree = {}
        self.div_data = []
        self.div_data_s = []

        for div in classification.divisions:
            n = 0
            self.tree[div[0]] = {}
            for fam in div[1]:
                if fam in self.table.keys():
                    self.tree[div[0]][fam] = {}
                    for gen in self.table[fam].keys():
                        self.tree[div[0]][fam][gen] = self.table[fam][gen]
                        n+=len(self.table[fam][gen])
            self.div_data.append([div[0]])
            self.div_data_s.append("{} ({})".format(div[0],n))

        print("DATA",self.div_data)

        classified_fam_list =  sum([div[1] for div in classification.divisions],[])

        # Other classified Famillies
        #----------------------------
        n=0
        self.tree["Other"] = {}
        for fam in self.table.keys():
            if fam not in classified_fam_list:
                self.tree["Other"][fam] = {}
                for gen in self.table[fam].keys():
                    self.tree["Other"][fam][gen] = self.table[fam][gen]
                    n+=len(self.table[fam][gen])
        self.div_data.append(["Other"])
        self.div_data_s.append("Other ({})".format(n))

        count = {}
        count["LIGNEUX"] = 0
        self.div_data.append(["LIGNEUX"])
        self.tree["LIGNEUX"] = {}

        type_ligneux_flag = hasattr(classification,"type_ligneux")
        if type_ligneux_flag:
            for tl in classification.type_ligneux:
                self.div_data.append([tl])
                self.tree[tl] = {}
                count[tl] = 0

        for fam in self.table.keys():
            for gen in self.table[fam].keys():
                for spe in self.table[fam][gen]:
                    struct = self.content[spe]
                    if "baseflor" in struct.keys():
                        if "TL" in struct["baseflor"].keys() and struct["baseflor"]["TL"] != "":
                            tl = struct["baseflor"]["TL"]
                            if type_ligneux_flag and tl not in classification.type_ligneux:
                                tl = "other"

                            for cat in ["LIGNEUX",tl]:
                                if fam not in self.tree[cat].keys():
                                    self.tree[cat][fam] = {gen:[spe]}
                                else:
                                    if gen not in self.tree[cat][fam].keys():
                                        self.tree[cat][fam][gen] = [spe]
                                    else:
                                        self.tree[cat][fam][gen].append(spe)
                                count[cat]+=1

        self.div_data_s.append("{} ({})".format("LIGNEUX",count["LIGNEUX"]))
        if type_ligneux_flag:
            for tl in classification.type_ligneux:
                self.div_data_s.append("    {} ({})".format(tl,count[tl]))

        self.notebook = aui.AuiNotebook(self) #,aui.AUI_NB_CLOSE_ON_ALL_TABS)

        tabArt = aui.ChromeTabArt()
        tabArt.SetDefaultColours(wx.Colour(20, 20, 20))
        #print(dir(tabArt))
        self.notebook.SetArtProvider(tabArt)

        self.mainPanel = panelMain.Panel(self)
        self.notebook.AddPage(self.mainPanel, "Main", True)
        PageIndex = self.notebook.GetSelection()
        self.notebook.SetPageTextColour(PageIndex,'#669900')

        #self.mainPanel = MainPanel(self)
        #self.notebook.AddPage(self.mainPanel, "Main", True)

        #sizer_0.Add(self.notebook, 1, flag=wx.ALIGN_LEFT|wx.EXPAND)
        #sizer_0.Add(self.statusbar, 1, flag=wx.ALIGN_LEFT) #|wx.EXPAND)

        sizer_0 = wx.BoxSizer(wx.VERTICAL)

#        sizer_0.Add(self.toolbar, 0, wx.EXPAND)
        sizer_0.Add(self.notebook, 1, wx.ALL|wx.EXPAND)
        sizer_0.Add(self.statusbar, 0, wx.ALIGN_LEFT|wx.EXPAND) #|wx.EXPAND)

        self.SetSizer(sizer_0)


        #self.splitter = wx.SplitterWindow(self, -1)
        #self.splitter.SplitVertically(self.panel1, self.panel2, 200) #sashPosition=-500)

        #splitter.SplitVertically(self.panel1, self.panel2)
        #splitter.SetMinimumPaneSize(20)

        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(splitter, 1, wx.EXPAND)
        #self.SetSizer(sizer)

        #self.ShowFullScreen(True)

        self.Show()

        if not options.wxga:
            self.Maximize(True)

    def LoadMarkers(self):
        fn = os.path.join(options.wxflore,u"markers-{}".format(self.options.suffix))
        try:
            f = codecs.open(fn, "r", "utf-8")
            print(u"Loading \"{}\" ...".format(fn))
            for line in f.readlines():
                index,mark = line.split(";")
                self.marker_table[int(index)].append(mark.strip())
            f.close()
        except:
            pass

        print(self.marker_table)

    #-------------------------------------------------------------------------------
#    def OnMouse_LeftClick():
#        print("="*50)
#        print("MainApp.OnMouse_LeftClick")

    #-------------------------------------------------------------------------------
    def SaveMarkers(self):
        fn = os.path.join(options.wxflore,u"markers-{}".format(self.options.suffix))
        print(u"Writting \"{}\" ...".format(fn))

        f = codecs.open(fn, "w", "utf-8")
        #f.write(codecs.BOM_UTF8)
        for index in range(0,len(self.marker_table)):
            for spe in self.marker_table[index]:
                s = u"{};{}\n".format(index,spe)
                print(s,type(s))
                f.write(s)
        f.close()

    #-------------------------------------------------------------------------------
    def onQuit(self,evt):

        self.SaveMarkers()
        self.Destroy()
        sys.exit()

    #-------------------------------------------------------------------------------
    def onCloseWindows(self, evt):
        print "wxbp.py / MainApp.onCloseWindows()"
        dlg = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            self.onQuit(evt)
            self.Destroy()

        dlg.Destroy()

    #-------------------------------------------------------------------------------
    def onOpenFile(self,event):
        pass

    #-------------------------------------------------------------------------------
    def onHelpAbout(self, event):
        try:
            import version
            msg=''
            msg+='wxFlore - Version {}'.format(version.version)
            msg+='\n\nStéphane Bausson (sbausson@gmail.com)'
            msg+='\n\nwxPython version {}'.format(wx.__version__)
            msg+='\n'

            if self.options.bdtfx.version != '':
                msg+='\nbdtfx [{}]'.format(options.bdtfx.version)
            if self.options.baseflor.version != '':
                msg+='\nbaseflor [{}]'.format(options.baseflor.version)
            if self.options.baseveg.version != '':
                msg+='\nbaseveg [{}]'.format(options.baseveg.version)
            if self.options.chorodep.version != '':
                msg+='\nchorodep [{}]'.format(options.chorodep.version)

            print msg
            msg = msg.decode('utf8','ignore')

            wx.MessageBox(msg, "About",wx.OK | wx.ICON_INFORMATION)

        except IOError:
            pass

    #-------------------------------------------------------------------------------
    def onHelpCredits(self, event):
        msg = ''


        msg += """
- BDTFX : Base de données des Trachéophytes de France métropolitaine.
  Version: {}
  http://referentiels.tela-botanica.org/referentiel/index.php?module=Informations&ref=bdtfx
""".format(options.bdtfx.version)

        if options.baseflor.version != '':
            msg+="""
- Baseflor: Index botanique, écologique et chorologique de la Flore de France.
  Catminat, Julve, Ph., 1998 : http://perso.wanadoo.fr/philippe.julve/catminat.htm
  Version: {}
""".format(options.baseflor.version)

        if options.baseveg.version != '':
            msg+="""
- Baseveg : Index phytosociologique synonymique de la végétation de la France.
  Catminat, Julve, Ph., 1998 : http://perso.wanadoo.fr/philippe.julve/catminat.htm
  Version: {}
""".format(options.baseveg.version)

        if options.chorodep.version != '':
            msg+="""
- Chorodep : Listes départementales des plantes de France.
  Catminat, Julve, Ph., 1998 : http://perso.wanadoo.fr/philippe.julve/catminat.htm
  Version: {}
""".format(options.chorodep.version)

        print(msg)
        msg = msg.decode('utf8','ignore')
        #wx.MessageBox(msg, "Credits",wx.OK | wx.ICON_INFORMATION)
        dlg = MyDialog(self,msg)
        dlg.ShowModal()

    #-------------------------------------------------------------------------------
    def select_button(self,index):

        for i in range(0,self.n_s_buttons):
            self.s_buttons[i].SetForegroundColour("#202020")
            if index == i:
                self.s_buttons[i].SetForegroundColour("#101010")
                self.s_buttons[i].SetBackgroundColour("#ccff66")
            else:
                self.s_buttons[i].SetForegroundColour("#808080")
                self.s_buttons[i].SetBackgroundColour("#cccccc")

    #-------------------------------------------------------------------------------
    def Button_MARKER(self,event):
        selection = event.GetEventObject().selection
        print("Button_SELECTION",selection)

        first_click = 0
        if self.marker_index != selection:
            if self.marker_table[selection] == []:
                first_click = 1

        self.marker_index=selection
        self.select_button(selection)

        if not first_click:
            name = "m%s" % (selection + 1)
            if self.marker_table[selection] == []:
                wx.MessageBox('No messages in \"%s\" ...' % name, 'Info', wx.OK | wx.ICON_INFORMATION)
            else:
                PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
                if PageIndex:
                    self.notebook.SetSelection(PageIndex - 1)
                else:
                    self.marker_table[selection].sort()
                    struct_list = []
                    for spe in self.marker_table[selection]:
                        if spe in self.content.keys():
                            struct_list.append(self.content[spe])


                    sorted_list = sorted(struct_list, key=lambda k: (k['FA'], k['NL']))

                    attrib_list = [""]*len(sorted_list)
                    for i in range(0,len(sorted_list)):
                        struct = sorted_list[i]
                        name_reduced = bota.ReduceName(struct["NL"])
                        if os.path.exists(os.path.join(self.options.paths.img,"photos",name_reduced)):
                            attrib_list[i] = "#1F7A1F"

                    self.selection_panels[selection] = FilteredPanel(self,sorted_list,attrib_list)
                    self.notebook.AddPage(self.selection_panels[selection], name, True)
                    PageIndex = self.notebook.GetSelection()
                    self.notebook.SetPageTextColour(PageIndex,'#669900')

    #-------------------------------------------------------------------------------
    def onCbSelect(self,event):
        self.filter_cb.SetBackgroundColour("#99ff66")
        event.Skip()

    #-------------------------------------------------------------------------------
    def onTextEntered(self,event):
        self.filter_cb.SetBackgroundColour("#99ff66")
        event.Skip()

    #-------------------------------------------------------------------------------
    def onFilterTextEnter(self,event):

        import unicodedata

        s = self.filter_cb.GetValue()
        flags = {}

        re_notes = re.compile('(^| )\$notes',re.U)
        re_obs = re.compile('(^| )\$obs',re.U)
        re_dept = re.compile('^| \(\$dept=([0-9,]*)\)',re.U)

        if re_notes.search(s):
            s = re_notes.sub('',s,re.U)
            flags['notes'] = 1

        if re_obs.search(s):
            s = re_obs.sub('',s,re.U)
            flags['obs'] = 1


        if re_dept.search(s):
            dept = re_dept.findall(s)[-1]
            if dept != '':
                flags['dept'] = dept.split(',')
                s = re_dept.sub('',s)
                print(flags['dept'])

        search_s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
        search_p = [p for p in re.split(" |\\\"(.*?)\\\"|'.*?'", search_s) if p and p.strip()]


        self.filter_cb.SetValue("")
        print("onFilterTextEnter",search_s)

        filtered_struct_list = []

        for fam in self.table.keys():
            #print("fam={}".format(fam))
            for gen in self.table[fam].keys():
                #print("gen={}".format(gen))
                for nl in self.table[fam][gen]:
                    #print(nl)
                    struct = self.content[nl]
                    s=""
                    for key in struct.keys():
                        if isinstance(struct[key],unicode) or isinstance(struct[key],str):
                            #print "string",struct[key]
                            s += struct[key]
                        elif isinstance(struct[key],list):
                            s += ''.join(struct[key])
                            #print "list"
                        #print "s",s

                    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

                    found = 1
                    for exp in search_p:
                        if not re.search(exp,s,re.I):
                            found = 0
                            break

                    if found:
                        handled = 0
                        if 'notes' in flags:
                            note_filename = os.path.join(options.paths.meta,"notes",struct["N."]+".txt")
                            if os.path.exists(note_filename):
                                filtered_struct_list.append(struct)
                            handled = 1

                        if 'obs' in flags:
                            obs_filename = os.path.join(options.paths.meta,"obs",struct["N."]+".csv")
                            if os.path.exists(obs_filename):
                                filtered_struct_list.append(struct)
                            handled = 1

                        if 'dept' in flags:
                            handled = 1
                            dept_match = 0
                            for d in flags['dept']:
                                if '1' in struct['chorodep'] and d in struct["chorodep"]["1"]:
                                    dept_match = 1
                                    break
                            if dept_match:
                                filtered_struct_list.append(struct)

                        if handled == 0:
                            filtered_struct_list.append(struct)


        sorted_list = sorted(filtered_struct_list, key=lambda k: (k['FA'], k['NL']))
        if len(filtered_struct_list) == 0:
            self.filter_cb.SetBackgroundColour("#ff5050")
        else:
            name = "{}".format(search_s)
            if 'dept' in flags:
                name += ' ({})'.format(','.join(flags['dept']))

            new_panel = FilteredPanel(self,sorted_list)
            self.notebook.AddPage( new_panel, name, True )
            PageIndex = self.notebook.GetSelection()
            self.notebook.SetPageTextColour(PageIndex,'#669900')

    #-------------------------------------------------------------------------------
    def onOpenNewTab(self,event):

        print("onOpenNewTab")
        print event.GetEventObject().struct_list
        name = event.GetEventObject().name

        sorted_list = sorted(event.GetEventObject().struct_list, key=lambda k: (k['FA'], k['NL']))
        if len(sorted_list) == 0:
            wx.MessageBox('Can not find ...' , wx.OK | wx.ICON_INFORMATION)
        else:
            print "else"

            name = "{}".format(name)
            new_panel = FilteredPanel(self,sorted_list) #parent, parent.notebook, name, grid, search_index_list, self, parent.options )
            self.notebook.AddPage( new_panel, name, True )
            PageIndex = self.notebook.GetSelection()
            self.notebook.SetPageTextColour(PageIndex,'#669900')

    #-------------------------------------------------------------------------------
    def onAdvancedSearch(self,event):

        name = "Advanced Search"
        PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
        if PageIndex:
            self.notebook.SetSelection(PageIndex - 1)
        else:
            panel = AdvancedSearchPanel(self)
            self.notebook.AddPage(panel, name, True)
            PageIndex = self.notebook.GetSelection()
            self.notebook.SetPageTextColour(PageIndex,'#669900')

    #-------------------------------------------------------------------------------
    def onRefresh(self,event):
        print("onRefresh")
        mkthumb.mkthumb(options)

    #-------------------------------------------------------------------------------
    def __Update(self,struct):
        print("MainApp.Update")
        self.content[struct["NL"]] = struct
        self.mainPanel.UpdateDesc()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

    options.config = ""

    i = 1
    while i < len(sys.argv):

        if re.match("-db",sys.argv[i]):
            options.paths.db = sys.argv[i+1]
            i+=1

        elif re.match("-img",sys.argv[i]):
            options.paths.img = sys.argv[i+1]
            i+=1

        elif re.match("-noconfig",sys.argv[i]):
            options.noconfig = 1

        elif re.match("-config",sys.argv[i]):
            i+=1
            options.config = sys.argv[i]

        elif re.match("-wxga",sys.argv[i]):
            options.wxga = 1

        i+=1

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    print("wxPython version: {}".format(wx.__version__))

    options = fldb.init() #OPTIONS()

    options.noconfig = 0
    options.wxga = 0
    options.debug = 1

    if os.getenv("HOME") == None:
        options.home  = os.getenv("HOMEPATH").decode(sys.stdout.encoding)
    else:
        options.home = os.getenv("HOME").decode(sys.stdout.encoding)

    options.wxflore = os.path.join(options.home,u".wxflore")
    if not os.path.exists(options.wxflore):
        os.makedirs(options.wxflore)

    #sys.path.append(options.wxflore)

    parse_argv(options)
    config.read(options)

    if options.paths.db == "":
        db_base_dir = os.path.join(options.paths.root,"db")

        if options.paths.meta == "":
            options.paths.meta = os.path.join(options.wxflore,'meta')
        print(db_base_dir)
        options.paths.db = os.path.join(db_base_dir,"flore.main")
        options.paths.coste = os.path.join(db_base_dir,"flore.coste")
        options.paths.telacol = os.path.join(db_base_dir,"flore.telacol")
        options.paths.seealso = os.path.join(db_base_dir,"see.also")
        options.paths.python = os.path.join(db_base_dir,"python")
        options.paths.cat = os.path.join(db_base_dir,"cat")
        sys.path.append(options.paths.python)

    # Create "meta/notes" if needed ...
    if options.paths.meta != "":
        notes_path = os.path.join(options.paths.meta,"notes")
        if not os.path.exists(notes_path):
            os.makedirs(notes_path)

    options.suffix='.'.join([x for x in options.paths.db.split(os.sep) if x !=""])

    print(os.sep)
    print('options.paths.db   : {}'.format(options.paths.db))
    print('options.paths.img  : {}'.format(options.paths.img))
    print('options.paths.meta : {}'.format(options.paths.meta))
    print(options.suffix)

    app = wx.App(redirect=False)
    MainApp(options)
    app.MainLoop()

    self.Show()
