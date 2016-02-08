# -*- coding: utf-8 -*-

import os
import functools
import codecs

import wx
import wx.aui
import wx.lib.agw.aui as aui

import bota
import wxeditor
import observations
from common import *


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
        self.Show()

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
class Panel(wx.Panel):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, parent, apps, options, colors):

        self.options = options
        self.colors = colors
        self.parent = parent
        self.apps = apps

        wx.Panel.__init__(self,parent,size=(-1,-1))
        self.SetBackgroundColour(self.colors.normal[1])

        self.descSizer = wx.BoxSizer(wx.VERTICAL)

    #-------------------------------------------------------------------------------
    def Button_SYN(self,event):
        print("Button_SYN")
        name = "Synonymes"
        PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
        if PageIndex:
            self.notebook.SetSelection(PageIndex - 1)
        else:
            panel = PanelSYN(self,self.struct)
            self.notebook.AddPage(panel, name, True)
            PageIndex = self.notebook.GetSelection()
            self.notebook.SetPageTextColour(PageIndex,'#669900')

    #-------------------------------------------------------------------------------
    def Button_BASEVEG(self,event):

        def filter_basveg_by_cat_id(cat_id):

            #table = self.apps.table
            content = self.apps.content
            filtered_struct_list = []

            for spe in content.keys():
                struct = content[spe]
                if 'ID.cat' in struct['baseflor'] and struct['baseflor']['ID.cat'] == cat_id:
                    filtered_struct_list.append(struct)

            sorted_list = sorted(filtered_struct_list, key=lambda k: (k['FA'], k['NL']))
            if len(filtered_struct_list) == 0:
                pass
            else:
                name = cat_id
                new_panel = FilteredPanel(self.apps,sorted_list)
                self.apps.notebook.AddPage( new_panel, name, True )
                PageIndex = self.apps.notebook.GetSelection()
                self.apps.notebook.SetPageTextColour(PageIndex,'#669900')


        #-------------------------------------------------------------------------------
        print("Button_baseveg")

        #name = "BaseVeg"
        name = self.struct['baseflor']['ID.cat']
        PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
        #print(self.notebook.GetSelection)

        if PageIndex:
            self.notebook.SetSelection(PageIndex - 1)
            #self.catminat_button=1
            filter_basveg_by_cat_id(self.struct['baseflor']['ID.cat'])

        else:
            #self.catminat_button=0
            panel = Panel_baseveg(self,self.struct,self.button_baseveg, self.options)
            self.notebook.AddPage(panel, name, True)
            PageIndex = self.notebook.GetSelection()
            self.notebook.SetPageTextColour(PageIndex,'#669900')

        #print("++++++++",self.catminat_button)
        print(len(self.apps.table.keys()))

    #-------------------------------------------------------------------------------
    def Button_OBS(self,event):
        print("Button_OBS")
        name = "Oberservations"
        PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
        if PageIndex:
            self.notebook.SetSelection(PageIndex - 1)
        else:
            panel = observations.ObsPanel(self, self.struct, self.obs_filename, self.button_obs)
            self.notebook.AddPage(panel, name, True)
            PageIndex = self.notebook.GetSelection()
            self.notebook.SetPageTextColour(PageIndex,'#669900')

    #-------------------------------------------------------------------------------
    def Button_NOTES(self,event):
        print("Button_NOTES")
        name = "Notes"
        PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
        if PageIndex:
            self.notebook.SetSelection(PageIndex - 1)
        else:
            panel = Panel_NOTES(self, self.struct,self.note_fn,self.button_note)
            self.notebook.AddPage(panel, name, True)
            PageIndex = self.notebook.GetSelection()
            self.notebook.SetPageTextColour(PageIndex,'#669900')

    #-------------------------------------------------------------------------------
    def OnObsUpdate(self,event):
        print("OnObspdate")
        if os.path.exists(self.obs_filename):
            self.button_obs.SetForegroundColour(self.colors.button.obs[0]) #"#101010")
            self.button_obs.SetBackgroundColour(self.colors.button.obs[1]) #"#33CCCC")
        else:
            self.button_obs.SetForegroundColour(self.colors.button.default[0]) #"#101010")
            self.button_obs.SetBackgroundColour(self.colors.button.default[1]) #"#D0D0D0")

    #-------------------------------------------------------------------------------
    def OnNoteUpdate(self,event):
        print("OnNoteUpdate")
        if os.path.exists(self.note_fn):
            self.button_note.SetForegroundColour(self.colors.button.note[0]) #"#101010")
            self.button_note.SetBackgroundColour(self.colors.button.note[1]) #"#33CCCC")
        else:
            self.button_note.SetForegroundColour(self.colors.button.default[0]) #"#101010")
            self.button_note.SetBackgroundColour(self.colors.button.default[1]) #"#D0D0D0")

    #-------------------------------------------------------------------------------
    def onNotebookClose(self,event):
        print("toto")

    #-------------------------------------------------------------------------------
    def UpdateHeader(self,struct):

        print("-----> wxflore.py / Description.UpdateHeader()")
        self.struct = struct

        n_ = struct["NL"].split("[")
        n1= n_[0]
        if len(n_) == 1:
            n2 = ""
        else:
            n2 = n_[1].replace("]","").strip()

        id = 400

        try:
            self.headerSizer.Clear(1)
            print("headerSizer.Clear()")
        except:
            self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.headerSizer.SetMinSize((-1,self.apps.size["THUMB.YMAX"]))

        self.headerRTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        self.headerRTC.SetBackgroundColour(self.colors.normal[1])
        self.headerRTC.SetForegroundColour(self.colors.normal[0])
        self.headerRTC.SetEditable(False)

        self.headerRTC.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)

        self.headerRTC.SelectNone()
        self.headerRTC.ChangeValue("")
        self.headerRTC.SelectNone()

