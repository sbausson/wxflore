#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import wx
import re
import functools
import codecs
import wx.lib.newevent


# AUI
import wx.lib.agw.aui as aui
import wx.aui

import wx.richtext

import wxgrid
import classification
import fldb
import wxeditor
import bota

from wx.lib.splitter import MultiSplitterWindow

ID_HELP_ABOUT = 300
ID_HELP_CREDITS = 301

(NoteUpdateEvent, EVT_NOTE_UPDATE_ID) = wx.lib.newevent.NewEvent()


class colors:
    #selected = ["#cc3399","#99ff33"]
    #selected = ["#ccff66","#808080"]
    selected = ["#ccff33","#707070"]
    selection = ["#ff9933","#202020"]
    #normal = ["#000000","#ffffff"]
    normal = ["#ffffff","#202020"] 
    #nl = ["#ffffff","#202020"]
    nl = ["#ffffff","#202020"]

    #nv = ["#3333CC","#202020"]
    nv = ["#3399ff","#202020"]

    #fa = ["#990033","#202020"]
    fa = ["#ff5c5c","#202020"]


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
def build_text_to_export(struct):

    #-------------------------------------------------------------------------------
    def fill_string(format_string,struct,field_name,field):

        s_res = ""

        try:            
            if field in ["NV","N.UK","N.IT","N.DE","N.ES","N.NL","ZO","FL","HB","REF.wiki.fr"]:
                s = struct[field].replace(";",",") #.encode("utf-8")
                s_res+=format_string.format(field_name,s.encode("utf-8"))

            elif field in ["SY","DS"]:
                s_res+="{}:\n".format(field_name)
                for item in struct[field]:
                    s_res+=format_string.format(item.encode("utf-8"))

            elif field in ["ID.tela","ID.inpn"]:
                s = struct[field]
                s_res+=format_string.format(field_name,s,s)

            elif field in ["FCBN"]:
                print "FCND"
                s = struct["ID.inpn"]
                s_res+=format_string.format(field_name,s)
                
            else:
                s = struct[field] #.encode("utf-8")
                s_res+=format_string.format(field_name,s.encode("utf-8"))
            
        except:
            s_res=""
#            print field
#            print format_string.format(field_name,s.encode("utf-8"))
            
        return s_res
        
    #-------------------------------------------------------------------------------
    s = ""
    format_string = "{:25} : {}\n"
    format_list = " "*8 + "- {}\n"
    format_tela = "{:25} : N°{}  http://www.tela-botanica.org/bdtfx-nn-{}-synthese\n"
    format_inpn = "{:25} : N°{}  http://inpn.mnhn.fr/espece/cd_nom/{}\n"
    format_fcnb = "{:25} : http://siflore.fcbn.fr/?cd_ref={}&r=metro\n"

    s+=fill_string(format_string,struct,"Nom latin","NL")
    s+=fill_string(format_string,struct,"Famille","FA")
    s+=fill_string(format_string,struct,"Nom(s) vernaculaire((s)","NV")
    s+=fill_string(format_string,struct,"Nom Anglais","N.UK")
    s+=fill_string(format_string,struct,"Nom Néerlandais","N.NL")
    s+=fill_string(format_string,struct,"Nom Italien","N.IT")
    s+=fill_string(format_string,struct,"Nom Espagnol","N.ES")
    s+=fill_string(format_string,struct,"Nom Allemand","N.DE")
    s+=fill_string(format_list,struct,"Synonymes","SY")
    s+=fill_string(format_list,struct,"Description","DS")
    s+=fill_string(format_string,struct,"Habitat","HB")
    s+=fill_string(format_string,struct,"Zone Géographique","ZO")
    s+=fill_string(format_string,struct,"Floraison","FL")
    s+=fill_string(format_string,struct,"Usage","US")
    #s+=fill_string(format_string,struct,"Ref. Coste","coste")
    s+=fill_string(format_tela,struct,"Ref. Tela","ID.tela")
    s+=fill_string(format_inpn,struct,"Ref. INPN","ID.inpn")
    s+=fill_string(format_fcnb,struct,"Répartition FCNB","FCBN")
    s+=fill_string(format_string,struct,"Wiki.Fr","REF.wiki.fr")

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
class PanelNOTES(wx.Panel):

    def __init__(self, parent, struct, filename, button):
        print("PanelNOTES")
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
            ed = wxeditor.MainWindow(self,u"Note : {}".format(self.struct["nl"]),self.fn)
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
class ThumbPanel(wx.lib.scrolledpanel.ScrolledPanel):

    #-------------------------------------------------------------------------------
    def __init__(self,parent,options):

        #wx.Panel.__init__(self,parent,size=(-1,-1))
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self,parent,size=(-1,200)) #,style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER|wx.HSCROLL)

        self.SetBackgroundColour("#202020")
        self.options = options
        self.parent = parent
        
