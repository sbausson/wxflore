# -*- coding: utf-8 -*-

import wx
from wx.lib.splitter import MultiSplitterWindow

import wxgrid
import panelDesc
import panelThumb

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Panel(wx.Panel):

    def __init__(self, apps):

        self.options = apps.options

        if self.options.debug:
            print("MainPanel.__init__()")

        wx.Panel.__init__(self, apps, -1) # size=(1700, 1000))
        #self.mainPanel = wx.Panel(self, -1)
        #self.mainPanel.SetBackgroundColour(wx.RED)

        self.apps = apps
        self.div_data = apps.div_data
        self.div_data_s = apps.div_data_s

        self.tree = apps.tree
        self.content = apps.content
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

        import classification

        self.pos.div =  [key[0] for key in self.div_data].index(classification.default_division)

        self.UpdateFam(0)
        self.UpdateGen(0)
        self.UpdateSpe(0)

        self.grids_splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.panel0 = wxgrid.Vpanel(self.grids_splitter, self, 0, self.div_data, self.div_data_s, self.pos.div)
        self.panel1 = wxgrid.Vpanel(self.grids_splitter, self, 1, self.fam_data, self.fam_data_s, self.pos.fam)
        self.panel2 = wxgrid.Vpanel(self.grids_splitter, self, 2, self.gen_data, self.gen_data_s, self.pos.gen)
        self.panel3 = wxgrid.Vpanel(self.grids_splitter, self, 3, self.spe_data, self.spe_data, self.pos.spe)
        # iiiiiiii self.descPanel = DescriptionPanel(self.grids_splitter, self.apps, self.options, self.colors)
        #self.descPanel = panelDesc.Panel(self, self.apps, self.options, self.colors)

        # Important keep self.grids_splitter for Windows behave correctly
        self.descPanel = panelDesc.Panel(self.grids_splitter, self, self.apps, self.options, self.colors)


        ##self.tb_desc.AppendText("{}\n".format(self.table[self.fam_data[self.pos.fam][0]][self.gen_data[self.pos.gen][0]]))

        self.grids_splitter.AppendWindow(self.panel0,180)
        self.grids_splitter.AppendWindow(self.panel1,180)
        self.grids_splitter.AppendWindow(self.panel2,180)
        self.grids_splitter.AppendWindow(self.panel3,200)
        self.grids_splitter.AppendWindow(self.descPanel,500)

        mainPanelSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanelSizer.Add(self.grids_splitter, 1, wx.EXPAND)
        self.thumbPanel = panelThumb.Panel(self,self.options)

        print("MainPanel.__init__() call to self.UpdateDesc()")
        self.UpdateDesc()
        print("MainPanel.__init__() return from self.UpdateDesc()")

        #mainPanelSizer.Add(self.thumbPanel, 1, wx.ALL|wx.EXPAND)
        mainPanelSizer.Add(self.thumbPanel, 0, wx.EXPAND) #|wx.EXPAND)
        self.SetSizer(mainPanelSizer)
        print("## END ## MainPanel.__init__()")

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
            # test self.descPanel.UpdateHeader(struct)
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
    def Refresh(self,struct=None):

        if struct != None:
            self.content[struct["NL"]] = struct

        self.UpdateDesc()
        self.Layout()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