#        self.headerRTC.BeginFontSize(self.apps.size["FONT.BIG"])
#        self.headerRTC.BeginAlignment(wx.TEXT_ALIGNMENT_RIGHT)
#        self.headerRTC.BeginTextColour(self.colors.fa[0])
#        self.headerRTC.BeginRightIndent(20)
#
#        self.headerRTC.WriteText("{}".format(struct["FA"]))
#        self.headerRTC.Newline()
#
#        self.headerRTC.EndRightIndent()
#        self.headerRTC.EndTextColour()
#        self.headerRTC.EndAlignment()
#        self.headerRTC.EndFontSize()


        self.headerRTC.BeginTextColour(self.colors.nl[0])
        self.headerRTC.BeginFontSize(self.apps.size["FONT.BIG"])
        self.headerRTC.BeginAlignment(wx.TEXT_ALIGNMENT_LEFT)
        #self.headerRTC.BeginLeftIndent(10)
        self.headerRTC.BeginBold()
        self.headerRTC.BeginItalic()

        self.headerRTC.WriteText(u"{}".format(n1))

        self.headerRTC.EndItalic()
        self.headerRTC.EndBold()
        #self.headerRTC.EndFontSize()

        #self.headerRTC.BeginFontSize(12)

        self.headerRTC.WriteText(u" {}".format(n2))

        #self.headerRTC.BeginFontSize(self.apps.size["FONT.BIG"])
        self.headerRTC.BeginTextColour("#808080")
        self.headerRTC.WriteText("     /     ")
        self.headerRTC.BeginTextColour(self.colors.fa[0])
        self.headerRTC.WriteText("{} ".format(struct["FA"]))
        self.headerRTC.EndTextColour()
        self.headerRTC.Newline()

        self.headerRTC.EndFontSize()
        self.headerRTC.BeginFontSize(12)
        self.headerRTC.EndFontSize()
        self.headerRTC.EndAlignment()
        self.headerRTC.EndTextColour()


        self.headerRTC.BeginAlignment(wx.TEXT_ALIGNMENT_LEFT)
        ##self.headerRTC.BeginLeftIndent(10)

        self.headerRTC.BeginFontSize(self.apps.size["FONT.BIG"])
        self.headerRTC.BeginTextColour(self.colors.nv[0])
        self.headerRTC.WriteText(u"{}\n".format(struct["NV"].replace(";",", ")))
        self.headerRTC.EndTextColour()
        self.headerRTC.EndFontSize()

        if "N.UK" in struct.keys() and struct["N.UK"] != "" and "UK" not in self.options.lang.hide:
            self.headerRTC.BeginFontSize(12)
            self.headerRTC.BeginTextColour("#cc6600")
            self.headerRTC.WriteText(struct["N.UK"].replace(";",", "))
            self.headerRTC.EndTextColour()
            self.headerRTC.EndFontSize()

        if "N.NL" in struct.keys() and struct["N.NL"] != "" and "NL" in self.options.lang.show:
            self.headerRTC.BeginFontSize(12)
            self.headerRTC.BeginTextColour("#6666ff")
            self.headerRTC.WriteText(struct["N.NL"].replace(";",", "))
            self.headerRTC.EndTextColour()
            self.headerRTC.EndFontSize()


        self.headerRTC.EndAlignment()
        ###self.headerRTC.EndLeftIndent()

        self.headerRTC.Newline()
        self.headerRTC.Newline()

        self.headerRTC.BeginTextColour(self.colors.normal[0])

        try:
            FL_col = struct["baseflor"]["FL.col"]
            self.headerRTC.WriteText("Fleur: ")
            first = 1
            for col in [x.strip() for x in FL_col.split(",")]:
                print col
                if first:
                    first = 0
                else:
                    self.headerRTC.WriteText(" ou ")

                self.headerRTC.BeginTextColour(self.colors.flower[col][0])
                self.headerRTC.WriteText(u"{}".format(col.upper()))
                self.headerRTC.EndTextColour()

            self.headerRTC.WriteText(u" / {}".format(struct["baseflor"]["FL.flo"]))
            self.headerRTC.WriteText(u" / {}".format(struct["baseflor"]["FL.inf"]))
            self.headerRTC.WriteText(u" / {}\n".format(struct["baseflor"]["FL.fru"]))

            self.headerRTC.WriteText(u"Sexualité: {}".format(struct["baseflor"]["FL.se"]))
            self.headerRTC.WriteText(u" / Ordre Maturation: {}".format(struct["baseflor"]["FL.mat"]))
            self.headerRTC.WriteText(u" / Dissemination: {}\n".format(struct["baseflor"]["FL.dis"]))


        except:
            pass

        try:
            self.headerRTC.Newline()
            self.headerRTC.WriteText(u"Ecologie: {} / {}\n".format(struct["baseflor"]["ECO.ch"],
                                                                   struct["baseflor"]["ECO.opt"]))
        except:
            pass

        try:
            self.headerRTC.WriteText(u"Lumière: {}".format(struct["baseflor"]["GRAD.L"]))
            self.headerRTC.WriteText(u", Humidité air: {}".format(struct["baseflor"]["GRAD.Ha"]))
            self.headerRTC.WriteText(u", Temp: {}".format(struct["baseflor"]["GRAD.T"]))
            self.headerRTC.WriteText(u", Conti: {}".format(struct["baseflor"]["GRAD.C"]))
        except:
            pass

        self.headerRTC.Newline()
        try:
            self.headerRTC.WriteText(u"pH: {}".format(struct["baseflor"]["GRAD.pH"]))
            self.headerRTC.WriteText(u", Humidité: {}".format(struct["baseflor"]["GRAD.He"]))
            self.headerRTC.WriteText(u", Texture: {}".format(struct["baseflor"]["GRAD.tex"]))
            self.headerRTC.WriteText(u", Nutriments: {}".format(struct["baseflor"]["GRAD.tro"]))
            self.headerRTC.WriteText(u", Salinité: {}".format(struct["baseflor"]["GRAD.sal"]))
            self.headerRTC.WriteText(u", Matière organique: {}".format(struct["baseflor"]["GRAD.MO"]))
        except:
            pass

        try:
            tl = struct["baseflor"]["TL"].strip().capitalize()
            if tl != "":
                self.headerRTC.Newline()
                self.headerRTC.WriteText(u"{}".format(tl))
                self.headerRTC.WriteText(u", H. maxi: {} m".format(struct["baseflor"]["Hmax"]))
        except:
            pass

        try:
            #print("struct[chorodep]",struct["chorodep"])
            pres = ", ".join(struct["chorodep"]["1"])
            rar = struct["chorodep"]["rar"]
            self.headerRTC.Newline()
            self.headerRTC.WriteText(u"Pres ({}) : {}".format(rar,pres.replace(";",", ")))
        except:
            pass