#        self.Autosizer = wx.FlexGridSizer(cols=2)
#        self.Autosizer.SetFlexibleDirection(wx.VERTICAL)

#        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1,
#                                                        style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER, name="panel1")
        self.SetupScrolling(True, True)
        self.SetAutoLayout(1)

        self.thumbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.thumbSizer)

        #self.thumbSizer = wx.WrapSizer()
        self.Bind(wx.EVT_SIZE, self.onSize)

    #-------------------------------------------------------------------------------
    def onSize(self, evt):
        size = self.GetSize()
        vsize = self.GetVirtualSize()
        self.SetVirtualSize((size[0], vsize[1]))
        evt.Skip()

    #-------------------------------------------------------------------------------
    def Update(self,struct):

        name_reduced = bota.ReduceName(struct["NL"])

        thumb_dir = os.path.join(self.options.paths.img,"photos.thumb",name_reduced)
        photo_dir = os.path.join(self.options.paths.img,"photos",name_reduced)

        print thumb_dir
        print photo_dir

        self.thumbSizer.DeleteWindows()        
        #self.thumbSizer = wx.BoxSizer(wx.HORIZONTAL)

        if os.path.exists(thumb_dir):
            print(name_reduced)
            
            n=0
            self.pictPaths = []
            locale = wx.Locale(wx.LANGUAGE_DEFAULT)
            for img_name in sorted(os.listdir(thumb_dir)):
                #print img_name
                thumb_path = os.path.join(thumb_dir,img_name)
                photo_path = os.path.join(photo_dir,img_name)

                self.pictPaths.append(photo_path)
                
                image = wx.Image(thumb_path, wx.BITMAP_TYPE_ANY)
                imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))  
                imageBitmap.Bind(wx.EVT_LEFT_DOWN, functools.partial(self.onPhotoClick,n))
                #self.thumbSizer.Add(imageBitmap, 0, wx.ALIGN_LEFT|wx.ALL, 8)
                self.thumbSizer.Add(imageBitmap, 0, wx.ALL|wx.EXPAND, 8)
                n+=1

            #self.Refresh()

        #self.mainthumbSizer.Add(self.thumbSizer)
#        self.SetSizerAndFit(self.thumbSizer)
#        size = self.GetSize()
#        vsize = self.GetVirtualSize()
#        self.SetVirtualSize((size[0], vsize[1]))

        self.Layout()
        #self.Refresh()

        self.FitInside()

    #-------------------------------------------------------------------------------
    def onPhotoClick(self,n,evt):
        print "onPhotoClick",n

        import wxpict

        viewer = wxpict.ViewerFrame(self.parent,self.pictPaths,n)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class DescriptionPanel(wx.Panel):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def __init__(self,parent,apps,options,colors):

        self.options = options
        self.colors = colors 
        self.parent = parent
        self.apps = apps

        wx.Panel.__init__(self,parent,size=(-1,-1))
        self.SetBackgroundColour(colors.normal[1])

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

    #-------------------------------------------------------------------------------
    def Button_OBS(self,event):
        pass

    #-------------------------------------------------------------------------------
    def Button_NOTES(self,event):
        print("Button_NOTES")
        name = "Notes"
        PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
        if PageIndex:
            self.notebook.SetSelection(PageIndex - 1)
        else:
            panel = PanelNOTES(self,self.struct,self.note_fn,self.button_note)
            self.notebook.AddPage(panel, name, True)


    #-------------------------------------------------------------------------------
    def OnNoteUpdate(self,event):
        print("OnNoteUpdate")
        if os.path.exists(self.note_fn):
            self.button_note.SetForegroundColour("#101010")
            self.button_note.SetBackgroundColour("#33CCCC") 
        else:
            self.button_note.SetForegroundColour("#101010")
            self.button_note.SetBackgroundColour("#D0D0D0") 

    #-------------------------------------------------------------------------------
    def onNotebookClose(self,event):
        print("toto")
        
#    def ReadTagsFile(self,name,struct):
#
#        print "TOTOTOTOTO"
#        #if os.path.exists(tag_file):
#
#
    #-------------------------------------------------------------------------------
    def UpdateHeader(self,struct):

        print("wxflore.py / Description.UpdateHeader()")
        self.struct = struct

        n_ = struct["NL"].split("[")
        n1= n_[0]
        if len(n_) == 1:
            n2 = ""
        else:
            n2 = n_[1].replace("]","").strip()

            
        #self.headerRTC.EndAllStyles()

