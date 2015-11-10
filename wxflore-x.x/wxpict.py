import os
import wx
#from wx.lib.pubsub import pub

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class ViewerFrame(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self,parent,pictPaths, index):

        wx.Frame.__init__(self,parent, title="Image Viewer")
        #self.SetBackgroundColour("#004000")

        panel = ViewerPanel(self,pictPaths,index)
        self.folderPath = ""
        #pub.subscribe(self.resizeFrame, ("resize"))
 
        self.initToolbar()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
 
        self.Show()
        self.sizer.Fit(self)
        self.Center()
 
    #----------------------------------------------------------------------
    def initToolbar(self):

        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
 
        open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
        openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Directory")
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)
 
        self.toolbar.Realize()
 
    #----------------------------------------------------------------------
    def onOpenDirectory(self, event):
        print("wxpict.py / onOpenDirectory()")
#
#        dlg = wx.DirDialog(self, "Choose a directory",
#                           style=wx.DD_DEFAULT_STYLE)
# 
#        if dlg.ShowModal() == wx.ID_OK:
#            self.folderPath = dlg.GetPath()
#            print self.folderPath
#            picPaths = glob.glob(self.folderPath + "\\*.jpg")
#            print picPaths
#        pub.sendMessage("update images", picPaths)
 
    #----------------------------------------------------------------------
    def resizeFrame(self, msg):
        self.sizer.Fit(self)


########################################################################
class ViewerPanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent,pictPaths,index):

        wx.Panel.__init__(self, parent, size=(900,600))
        self.SetBackgroundColour("#202020")

        width, height = wx.DisplaySize()
        self.picPaths = pictPaths
        self.currentPicture = index
        self.totalPictures = len(pictPaths)
        self.photoMaxSize = height - 300
#        pub.subscribe(self.updateImages, ("update images"))
 
        self.slideTimer = wx.Timer(None)
        self.slideTimer.Bind(wx.EVT_TIMER, self.update)
 
        self.layout()
 
    #----------------------------------------------------------------------
    def layout(self):
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #imgSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        #image = wx.EmptyImage()
        
        #        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, 
        #                                         wx.BitmapFromImage(img))
        image = wx.Image(self.picPaths[self.currentPicture], wx.BITMAP_TYPE_ANY)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))  
        W = image.GetWidth()
        H = image.GetHeight()
        if W > H:
            NewW = self.photoMaxSize
            NewH = self.photoMaxSize * H / W
        else:
            NewH = self.photoMaxSize
            NewW = self.photoMaxSize * W / H
        image = image.Scale(NewW,NewH)


        #self.mainSizer.Add(self.imageCtrl, 0, wx.ALL|wx.CENTER, 5)

        self.mainSizer.Add(self.imageCtrl, 1, wx.ALL|wx.CENTER, 5)
        #self.mainSizer.Add(imgSizer, 0, wx.ALL, 5)

        if len(self.picPaths) > 1:
            self.imageLabel = wx.StaticText(self, label="")
            self.mainSizer.Add(self.imageLabel, 0, wx.ALL|wx.CENTER, 5)
 
        
            btnData = [("<", btnSizer, self.onPrevious),
                       ("Slide Show", btnSizer, self.onSlideShow),
                       (">", btnSizer, self.onNext)]

            for data in btnData:
                label, sizer, handler = data
                self.btnBuilder(label, sizer, handler)
 
            self.mainSizer.Add(btnSizer, 0, wx.CENTER)

        self.SetSizer(self.mainSizer)
 
    #----------------------------------------------------------------------
    def btnBuilder(self, label, sizer, handler):

        btn = wx.Button(self, label=label)
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
 
    #----------------------------------------------------------------------
    def loadImage(self, image):

        image_name = os.path.basename(image)
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
#        W = img.GetWidth()
#        H = img.GetHeight()
#        if W > H:
#            NewW = self.photoMaxSize
#            NewH = self.photoMaxSize * H / W
#        else:
#            NewH = self.photoMaxSize
#            NewW = self.photoMaxSize * W / H
#        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.imageLabel.SetLabel(image_name)
        #self.Layout()
        self.mainSizer.Layout()
        self.Refresh()
#        pub.sendMessage("resize","")
 
    #----------------------------------------------------------------------
    def nextPicture(self):

        if self.currentPicture == self.totalPictures-1:
            self.currentPicture = 0
        else:
            self.currentPicture += 1
        self.loadImage(self.picPaths[self.currentPicture])
 
    #----------------------------------------------------------------------
    def previousPicture(self):

        if self.currentPicture == 0:
            self.currentPicture = self.totalPictures - 1
        else:
            self.currentPicture -= 1
        self.loadImage(self.picPaths[self.currentPicture])
 
    #----------------------------------------------------------------------
    def update(self, event):

        self.nextPicture()
 
    #----------------------------------------------------------------------
    def updateImages(self, msg):

        self.picPaths = msg.data
        self.totalPictures = len(self.picPaths)
        self.loadImage(self.picPaths[0])
 
    #----------------------------------------------------------------------
    def onNext(self, event):

        self.nextPicture()
 
    #----------------------------------------------------------------------
    def onPrevious(self, event):

        self.previousPicture()
 
    #----------------------------------------------------------------------
    def onSlideShow(self, event):

        btn = event.GetEventObject()
        label = btn.GetLabel()
        if label == "Slide Show":
            self.slideTimer.Start(3000)
            btn.SetLabel("Stop")
        else:
            self.slideTimer.Stop()
            btn.SetLabel("Slide Show")