#        self.headerRTC.Newline()
#        for label in ["LABEL1","LABEL2","LABEL3","LABEL4"]:
#            self.headerRTC.BeginTextColour("#6699ff")
#            #self.headerRTC.SetForegroundColour("#808000")#            self.headerRTC.WriteText("{}".format(label))
#            self.headerRTC.WriteText(" ")

        self.headerRTC.SetBackgroundColour(self.colors.normal[1])
        self.headerRTC.SetForegroundColour(self.colors.normal[0])

        self.headerSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.tagsSizer =  wx.BoxSizer(wx.HORIZONTAL)
        self.scrolledTagPanel = wx.lib.scrolledpanel.ScrolledPanel(self,size=(-1,28))
        self.scrolledTagPanel.SetBackgroundColour(self.colors.normal[1])
        self.tagFlag = 0

        self.protSizer =  wx.BoxSizer(wx.HORIZONTAL)
        self.scrolledProtPanel = wx.lib.scrolledpanel.ScrolledPanel(self,size=(-1,28))
        self.scrolledProtPanel.SetBackgroundColour(self.colors.normal[1])
        self.protFlag = 0


        # Tags
        #--------------
        if "tags" in struct.keys():
            for tag in struct["tags"]:

                self.tagsSizer.Add((5,-1))

                button = wx.Button(self.scrolledTagPanel, wx.ID_ANY, u" {} ".format(tag),
                                   wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
                button.SetForegroundColour("#600060")
                button.SetBackgroundColour("#6699ff")
                self.tagsSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
                self.tagFlag = 1

        self.protSizer.Add((5,-1))

        # Catergories
        #-------------
        if "cat" in struct.keys():
            for cat in struct["cat"]:
                button = wx.Button(self.scrolledTagPanel, wx.ID_ANY,
                                   u" {} ".format(self.apps.button_config["cat"]["names"][cat]),
                                   wx.DefaultPosition, (-1,-1),
                                   style=wx.BU_EXACTFIT)
                try:
                    button.SetForegroundColour(self.apps.button_config["cat"]["colors"][cat][0])
                    button.SetBackgroundColour(self.apps.button_config["cat"]["colors"][cat][1])
                except:
                    pass


                self.tagsSizer.Add((5,-1))
                self.tagsSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
                self.tagFlag = 1
                print(" ======== if tagflag / Category")

                self.apps.button_list["cat"].append(cat)


        # Red List Status
        #-----------------
        if "redlist" in struct.keys():

            rl = struct["redlist"]
            try:
                button = wx.Button(self.scrolledProtPanel, wx.ID_ANY,
                                   u" {} ".format(self.apps.button_config["redlist"]["names"][rl]),
                                   wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
                button.SetForegroundColour(self.apps.button_config["redlist"]["colors"][rl][0])
                button.SetBackgroundColour(self.apps.button_config["redlist"]["colors"][rl][1])
                self.protSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
                self.protFlag = 1
            except:
                print("## WARNING ## : Status error = {}".format(rl))
                pass

        # Red List Status
        #-----------------
        if struct["prot.nat"] != []:

            button = wx.Button(self.scrolledProtPanel, wx.ID_ANY, u"France Métropole",
                               wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
            button.SetForegroundColour("#660033")
            button.SetBackgroundColour("#ff0066")
            self.protSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
            self.protFlag = 1

        # Regional Protections
        #----------------------
        prot_colors={u'Languedoc-Roussillon':[-1,-1],
                     u'Basse-Normandie':[-1,-1],
                     u'Lorraine':[-1,-1],
                     u'Poitou-Charentes':[-1,-1],
                     u'Nord-Pas-de-Calais':[-1,-1],
                     u'Pays-de-la-Loire':[-1,-1],
                     u'Centre':[-1,-1],
                     u'Bretagne':[-1,-1],
                     u'Bourgogne':[-1,-1],
                     u'Aquitaine':[-1,-1],
                     u'Auvergne':[-1,-1],
                     u'Alsace':[-1,-1],
                     u'IDF':[-1,-1],
                     u'Corse':[-1,-1],
                     u'Franche-Comte':[-1,-1],
                     u'Limousin':[-1,-1],
                     u'Rhone-Alpes':[-1,-1],
                     u'PACA':[-1,-1],
                     u'Haute-Normandie':[-1,-1],
                     u'Picardie':[-1,-1],
                     u'Champagne-Ardenne':[-1,-1],
                     u'Midi-Pyrenees':["#99ff33",-1]}

        prot_prio = [u'Midi-Pyrenees',u'Aquitaine']

        import region
        prot_pattern = [[prot for prot in struct["prot.reg"] if prot in prot_prio],
                        [prot for prot in struct["prot.reg"] if prot not in prot_prio]]

        print(struct["prot.reg"])
        print(prot_pattern)

        first = 1
        for i in range(0,2):
            for prot in prot_pattern[i]:
                if first:
                    first = 0
                    statictext = wx.StaticText(self.scrolledProtPanel, -1, u" RÉGIONS:")
                    statictext.SetForegroundColour("#F0F0F0")
                    self.protSizer.Add((5,-1))
                    self.protSizer.Add(statictext, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, border=0)
                    self.protSizer.Add((5,-1))

                try:
                    button = wx.Button(self.scrolledProtPanel,
                                       wx.ID_ANY,
                                       u" {} ".format(region.table[prot][0]),style=wx.BU_EXACTFIT) #.decode("utf8")))

                    if prot_colors[prot][0] != -1:
                        button.SetForegroundColour(prot_colors[prot][0])
                    else:
                        button.SetForegroundColour("#ffff99")

                    if prot_colors[prot][1] != -1:
                        button.SetBackgroundColour(prot_colors[prot][1])
                    else:
                        button.SetBackgroundColour("#202020")

                    self.protSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
                    self.protFlag = 1
                except IOError:
                    print("## WARNING ## : Protection Status error")

        # Departemental protection
        #--------------------------
        prot_prio = []
        prot_pattern = [[prot for prot in struct["prot.dep"] if prot in prot_prio],
                        [prot for prot in struct["prot.dep"] if prot not in prot_prio]]

        print(struct["prot.dep"])
        print(prot_pattern)

        first = 1
        for i in range(0,2):
            for prot in prot_pattern[i]:
                if first:
                    first = 0
                    statictext = wx.StaticText(self.scrolledProtPanel, -1, u" DEPT:")
                    statictext.SetForegroundColour("#F0F0F0")
                    self.protSizer.Add((5,-1))
                    self.protSizer.Add(statictext, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, border=0)
                    self.protSizer.Add((5,-1))

                try:
                    button = wx.Button(self.scrolledProtPanel, wx.ID_ANY, u" {} ".format(prot),style=wx.BU_EXACTFIT) #.decode("utf8")))

                    button.SetForegroundColour("#FF9966")
                    button.SetBackgroundColour("#202020")

                    self.protSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
                    self.protFlag = 1
                except IOError:
                    print("## WARNING ## : Protection Status error")

        # See Also ...
        #--------------
        self.seealsoSizer =  wx.BoxSizer(wx.HORIZONTAL)
        if "seealso" in struct.keys():

            statictext = wx.StaticText(self, -1, "Voir aussi:")
            self.seealsoSizer.Add((5,-1))
            self.seealsoSizer.Add(statictext, 0, wx.ALIGN_LEFT|wx.EXPAND, border=0)
            self.seealsoSizer.Add((5,-1))

            short_name =  struct["NL"].split("[")[0].strip()
            struct_t = []
            for seealso in struct["seealso"]:
                for fam in self.apps.table.keys():
                    for gen in self.apps.table[fam].keys():
                        for nl in self.apps.table[fam][gen]:
                            if seealso == self.apps.content[nl]["ID.tela"]:
                                name = self.apps.content[nl]["NL"].split("[")[0].strip()
                                tela_id = self.apps.content[nl]["ID.tela"]
                                struct_t.append(self.apps.content[nl])
                                break
                if seealso != struct["ID.tela"]:
                    button = wx.Button(self, id, " {} ".format(name), wx.DefaultPosition, (-1,-1), wx.BU_EXACTFIT )
                    button.SetForegroundColour("#FfFfFf")
                    button.SetBackgroundColour("#85adad") #"#00CC99")
                    button.struct_list = struct_t
                    button.name = "See also: {}".format(short_name)

                    wx.EVT_BUTTON( self, id, self.apps.onOpenNewTab)

                    id+=1
                    self.seealsoSizer.Add(button,0,wx.ALL)
                    #self.tagFlag = 1
                    print(" ======== if tagflag / ID.tela .{}.".format(seealso))



        # COSTE Illustration
        #--------------------
        coste_ill = os.path.join(self.options.paths.img,u"illustrations",u"Coste",u"{}.png".format(struct["ID.coste"]))
        #print("COSTE",coste_ill)
        if os.path.exists(coste_ill):
            print(coste_ill)
            locale = wx.Locale(wx.LANGUAGE_DEFAULT)
            image = wx.Image(coste_ill, wx.BITMAP_TYPE_ANY)
            #image = image.Scale(200,250, wx.IMAGE_QUALITY_HIGH)
            image = image.Scale(self.apps.size["THUMB.XMAX"],
                                self.apps.size["THUMB.YMAX"], wx.IMAGE_QUALITY_HIGH)
            imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))
            imageBitmap.Bind(wx.EVT_LEFT_DOWN, functools.partial(self.onPhotoClick,coste_ill))
            self.headerSizer.Add(imageBitmap,0,wx.ALL)

        elif 1:
            name_reduced = bota.ReduceName(struct["NL"])
            thumb_dir = os.path.join(self.options.paths.img,"photos",name_reduced)
            thumb_file = os.path.join(thumb_dir,name_reduced+'.00.jpg')
            if os.path.exists(thumb_file):
                locale = wx.Locale(wx.LANGUAGE_DEFAULT)
                image = wx.Image(thumb_file, wx.BITMAP_TYPE_JPEG)

                # scale the image, preserving the aspect ratio
                W = image.GetWidth()
                H = image.GetHeight()

                h = self.apps.size["THUMB.YMAX"]
                w = W*h/H

                image = image.Scale(w, h, wx.IMAGE_QUALITY_HIGH)

                imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))
                imageBitmap.Bind(wx.EVT_LEFT_DOWN, functools.partial(self.onPhotoClick,coste_ill))
                self.headerSizer.Add(imageBitmap,0,wx.ALL)
        else:
            self.headerSizer.Add((240,-1))


        #self.headerSizer.Layout()
        self.headerSizer1.Add(self.headerRTC,1,wx.ALIGN_LEFT|wx.EXPAND,4)

        if hasattr(self,"seealsoSizer"):
            self.headerSizer1.Add(self.seealsoSizer,0,wx.ALIGN_LEFT)

        if self.tagFlag:
            self.scrolledTagPanel.SetupScrolling(True,True)
            #self.SetAutoLayout(1)
            self.scrolledTagPanel.SetSizer(self.tagsSizer)
            self.headerSizer1.Add(self.scrolledTagPanel,0,wx.ALIGN_LEFT|wx.EXPAND)

        if self.protFlag:
            self.scrolledProtPanel.SetupScrolling(True,True)
            #self.SetAutoLayout(1)
            self.scrolledProtPanel.SetSizer(self.protSizer)
            self.headerSizer1.Add(self.scrolledProtPanel,0,wx.ALIGN_LEFT|wx.EXPAND)

        self.headerSizer.Add(self.headerSizer1,1,wx.ALIGN_LEFT|wx.EXPAND)

        self.headerSizer.Layout()

        #print(u"[ {} ]".format(struct["REF"]))
        print(u"[ {} ]".format(struct["FN"]))
        print("## END ## DescriptionPanel.UpdateHeader()")

    #-------------------------------------------------------------------------------
    def onPhotoClick(self,coste_ill,evt):
        print "onPhotoClick",coste_ill
        import wxpict
        viewer = wxpict.ViewerFrame(self.parent,[coste_ill],0)

    #-------------------------------------------------------------------------------
    def RightClick(self,event):

        menu = wx.Menu()

        self.popupID_COPY = wx.NewId()
        self.popupID_COPY_NL_FA_NV_UK = wx.NewId()
        self.popupID_COPY_DIASPORA_names = wx.NewId()
        self.popupID_COPY_DIASPORA_desc = wx.NewId()
        self.popupID_COPY_DIASPORA_baseveg = wx.NewId()
        self.popupID_COPY_NL_FA_NV = wx.NewId()
        self.popupID_COPY_NL_FA = wx.NewId()
        self.popupID_COPY_ID_TELA = wx.NewId()
        self.popupID_COPY_ID_INPN = wx.NewId()

        self.popupID_PROT = wx.NewId()

        self.popupID_COPY_URL_TELA = wx.NewId()
        self.popupID_COPY_URL_INPN = wx.NewId()
        self.popupID_COPY_URL_FCNB = wx.NewId()

        self.popupID_EDIT_MAIN = wx.NewId()
        self.popupID_EDIT_COSTE = wx.NewId()

        self.popupID_EXPORT = wx.NewId()

        menu.Append(self.popupID_COPY, "Copy (selected text)")
        menu.AppendSeparator()
        menu.Append(self.popupID_COPY_NL_FA_NV_UK, "Copy NL (FA) + NV + N.UK")
        menu.Append(self.popupID_COPY_NL_FA_NV, "Copy NL (FA) + NV")
        menu.Append(self.popupID_COPY_NL_FA, "Copy NL (FA)")
        menu.AppendSeparator()
        menu.Append(self.popupID_COPY_DIASPORA_names, 'Diaspora* : copy NL + (FA) + Names')
        menu.Append(self.popupID_COPY_DIASPORA_desc, 'Diaspora* : copy Description')
        menu.Append(self.popupID_COPY_DIASPORA_baseveg, 'Diaspora* : copy BaseVeg')
        menu.AppendSeparator()
        menu.Append(self.popupID_COPY_ID_TELA, "Copy ID TELA")
        menu.Append(self.popupID_COPY_ID_INPN, "Copy ID INPN")
        menu.AppendSeparator()
        menu.Append(self.popupID_PROT, "Copy Protection Status")
        menu.AppendSeparator()
        menu.Append(self.popupID_COPY_URL_TELA, "Copy URL for 'TELA'")
        menu.Append(self.popupID_COPY_URL_INPN, "Copy URL for 'INPN'")
        menu.Append(self.popupID_COPY_URL_FCNB, "Copy URL for 'FCNB'")
        menu.AppendSeparator()

        menu.Append(self.popupID_EDIT_MAIN, "Edit this sheet")

        if "FN.coste" in self.struct.keys():
            menu.Append(self.popupID_EDIT_COSTE, "Edit Coste Desc.")

        menu.AppendSeparator()
        menu.Append(self.popupID_EXPORT, "Export to TXT")

        self.Bind(wx.EVT_MENU, self.RightClickMenu)

        self.PopupMenu(menu)
        menu.Destroy()

    #-------------------------------------------------------------------------------
    def RightClickMenu(self,event):
        print("RightClickMenu")
        s=""
        if event.GetId() == self.popupID_EXPORT:
            text = build_text_to_export(self.struct)
            TextFrame(text,self)

        elif event.GetId() == self.popupID_EDIT_MAIN:
            ed = wxeditor.MainWindow(self,
                                     u"Main description : {}".format(self.struct["nl"]),
                                     self.struct["FN"],
                                     self.colors)
            ed.ShowModal()

            struct = fldb.parse_file(self.struct["FN"],self.struct["N."],self.options)

            self.parent.Refresh(struct)
            #self.appq.Update(struct)
            # iiiiiiiii

        elif event.GetId() == self.popupID_EDIT_COSTE:
            ed = wxeditor.MainWindow(self,
                                     u"COSTE description : {}".format(self.struct["nl"]),
                                     self.struct["FN.coste"],
                                     self.colors)
            ed.ShowModal()

        elif event.GetId() == self.popupID_COPY:
            self.headerRTC.Copy()

        elif event.GetId() == self.popupID_COPY_NL_FA_NV_UK:
            nl = self.struct["NL"].replace("["," ").replace("]","") #.encode("utf-8")
            s = u"{} / {}".format(nl,self.struct["FA"])
            try:
                s+=u"\nNom(s) français: {}".format(self.struct["NV"].replace(";",",")) #.encode("utf-8"))
            except:
                pass

            try:
                s+=u"\nNom(s) anglais: {}".format(self.struct["N.UK"].replace(";",","))
            except:
                pass

        elif event.GetId() == self.popupID_COPY_DIASPORA_names:
            #nl = self.struct["NL"].replace("["," ").replace("]","") #.encode("utf-8")
            nl1, nl2 = re.findall("(.*)\[(.*)\]",self.struct['NL'])[0]
            nl1 = nl1.strip()
            nl2 = nl2.strip()

            s = u"***{}***  {}  /  **{}**".format(nl1,nl2,self.struct["FA"])
            try:
                s+=u"\n**Nom(s) français:** {}".format(self.struct["NV"].replace(";",",")) #.encode("utf-8"))
            except:
                pass

            try:
                s+=u"\n**English:** {}".format(self.struct["N.UK"].replace(";",","))
            except:
                pass

            try:
                s+=u"\n**Nederlands:** {}".format(self.struct["N.NL"].replace(";",","))
            except:
                pass

            try:
                s+=u"\n**Deutsch:** {}".format(self.struct["N.DE"].replace(";",","))
            except:
                pass

            try:
                s+=u"\n**Italiano:** {}".format(self.struct["N.IT"].replace(";",","))
            except:
                pass

            try:
                s+=u"\n**Español:** {}".format(self.struct["N.ES"].replace(";",","))
            except:
                pass

            s+='\n\n'
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
            s+='#{} '.format(nl1.split()[0].lower())
            s+='#{} '.format(self.struct['FA'].lower())

        elif event.GetId() == self.popupID_COPY_DIASPORA_desc:
            s = build_text_to_export(self.struct,True)
            print(s)

        elif event.GetId() == self.popupID_COPY_DIASPORA_baseveg:
            s = build_baseveg_string(self.struct,self.options,True)
            print(s)

        elif event.GetId() == self.popupID_COPY_NL_FA_NV:
            nl = self.struct["NL"].replace("["," ").replace("]","") #.encode("utf-8")
            s = u"{} / {}".format(nl,self.struct["FA"])
            try:
                s+=u"\nNom(s) français: {}".format(self.struct["NV"].replace(";",",")) #.encode("utf-8"))
            except:
                pass

        elif event.GetId() == self.popupID_COPY_NL_FA:
            nl = self.struct["NL"].replace("["," ").replace("]","") #.encode("utf-8")
            s = u"{} / {}".format(nl,self.struct["FA"])

        elif event.GetId() == self.popupID_COPY_ID_TELA:
            s = "{}".format(self.struct["ID.tela"])

        elif event.GetId() == self.popupID_COPY_ID_INPN:
            s = "{}".format(self.struct["ID.inpn"])

        elif event.GetId() == self.popupID_PROT:
            s=""

            if self.struct["prot.nat"] != []:
                s+="Protection Nationale"

            try:
                rl = " (RL '{}')".format(self.apps.button_config["redlist"]["names"][self.struct["redlist"]])
            except:
                rl = ""

            s+=rl
            s+="\n"

            s_ = []
            for prot in self.struct["prot.reg"]:
                s_.append(prot)
            if s_ != []:
                s+="Protection(s) Régionale(s) : {}\n".format(", ".join(s_))

            s_ = []
            for prot in self.struct["prot.dep"]:
                s_.append(prot)
            if s_ != []:
                s+="Protection Départementale : {}\n".format(", ".join(s_))

            print(s)


        elif event.GetId() == self.popupID_COPY_URL_TELA:
            s = format_url_tela.format(self.struct["ID.tela"])

        elif event.GetId() == self.popupID_COPY_URL_INPN:
            s = format_url_inpn.format(self.struct["ID.inpn"])

        elif event.GetId() == self.popupID_COPY_URL_FCNB:
            s = format_url_fcnb.format(self.struct["ID.inpn"])

        if s != "":
            clipdata = wx.TextDataObject()
            clipdata.SetText(s)
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()

    #-------------------------------------------------------------------------------
    def UpdateDesc(self,struct):

        if self.options.debug:
            print("=====> wxflore.py / Description.UpdateDesc()")

        #self.descRTC.Clear()
        big_font = 11
        small_font = 10

        self.descSizer.Clear(1)
        #self.descSizer = wx.BoxSizer(wx.VERTICAL)

        print("DescriptionPanel.UpdateDesc() -> call to UpdateHeader()")
        self.UpdateHeader(struct)
        print("DescriptionPanel.UpdateDesc() -> return from UpdateHeader()")

        self.descRTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        self.descRTC.SetBackgroundColour(self.colors.normal[1])
        self.descRTC.SetForegroundColour(self.colors.normal[0])
        self.descRTC.SetEditable(False)

        self.descRTC.BeginTextColour(self.colors.normal[0])

        #font = wx.FFont(12, wx.FONTFAMILY_DEFAULT, face='Arial', flags=wx.FONTFLAG_STRIKETHROUGH)
        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.descRTC.BeginFont(font)

        self.descRTC.BeginFontSize(big_font)
        self.descRTC.BeginBold()
        self.descRTC.WriteText("Description:")
        self.descRTC.Newline()
        self.descRTC.EndFontSize()
        self.descRTC.EndBold()

        self.descRTC.BeginFontSize(small_font)
        self.descRTC.BeginLeftIndent(50)

        if struct["DS"] != []:
            for l in struct["DS"]:
                self.descRTC.WriteText(u"- {}\n".format(l))

        elif "telacol.DS" in struct.keys() and struct["telacol.DS"] != []:

            for l in struct["telacol.DS"]:
                if re.match(r"Identification|Générale|NB |\-\s*$",l,re.UNICODE):
                    self.descRTC.WriteText(u"{}\n".format(l))
                else:
                    self.descRTC.WriteText(u"- {}\n".format(l))

        #self.descRTC.EndLeftIndent()
        self.descRTC.EndFontSize()

        if "HB" in struct.keys():
            self.descRTC.Newline()
            self.descRTC.BeginFontSize(big_font)
            self.descRTC.BeginBold()
            self.descRTC.WriteText("Ecologie:\n")
            self.descRTC.EndBold()
            self.descRTC.EndFontSize()

            self.descRTC.BeginFontSize(small_font)
            self.descRTC.BeginLeftIndent(50)
            self.descRTC.WriteText(u"- {}\n".format(struct["HB"]))
            self.descRTC.EndFontSize()
            self.descRTC.EndLeftIndent()


        if "ZO" in struct.keys():
            self.descRTC.WriteText("\n")

            self.descRTC.BeginFontSize(big_font)
            self.descRTC.BeginBold()
            self.descRTC.WriteText("Zone Géographique:\n")
            self.descRTC.EndBold()
            self.descRTC.EndFontSize()

            self.descRTC.BeginFontSize(small_font)
            self.descRTC.BeginLeftIndent(50)
            self.descRTC.WriteText(u"- {}\n".format(struct["ZO"]))
            self.descRTC.EndFontSize()
            self.descRTC.EndLeftIndent()


        if "FL" in struct.keys():
            self.descRTC.WriteText("\n")

            self.descRTC.BeginFontSize(big_font)
            self.descRTC.BeginBold()
            self.descRTC.WriteText(u"Floraison:")
            self.descRTC.EndBold()
            self.descRTC.EndFontSize()

            self.descRTC.BeginFontSize(small_font)
            self.descRTC.WriteText("    ")
            self.descRTC.WriteText(u"{}\n".format(struct["FL"]))
            self.descRTC.EndFontSize()


        ref_coste = u""
        if "ID.coste" in struct.keys():
            if struct["ID.coste"] != "":
                ref_coste +=u"N°{}".format(struct["ID.coste"])
        if "N.coste" in struct.keys():
            ref_coste +=u"  -  {}".format(struct["N.coste"])

        if ref_coste != "":
            self.descRTC.WriteText("\n")

            self.descRTC.BeginFontSize(big_font)
            self.descRTC.BeginBold()
            self.descRTC.WriteText("Ref. Coste:")
            self.descRTC.EndBold()
            self.descRTC.EndFontSize()

            self.descRTC.BeginFontSize(small_font)
            self.descRTC.WriteText("    ")
            self.descRTC.WriteText(u"{}\n".format(ref_coste))
            self.descRTC.EndFontSize()

        if "REF.wiki.fr" in struct.keys():
            self.descRTC.WriteText("\n")

            self.descRTC.BeginFontSize(big_font)
            self.descRTC.BeginBold()
            self.descRTC.WriteText("Wikipedia:")
            self.descRTC.EndBold()
            self.descRTC.EndFontSize()
            self.descRTC.BeginFontSize(small_font)
            self.descRTC.WriteText("    ")
            self.descRTC.WriteText("{}\n".format(struct["REF.wiki.fr"]))
            self.descRTC.EndFontSize()

        if "ID.inpn" in struct.keys():
            self.descRTC.BeginFontSize(big_font)
            self.descRTC.BeginBold()
            self.descRTC.WriteText("INPN:")
            self.descRTC.EndBold()
            self.descRTC.EndFontSize()

            self.descRTC.BeginFontSize(small_font)
            self.descRTC.WriteText("    ")
            self.descRTC.WriteText("http://inpn.mnhn.fr/espece/cd_nom/{}\n".format(struct["ID.inpn"]))
            self.descRTC.EndFontSize()

        if "ID.tela" in struct.keys():
            self.descRTC.BeginFontSize(big_font)
            self.descRTC.BeginBold()
            self.descRTC.WriteText("Tela:")
            self.descRTC.EndBold()
            self.descRTC.EndFontSize()

            self.descRTC.BeginFontSize(small_font)
            self.descRTC.WriteText("    ")
            self.descRTC.WriteText("http://www.tela-botanica.org/bdtfx-nn-{}-synthese".format(struct["ID.tela"]))

            self.descRTC.EndFontSize()

        # DescriptionPanel Toolbar
        #----------------------------------
        # self.descTB = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
        # wx.TB_FLAT | wx.TB_NODIVIDER)

        self.descTB_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.descTB = wx.Panel(self,size=(-1,35))

        self.descTB.SetBackgroundColour(self.colors.normal[1])
        self.descTB.SetForegroundColour(self.colors.normal[0])

        id = wx.NewId()
        button = wx.Button(self.descTB, id, "Synonymes", wx.DefaultPosition, (-1,-1)) #, wx.BU_EXACTFIT )
        button.SetForegroundColour(self.colors.button.default[0])
        button.SetBackgroundColour(self.colors.button.default[1])
        # self.descTB.AddControl(button)
        self.descTB_sizer.Add(button,0,wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM,border=2)
        wx.EVT_BUTTON( self, id, self.Button_SYN)
        id+=1

        # Button OSERVATIONS
        #-------------------------------------------------------------------------------
        self.button_obs = wx.Button(self.descTB, id, "Observations", wx.DefaultPosition, (-1,-1))
        self.button_obs.SetForegroundColour(self.colors.button.default[0])
        self.button_obs.SetBackgroundColour(self.colors.button.default[1])
        self.descTB_sizer.Add(self.button_obs,0,wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM,border=2)

        self.obs_filename = ""
        if self.options.paths.meta != "":
            if not os.path.exists(os.path.join(self.options.paths.meta,"obs")):
                os.makedirs(os.path.join(self.options.paths.meta,"obs"))

            self.obs_filename = os.path.join(self.options.paths.meta,"obs",struct["N."]+".csv")
            print(self.obs_filename)
            if os.path.exists(self.obs_filename):
                self.button_obs.SetForegroundColour(self.colors.button.obs[0])
                self.button_obs.SetBackgroundColour(self.colors.button.obs[1])

            wx.EVT_BUTTON( self, id, self.Button_OBS)
            self.Bind(EVT_OBS_UPDATE_ID, self.OnObsUpdate)
            id+=1


        # Button NOTES
        #-------------------------------------------------------------------------------
        self.button_note = wx.Button(self.descTB, id, "Notes", wx.DefaultPosition, (-1,-1))
        self.button_note.SetForegroundColour(self.colors.button.default[0])
        self.button_note.SetBackgroundColour(self.colors.button.default[1])
        self.descTB_sizer.Add(self.button_note,0,wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM,border=2)

        self.note_fn = ""
        if self.options.paths.meta != "":
            self.note_fn = os.path.join(self.options.paths.meta,"notes",struct["N."]+".txt")
            print(self.note_fn)
            if os.path.exists(self.note_fn):
                self.button_note.SetForegroundColour(self.colors.button.note[0])
                self.button_note.SetBackgroundColour(self.colors.button.note[1])

            wx.EVT_BUTTON( self, id, self.Button_NOTES)
            self.Bind(EVT_NOTE_UPDATE_ID, self.OnNoteUpdate)
            id+=1

        # ID Catminat
        #--------------
        if 'ID.cat' in self.struct['baseflor'] and self.struct['baseflor']['ID.cat'] != '':

            self.tagsSizer.Add((5,-1))
            #self.button_baseveg = wx.Button(self.scrolledTagPanel,
            self.button_baseveg = wx.Button(self.descTB, id,
                                            u" Cat: {} ".format(self.struct['baseflor']['ID.cat']),
                                            wx.DefaultPosition, (-1,-1)) #, style=wx.BU_EXACTFIT)
            self.button_baseveg.SetForegroundColour("#000000")
            #self.button_note.SetForegroundColour(self.colors.button.note[0])
            #button.SetBackgroundColour("#6699ff")
            self.button_baseveg.SetBackgroundColour("#ffffff")
            self.descTB_sizer.Add(self.button_baseveg,0,wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM,border=2)

            wx.EVT_BUTTON( self, id, self.Button_BASEVEG)
            id+=1


        self.descTB.SetSizer(self.descTB_sizer)
        self.descTB.Layout()

        # Description Notebook
        self.notebook = aui.AuiNotebook(self) #,"True",aui.AUI_NB_HIDE_ON_SINGLE_TAB) #,aui.AUI_NB_CLOSE_ON_ALL_TABS)

        tabArt = aui.ChromeTabArt()
        tabArt.SetDefaultColours(wx.Colour(20, 20, 20))
        #print(dir(tabArt))
        self.notebook.SetArtProvider(tabArt)
        #self.notebook.SetAGWFlags(self.aui_mgr.GetAGWFlags()|wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE )
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onNotebookClose)

        self.notebook.AddPage(self.descRTC, "Description (COSTE)", True)
        PageIndex = self.notebook.GetSelection()
        self.notebook.SetPageTextColour(PageIndex,'#669900')

        #self.scrolled_header = wx.lib.scrolledpanel.ScrolledPanel(self,size=(-1,-1))
        #self.scrolled_header.SetupScrolling(True,True)
        #self.scrolled_header.SetSizer(self.headerSizer)

        self.descSizer.Add(self.headerSizer,0,wx.ALIGN_LEFT|wx.EXPAND)
        self.descSizer.Add(self.descTB,0,wx.ALIGN_LEFT)
        self.descSizer.Add(self.notebook,1,wx.ALIGN_LEFT|wx.EXPAND)

        self.SetSizer(self.descSizer)
        self.Layout()

        if self.options.debug:
            print("## END ## DescriptionPanel.UpdateDesc()")

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