#        try:
#            self.headerSizer1.Clear()
#        except:
#            pass

        try:
            self.headerSizer.Clear(1)
            print("UpdateHeader.Clear()")
        except:
            self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.headerSizer.SetMinSize((-1,self.apps.size["THUMB.YMAX"]))
        
        self.headerRTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        self.headerRTC.SetBackgroundColour(colors.normal[1])
        self.headerRTC.SetForegroundColour(colors.normal[0])
        self.headerRTC.SetEditable(False)

        self.headerRTC.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)

        self.headerRTC.SelectNone()
        self.headerRTC.ChangeValue("")
        self.headerRTC.SelectNone()
        
        self.headerRTC.BeginFontSize(self.apps.size["FONT.BIG"])    
        self.headerRTC.BeginAlignment(wx.TEXT_ALIGNMENT_RIGHT)
        self.headerRTC.BeginTextColour(self.colors.fa[0])
        self.headerRTC.BeginRightIndent(20)

        self.headerRTC.WriteText("{}".format(struct["FA"]))
        self.headerRTC.Newline()

        self.headerRTC.EndRightIndent()
        self.headerRTC.EndTextColour()
        self.headerRTC.EndAlignment()
        self.headerRTC.EndFontSize()

        #self.headerRTC.EndRightIndent()        

        self.headerRTC.BeginTextColour(self.colors.nl[0])
        self.headerRTC.BeginFontSize(self.apps.size["FONT.BIG"])
        self.headerRTC.BeginAlignment(wx.TEXT_ALIGNMENT_LEFT)
        self.headerRTC.BeginLeftIndent(10)
        self.headerRTC.BeginBold()
        self.headerRTC.BeginItalic()
        
        self.headerRTC.WriteText(u"{}".format(n1))

        self.headerRTC.EndItalic()
        self.headerRTC.EndBold()
        self.headerRTC.EndFontSize()        

        self.headerRTC.BeginFontSize(12)
        
        self.headerRTC.WriteText(u" {}".format(n2))
        self.headerRTC.Newline()
        self.headerRTC.EndFontSize()
        self.headerRTC.EndAlignment()
        self.headerRTC.EndTextColour()


        self.headerRTC.BeginAlignment(wx.TEXT_ALIGNMENT_LEFT)

        self.headerRTC.BeginFontSize(self.apps.size["FONT.BIG"])  
        self.headerRTC.BeginTextColour(self.colors.nv[0])
        self.headerRTC.WriteText(u"{}\n".format(struct["NV"].replace(";",", ")))
        self.headerRTC.EndTextColour()
        self.headerRTC.EndFontSize()

        if "N.UK" in struct.keys() and struct["N.UK"] != "":
            self.headerRTC.BeginFontSize(12)  
            self.headerRTC.BeginTextColour("#cc6600")
            self.headerRTC.WriteText(struct["N.UK"].replace(";",", "))
            self.headerRTC.EndTextColour()
            self.headerRTC.EndFontSize()
        
        self.headerRTC.EndAlignment()
        self.headerRTC.EndLeftIndent()        

        self.headerRTC.Newline()
        self.headerRTC.Newline()

        self.headerRTC.BeginTextColour(colors.normal[0])

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
            self.headerRTC.WriteText(u"Ecologie: {} / {}\n".format(struct["baseflor"]["ECO.ch"],struct["baseflor"]["ECO.opt"]))
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

        self.headerRTC.SetBackgroundColour(colors.normal[1])
        self.headerRTC.SetForegroundColour(colors.normal[0])

        self.headerSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.tagsSizer =  wx.BoxSizer(wx.HORIZONTAL)
        self.scrolledTagPanel = wx.lib.scrolledpanel.ScrolledPanel(self,size=(-1,28))
        self.tagFlag = 0

        self.protSizer =  wx.BoxSizer(wx.HORIZONTAL)
        self.scrolledProtPanel = wx.lib.scrolledpanel.ScrolledPanel(self,size=(-1,34))
        self.protFlag = 0

        if "tags" in struct.keys():
            for tag in struct["tags"]:

                statictext = wx.StaticText(self, -1, "Tags:")
                self.tagsSizer.Add((5,-1))
                self.tagsSizer.Add(statictext, 0, wx.ALIGN_LEFT|wx.EXPAND, border=0)
                self.tagsSizer.Add((5,-1))

                button = wx.Button(self.scrolledTagPanel, wx.ID_ANY, u" {} ".format(tag), wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
                button.SetForegroundColour("#600060")
                button.SetBackgroundColour("#6699ff")
                self.tagsSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
                self.tagFlag = 1

        # Catergories
        #-------------
        if "cat" in struct.keys():
#            cat_colors={u"Aquatique":["#f0f0f0","#3399ff"], 
#                        #u'Montagne':["#ffccff","#666699"], 
#                        u"Fougere":["#0C5A10","#A4D765"],
#                        u"Montagne":["#701FE5","#D1ED4A"],
#                        u"Alpine":["#D1F5FA","#9D96A1"],
#                        u"Littoral":["#117BA7","#E9D27C"],
#                        u"Foret":["#002900","#00cc00"], 
#                        u"Ligneuse":[-1,-1]}
#
#            cat_names={"Aquatique":u"Aquatique",
#                        #u'Montagne':["#ffccff","#666699"], 
#                       "Fougere":u"Fougère",
#                       "Montagne":u"Montagne",
#                       "Alpine":u"Alpine",
#                       "Littoral":u"Littoral",
#                       "Foret":u"Forêt",
#                       "Ligneuse":u"Ligneuse"}


            for cat in struct["cat"]:
                button = wx.Button(self.scrolledTagPanel, wx.ID_ANY, u" {} ".format(self.apps.button_config["cat"]["names"][cat]), wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
                try:
                    button.SetForegroundColour(self.apps.button_config["cat"]["colors"][cat][0])
                    button.SetBackgroundColour(self.apps.button_config["cat"]["colors"][cat][1])
                except:
                    pass

                self.tagsSizer.Add(button,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
                self.tagFlag = 1

                self.apps.button_list["cat"].append(cat)


        # Red List Status
        #-----------------
        if "redlist" in struct.keys():
                
            
            rl = struct["redlist"]
            try:
                button = wx.Button(self.scrolledProtPanel, wx.ID_ANY, u" {} ".format(self.apps.button_config["redlist"]["names"][rl]), wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
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
            
            button = wx.Button(self.scrolledProtPanel, wx.ID_ANY, u"France Métropole", wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
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
                    button = wx.Button(self.scrolledProtPanel, wx.ID_ANY, u" {} ".format(region.table[prot][0]),style=wx.BU_EXACTFIT) #.decode("utf8")))
                
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
            id = 400
        
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
                    self.tagFlag = 1

        # COSTE Illustration
        #--------------------
        coste_ill = os.path.join(options.paths.img,u"illustrations",u"Coste",u"{}.png".format(struct["ID.coste"]))
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
        else:
            self.headerSizer.Add((240,-1))


        #self.headerSizer.Layout()
        self.headerSizer1.Add(self.headerRTC,1,wx.ALIGN_LEFT|wx.EXPAND)

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
        
    #-------------------------------------------------------------------------------
    def onPhotoClick(self,coste_ill,evt):
        print "onPhotoClick",coste_ill
        import wxpict
        viewer = wxpict.ViewerFrame(self.parent,[coste_ill],0)

    #-------------------------------------------------------------------------------
    def RightClick(self,event):
        
        menu = wx.Menu()

        self.popupID_COPY_NL_FA_NV_UK = wx.NewId()
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

        menu.Append(self.popupID_COPY_NL_FA_NV_UK, "Copy NL (FA) + NV + N.UK")
        menu.Append(self.popupID_COPY_NL_FA_NV, "Copy NL (FA) + NV")
        menu.Append(self.popupID_COPY_NL_FA, "Copy NL (FA)")
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
            ed = wxeditor.MainWindow(self,u"Main description : {}".format(self.struct["nl"]),self.struct["FN"])
            ed.ShowModal()
            struct = fldb.parse_file(self.struct["FN"],self.struct["N."],options)
            self.apps.Update(struct)

        elif event.GetId() == self.popupID_EDIT_COSTE:
            ed = wxeditor.MainWindow(self,u"COSTE description : {}".format(self.struct["nl"]),self.struct["FN.coste"])
            ed.ShowModal()

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

        print("wxflore.py / Description.UpdateDesc()")
        
        #self.descRTC.Clear()
        big_font = 11
        small_font = 10

        self.descSizer.Clear(1)
        #self.descSizer = wx.BoxSizer(wx.VERTICAL)

        self.UpdateHeader(struct)

        self.descRTC = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        self.descRTC.SetBackgroundColour(colors.normal[1])
        self.descRTC.SetForegroundColour(colors.normal[0])
        self.descRTC.SetEditable(False)

        self.descRTC.BeginTextColour(colors.normal[0])

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
        
        self.descRTC.EndLeftIndent()                
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

        # Toolbar
        self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TB_FLAT | wx.TB_NODIVIDER)

        id = wx.NewId()

        button = wx.Button(self.toolbar, id, "Synonymes", wx.DefaultPosition, (-1,-1), wx.BU_EXACTFIT )
        #button.selection = 0
        self.toolbar.AddControl(button)
        wx.EVT_BUTTON( self, id, self.Button_SYN)
        #self.s_buttons.append(button)
        id+=1

        button = wx.Button(self.toolbar, id, "Observations", wx.DefaultPosition, (-1,-1), wx.BU_EXACTFIT )
        self.toolbar.AddControl(button)
        wx.EVT_BUTTON( self, id, self.Button_OBS)
        id+=1

        self.Bind(EVT_NOTE_UPDATE_ID, self.OnNoteUpdate)

        self.button_note = wx.Button(self.toolbar, id, "Notes", wx.DefaultPosition, (-1,-1), wx.BU_EXACTFIT )
        self.button_note.SetForegroundColour("#101010")
        self.button_note.SetBackgroundColour("#D0D0D0") 
        self.toolbar.AddControl(self.button_note)

        self.note_fn = ""
        if options.paths.meta != "":
            self.note_fn = os.path.join(options.paths.meta,"notes",struct["N."]+".txt")
            print(self.note_fn)
            if os.path.exists(self.note_fn):
                self.button_note.SetForegroundColour("#101010")
                self.button_note.SetBackgroundColour("#33CCCC") 
                
            wx.EVT_BUTTON( self, id, self.Button_NOTES)
            id+=1


#        # Catergories
#        #-------------
#        if "cat" in struct.keys():
#            cat_colors={u'Aquatique':["#f0f0f0","#3399ff"], 
#                        u'Montagne':["#ffccff","#666699"], 
#                        u'Littoral':["#660066","#b89470"], 
#                        u'Forêt':["#002900","#00cc00"], 
#                        u'Ligneuse':[-1,-1]}
#
#
#            for cat in struct["cat"]:
#
#                button = wx.Button(self.toolbar, wx.ID_ANY, u" {} ".format(cat), wx.DefaultPosition, (-1,-1), style=wx.BU_EXACTFIT)
#                try:
#                    button.SetForegroundColour(cat_colors[cat][0])
#                    button.SetBackgroundColour(cat_colors[cat][1])
#                except:
#                    pass
#
#                self.toolbar.AddControl(button)



        self.toolbar.Realize()

        # Description Notebook
        self.notebook = aui.AuiNotebook(self) #,"True",aui.AUI_NB_HIDE_ON_SINGLE_TAB) #,aui.AUI_NB_CLOSE_ON_ALL_TABS)
        self.notebook.SetArtProvider(aui.ChromeTabArt())
        #self.notebook.SetAGWFlags(self.aui_mgr.GetAGWFlags()|wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE )
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onNotebookClose)

        self.notebook.AddPage(self.descRTC, "Description (COSTE)", True)

        #self.scrolled_header = wx.lib.scrolledpanel.ScrolledPanel(self,size=(-1,-1))
        #self.scrolled_header.SetupScrolling(True,True)
        #self.scrolled_header.SetSizer(self.headerSizer)

        self.descSizer.Add(self.headerSizer,0,wx.ALIGN_LEFT|wx.EXPAND)      
        self.descSizer.Add(self.toolbar,0,wx.ALIGN_LEFT) #|wx.EXPAND)  
        self.descSizer.Add(self.notebook,1,wx.ALIGN_LEFT|wx.EXPAND)
        
        self.SetSizer(self.descSizer)
        self.Layout()

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

        self.descPanel = DescriptionPanel(self.grids_splitter, self.apps, self.options, colors)
        
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
        self.thumbPanel = ThumbPanel(self,self.options)        
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

        print("wxflore.py FilteredPanel.Update()",index)

        self.index = index
        self.UpdateDesc()

        self.Layout()
        
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MainPanel(wx.Panel):

    def __init__(self, apps):

        wx.Panel.__init__(self, apps, -1) # size=(1700, 1000))
        #self.mainPanel = wx.Panel(self, -1)        
        #self.mainPanel.SetBackgroundColour(wx.RED)

        self.apps = apps
        self.div_data = apps.div_data
        self.div_data_s = apps.div_data_s

        self.tree = apps.tree
        self.content = apps.content
        self.options = apps.options
        self.colors = apps.colors
#        self.apps = apps
        
        # Content
        #---------
        class pos:
            div = 0
            fam = 0
            gen = 0
            spe = 0

        self.pos=pos()
#        self.colors = colors
        self.pos.div =  [key[0] for key in self.div_data].index("Dicots")

        self.UpdateFam(0)
        self.UpdateGen(0)
        self.UpdateSpe(0)

        self.grids_splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.panel0 = wxgrid.Vpanel(self.grids_splitter, self, 0, self.div_data, self.div_data_s, self.pos.div)
        self.panel1 = wxgrid.Vpanel(self.grids_splitter, self, 1, self.fam_data, self.fam_data_s, self.pos.fam)
        self.panel2 = wxgrid.Vpanel(self.grids_splitter, self, 2, self.gen_data, self.gen_data_s, self.pos.gen)
        self.panel3 = wxgrid.Vpanel(self.grids_splitter, self, 3, self.spe_data, self.spe_data, self.pos.spe)
        self.descPanel = DescriptionPanel(self.grids_splitter, self.apps, self.options, self.colors)


        ##self.tb_desc.AppendText("{}\n".format(self.table[self.fam_data[self.pos.fam][0]][self.gen_data[self.pos.gen][0]]))    

        self.grids_splitter.AppendWindow(self.panel0,180)
        self.grids_splitter.AppendWindow(self.panel1,180)
        self.grids_splitter.AppendWindow(self.panel2,180)
        self.grids_splitter.AppendWindow(self.panel3,200)
        self.grids_splitter.AppendWindow(self.descPanel,500)

        mainPanelSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanelSizer.Add(self.grids_splitter, 1, wx.EXPAND)
        self.thumbPanel = ThumbPanel(self,self.options)        
        self.UpdateDesc()

        #mainPanelSizer.Add(self.thumbPanel, 1, wx.ALL|wx.EXPAND)
        mainPanelSizer.Add(self.thumbPanel, 0, wx.EXPAND) #|wx.EXPAND)
        self.SetSizer(mainPanelSizer)

    #-------------------------------------------------------------------------------
    def UpdateFam(self,update):

        self.fam_data = []
        self.fam_data_s = []
        
        for fam in sorted(self.tree[self.div_data[self.pos.div][0]].keys()):
            n=0
            for gen in self.tree[self.div_data[self.pos.div][0]][fam]:
                n+=len(self.tree[self.div_data[self.pos.div][0]][fam][gen])
            self.fam_data_s.append("{} ({})".format(fam,n))
            self.fam_data.append(fam)
                
        if update:
            self.panel1.UpdateGrid(self, self.fam_data, self.fam_data_s, self.pos.fam)
        
    #-------------------------------------------------------------------------------
    def UpdateGen(self,update):
        if self.fam_data == []:
            self.gen_data = []
            self.gen_data_s = []
        else:
            self.gen_data = []
            self.gen_data_s = []
            for gen in sorted(self.tree[self.div_data[self.pos.div][0]][self.fam_data[self.pos.fam]].keys()):
                n = len(self.tree[self.div_data[self.pos.div][0]][self.fam_data[self.pos.fam]][gen])
                self.gen_data_s.append("{} ({})".format(gen,n))
                self.gen_data.append(gen)
                             
        if update:
            self.panel2.UpdateGrid(self, self.gen_data, self.gen_data_s, self.pos.gen)

    #-------------------------------------------------------------------------------
    def UpdateSpe(self,update):
        if self.fam_data == []:
            self.spe_data = []
            self.spe_data_s = []
        else:
            
            
            self.spe_data = [key for key in sorted(self.tree[self.div_data[self.pos.div][0]][self.fam_data[self.pos.fam]][self.gen_data[self.pos.gen]])]
            #self.spe_data_s = [[key] for key in sorted(self.tree[self.div_data[self.pos.div][0]][self.fam_data[self.pos.fam][0]][self.gen_data[self.pos.gen][0]])

        if update:
            self.panel3.UpdateGrid(self, self.spe_data, self.spe_data, self.pos.spe)

    #-------------------------------------------------------------------------------
    def UpdateDesc(self):

        try:            
            struct = self.content[self.spe_data[self.pos.spe]]
            #print(struct)
            self.descPanel.UpdateHeader(struct)
            self.descPanel.UpdateDesc(struct)
            self.descPanel.Layout()
            self.thumbPanel.Update(struct)
        except IOError:
            print("## WARNING ## Skip UpdateDesc() !!!")


    #-------------------------------------------------------------------------------
    def Update(self,num,index):

        print("wxflore.py / MainPanel.Update()",num,index)
            
        if num == 0:
            self.pos.div = index
            self.pos.fam = 0
            self.pos.gen = 0
            self.pos.spe = 0
            self.UpdateFam(1)
            self.UpdateGen(1)
            self.UpdateSpe(1)
            self.UpdateDesc()
        elif num == 1:
            self.pos.fam = index
            self.pos.gen = 0
            self.pos.spe = 0
            self.UpdateGen(1)
            self.UpdateSpe(1)
            self.UpdateDesc()
            self.panel1.grid.SetFocus()
        elif num == 2:
            self.pos.gen = index
            self.pos.spe = 0
            self.UpdateSpe(1)
            self.UpdateDesc()
            self.panel2.grid.SetFocus()
        elif num == 3:
            self.pos.spe = index
            self.UpdateDesc()
            self.panel3.grid.SetFocus()

        self.Layout()
        

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
        self.SetTitle("wxFlore")
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
        toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TB_FLAT | wx.TB_NODIVIDER)
        
        toolbar.Realize()

        id = 40

        # StatusBar
        #-----------
        #self.statusbar = wx.StatusBar(self, -1)
        #self.statusbar = self.CreateStatusBar()
        #statusbar_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.statusbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                                    wx.TB_FLAT | wx.TB_NODIVIDER)
        sep = "    "

        statictext = wx.StaticText(self.statusbar, -1, "Familles: {}".format(len(self.stats.fam_list)))
#        statusbar_sizer.Add(, 0, wx.ALIGN_LEFT|wx.EXPAND, border=0)
#        statusbar_sizer.Add((30,-1))
        self.statusbar.AddControl(statictext)
        self.statusbar.AddControl(wx.StaticText(self.statusbar, -1, sep))

        statictext = wx.StaticText(self.statusbar, -1, "Genres: {}".format(len(self.stats.gen_list)))
#        statusbar_sizer.Add(statictext, 0, wx.ALIGN_LEFT|wx.EXPAND, border=0)
#        statusbar_sizer.Add((30,-1))
        self.statusbar.AddControl(statictext)
        self.statusbar.AddControl(wx.StaticText(self.statusbar, -1, sep))

        statictext = wx.StaticText(self.statusbar, -1, "Especes: {}".format(len(self.stats.spe_list)))
#        statusbar_sizer.Add(statictext, 0, wx.ALIGN_LEFT|wx.EXPAND, border=0)
#        statusbar_sizer.Add((30,-1))
        self.statusbar.AddControl(statictext)
        self.statusbar.AddControl(wx.StaticText(self.statusbar, -1, sep))

        button = wx.Button(self.statusbar, id, "m1", wx.DefaultPosition, (30,-1))
        button.selection = 0
#        statusbar_sizer.Add(button,0)
        self.statusbar.AddControl(button)
        self.s_buttons.append(button)
        wx.EVT_BUTTON( self, id, self.Button_MARKER)
        id+=1

        button = wx.Button(self.statusbar, id, "m2", wx.DefaultPosition, (30,-1))
        button.selection = 1
#        statusbar_sizer.Add(button,0)
        self.statusbar.AddControl(button)
        self.s_buttons.append(button)
        wx.EVT_BUTTON( self, id, self.Button_MARKER)
        id+=1

        button = wx.Button(self.statusbar, id, "m3", wx.DefaultPosition, (30,-1))
        button.selection = 2
#        statusbar_sizer.Add(button,0)
        self.statusbar.AddControl(button)
        self.s_buttons.append(button)
        wx.EVT_BUTTON( self, id, self.Button_MARKER)
        id+=1

        self.select_button(self.marker_index)

        self.statusbar.AddControl(wx.StaticText(self.statusbar, -1, sep))

#        statusbar_sizer.Add(wx.StaticText(self.statusbar, label=" Search"),0, wx.ALIGN_LEFT|wx.EXPAND, border=0)
#        statusbar_sizer.Add((10,-1))

        self.statusbar.AddControl(wx.StaticText(self.statusbar, label=" Search"))
#        self.statusbar.AddControl((10,-1))

        self.filter_cb = wx.ComboBox(self.statusbar,  wx.CB_DROPDOWN, style=wx.TE_PROCESS_ENTER, pos=(25,25), size=(400,-1)) #|wx.TE_PROCESS_ENTER
        self.filter_cb.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.filter_cb.SetBackgroundColour("#99ff66") ##ccff99")
        self.filter_cb.Clear()
#        statusbar_sozer.Add(self.filter_cb, 0, wx.ALIGN_LEFT|wx.EXPAND, border=0)
        self.statusbar.AddControl(self.filter_cb)
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
        self.statusbar.AddControl(button,) #,0,wx.ALIGN_LEFT|wx.EXPAND) #wx.ALL)
        wx.EVT_BUTTON( self, id, self.onAdvancedSearch)
        id+=1


        self.div_data = [[x[0]] for x in classification.divisions]
        self.div_data += [["Other"]]
        self.div_data += [["All"]]

        self.statusbar.Realize()
        #self.stats.fam_count[key[0]]
        
        #print(self.div_data)
        #print "=========",self.stats.fam_count.keys()
        #print "////////",classification.divisions
        #self.div_fam = [x[1] for x in classification.divisions if x[1] in self.stats.fam_count.keys()]

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
                            if tl not in classification.type_ligneux:
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
        for tl in classification.type_ligneux:
            self.div_data_s.append("    {} ({})".format(tl,count[tl]))  

        self.notebook = aui.AuiNotebook(self) #,aui.AUI_NB_CLOSE_ON_ALL_TABS)
        self.notebook.SetArtProvider(aui.ChromeTabArt())

        self.mainPanel = MainPanel(self)
        self.notebook.AddPage(self.mainPanel, "Main", True)

        #self.mainPanel = MainPanel(self)
        #self.notebook.AddPage(self.mainPanel, "Main", True)
        
        #sizer_0.Add(self.notebook, 1, flag=wx.ALIGN_LEFT|wx.EXPAND)
        #sizer_0.Add(self.statusbar, 1, flag=wx.ALIGN_LEFT) #|wx.EXPAND)

        sizer_0 = wx.BoxSizer(wx.VERTICAL)
        
        sizer_0.Add(toolbar, 0, wx.EXPAND)        
        sizer_0.Add(self.notebook, 1, wx.ALL|wx.EXPAND)
        sizer_0.Add(self.statusbar, 0, wx.ALIGN_LEFT) #|wx.EXPAND)

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
            msg = 'wxFlore - Version %s\nStéphane Bausson' %  version.version
            msg += "\nwxPython version %s" % wx.__version__

            print msg
            msg = msg.decode('utf8','ignore') 

            wx.MessageBox(msg, "About",wx.OK | wx.ICON_INFORMATION)

        except IOError:
            pass

    #-------------------------------------------------------------------------------
    def onHelpCredits(self, event):
        msg = """
Base de données des Trachéophytes de France métropolitaine (bdtfx) (Version 3.00 - 26 janvier 2015)
http://referentiels.tela-botanica.org/referentiel/index.php?module=Informations&ref=bdtfx

Julve, Ph., 1998 ff. baseflor. 
Index botanique, écologique et chorologique de la Flore de France.
Version [date de la version utilisée].
Programme Catminat. <http://perso.wanadoo.fr/philippe.julve/catminat.htm>"""
        print msg
        msg = msg.decode('utf8','ignore')         
        wx.MessageBox(msg, "Credits",wx.OK | wx.ICON_INFORMATION)

    #-------------------------------------------------------------------------------
    def select_button(self,index):

        for i in range(0,self.n_s_buttons):
            if index == i:                
                self.s_buttons[i].SetBackgroundColour("#ccff66")
            else:
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
        search_s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
        #search_p = search_s.split()
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
                        #print struct["NL"]
                        #if struct in filtered_struct_list:
                        #    print(struct["NL"])
                        #    error()

                        filtered_struct_list.append(struct)

        sorted_list = sorted(filtered_struct_list, key=lambda k: (k['FA'], k['NL']))
        if len(filtered_struct_list) == 0:
            self.filter_cb.SetBackgroundColour("#ff5050")
            #wx.MessageBox('Can not find \"%s\" ...' % search_s, 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            print "else"
            
            name = "{}".format(search_s)
            new_panel = FilteredPanel(self,sorted_list) #parent, parent.notebook, name, grid, search_index_list, self, parent.options )
            self.notebook.AddPage( new_panel, name, True )

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

    #-------------------------------------------------------------------------------
    def onAdvancedSearch(self,even):

        name = "Advanced Search"
        PageIndex = IsNotebookPageAlreadyExist(self.notebook,name)
        if PageIndex:
            self.notebook.SetSelection(PageIndex - 1)
        else:
            panel = AdvancedSearchPanel(self)
            self.notebook.AddPage(panel, name, True)

    #-------------------------------------------------------------------------------
    def Update(self,struct):
        print("MainApp.Update")
        self.content[struct["NL"]] = struct
        self.mainPanel.UpdateDesc()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

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

        elif re.match("-wxga",sys.argv[i]):
            options.wxga = 1

        i+=1

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    print("wxPython version: {}".format(wx.__version__))

    options = fldb.OPTIONS()
    #sys.setdefaultencoding('utf8')
    options.noconfig = 0
    options.wxga = 0
    
    if os.getenv("HOME") == None:
        options.home  = os.getenv("HOMEPATH").decode(sys.stdout.encoding)
    else:
        options.home = os.getenv("HOME").decode(sys.stdout.encoding)            

    options.wxflore = os.path.join(options.home,u".wxflore") 
    if not os.path.exists(options.wxflore):
        os.makedirs(options.wxflore)

    sys.path.append(options.wxflore)

    parse_argv(options)

    if options.noconfig:
        default_config = 1
    else:
        default_config = 0

    try:
        import config
        root = config.flore_root
        img_path = config.flore_img_path
    except ImportError:
        default_config = 1

    if default_config:
        script_path = os.path.abspath(os.path.dirname(__file__.decode(sys.stdout.encoding))) 
        root = os.path.join(os.path.split(script_path)[0],"Flores","Main")
        img_path = os.path.join(root,"img")
        print(root,img_path)        
        
    if options.paths.db == "":
        db_base_dir = os.path.join(root,"db")
        options.paths.meta = os.path.join(root,"meta")
        options.paths.db = os.path.join(db_base_dir,"flore.main")
        options.paths.coste = os.path.join(db_base_dir,"flore.coste")
        options.paths.telacol = os.path.join(db_base_dir,"flore.telacol")
        options.paths.seealso = os.path.join(db_base_dir,"see.also")
        options.paths.python = os.path.join(db_base_dir,"python")
        options.paths.cat = os.path.join(db_base_dir,"cat")
        sys.path.append(options.paths.python)
        #sys.path.append(os.path.join(options.paths.python,"prot"))
    else:
        options.paths.meta = ""

    if options.paths.img == "":
        options.paths.img = img_path

    # Create "meta/notes" if needed ...
    if options.paths.meta != "":
        notes_path = os.path.join(options.paths.meta,"notes")
        if not os.path.exists(notes_path):
            os.makedirs(notes_path)


    options.suffix='.'.join([x for x in options.paths.db.split(os.sep) if x !=""])

    print(os.sep)
    print(options.paths.db) 
    print(options.suffix)

    app = wx.App(redirect=False)
    MainApp(options)
    app.MainLoop()

    self.Show()
