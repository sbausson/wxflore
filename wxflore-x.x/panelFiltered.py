import wx
import wxgrid
import panelDesc
import panelThumb
from wx.lib.splitter import MultiSplitterWindow

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Panel(wx.Panel):

    def __init__(self, apps, filtered_struct_list, name, attrib_list = []):

        wx.Panel.__init__(self, apps, -1) # size=(1700, 1000))
        #self.mainPanel = wx.Panel(self, -1)
        #self.mainPanel.SetBackgroundColour(wx.RED)

        self.div_data = apps.div_data
        self.div_data_s = apps.div_data_s

        self.apps = apps
        self.tree = apps.tree
        self.content = apps.content
        self.name = name
        self.options = apps.options
        self.colors = apps.colors

        self.grids_splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        self.index = 0

        self.grid = wxgrid.filteredGrid(self.grids_splitter, self, filtered_struct_list, self.index, attrib_list)
        #self.grid.SetSelection(self.index)

#        self.grid.Bind(wx.EVT_SET_FOCUS, self.onFocus)
#        self.grid.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

        # iiiiiiiii self.descPanel = DescriptionPanel(self.grids_splitter, self.apps, self.options, colors)
        #self.descPanel = panelDesc.Panel(self, self.apps, self.options, colors)

        # Important keep self.grids_splitter for Windows behave correctly
        self.descPanel = panelDesc.Panel(self.grids_splitter, self, self.apps, self.options, self.colors)

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

        if self.options.debug:
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

        if self.options.debug:
            print("wxflore.py FilteredPanel.Update() / index={}".format(index))

        self.index = index

        if self.options.debug:
            print("FilteredPanel.Update() call to self.UpdateDesc()")

        #iiiiii
        #self.content[struct["NL"]] = struct
        self.UpdateDesc()

        if self.options.debug:
            print("FilteredPanel.Update() return from self.UpdateDesc()")

        self.Layout()

    #-------------------------------------------------------------------------------
    def Refresh(self,struct=None):

        if struct != None:
            self.content[struct["NL"]] = struct

        self.UpdateDesc()
        self.Layout()
