#!/usr/bin/env python2

import os
import wx

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class ImagePanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self,parent,imgFile):

        wx.Panel.__init__(self,
                          parent,
                          style=wx.FULL_REPAINT_ON_RESIZE,
                          size=(900,600))
        self.SetBackgroundColour("#2f9254") ##007256")
        #4a5444") #1c1d22") #"#99cc00") #"#669900")#99cc00

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.UpdateImage(imgFile)

    #----------------------------------------------------------------------
    def UpdateImage(self, imgFile):
        self.img = wx.Image(imgFile, wx.BITMAP_TYPE_ANY)
        #self.img = wx.Image(imgFile, wx.BITMAP_TYPE_PNG)
        #self.img = wx.Image(imgFile, wx.IMAGE_QUALITY_HIGH)
        self.imgx, self.imgy = self.img.GetSize()

    #----------------------------------------------------------------------
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        x,y = self.GetSize()
        posx,posy = 0, 0
        newy = int(float(x)/self.imgx*self.imgy)
        if newy < y:
            posy = int((y - newy) / 2)
            y = newy
        else:
            newx = int(float(y)/self.imgy*self.imgx)
            posx = int((x - newx) / 2)
            x = newx

        img = self.img.Scale(x,y, wx.IMAGE_QUALITY_HIGH)
        self.bmp = wx.BitmapFromImage(img)
        dc.DrawBitmap(self.bmp,posx,posy)

# #    #----------------------------------------------------------------------
# #    def OnPaint(self, event):
# #        #print("OnPaint")
# #        self.dc = wx.PaintDC(self)
# #        self.dc.DrawBitmap(self.bitmap, 0, 0, useMask=False)
# #
# #    #----------------------------------------------------------------------
# #    def getBestSize(self):
# #        (window_width, window_height) = self.GetSizeTuple()
# #        new_height = window_width / self.image_ar
# #        new_size = (window_width, new_height)
# #        return new_size
# #
# #    #----------------------------------------------------------------------
# #    def OnResize(self, event):
# #        (w, h) = self.getBestSize()
# #        self.s_image = self.image.Scale(w, h)
# #        self.bitmap = wx.BitmapFromImage(self.s_image)
# #        self.Refresh()

#        dc.Clear()
#        x,y = self.image.GetSize()
#        posx,posy = 0, 0
#        newy = int(float(x)/self.imgx*self.imgy)
#        if newy < y:
#            posy = int((y - newy) / 2)
#            y = newy
#        else:
#            newx = int(float(y)/self.imgy*self.imgx)
#            posx = int((x - newx) / 2)
#            x = newx
#
#        image = self.image.Scale(x,y, wx.IMAGE_QUALITY_HIGH)
#        self.bmp = wx.BitmapFromImage(image)
#        dc.DrawBitmap(self.bmp,posx,posy)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class ViewerFrame(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, parent, pictPaths, index):

        wx.Frame.__init__(self, parent, title="Image Viewer")
        #self.SetBackgroundColour("#004000")

        panel = ViewerPanel(self,pictPaths,index)
        self.folderPath = ""

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


#----------------------------------------------------------------------
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

        self.slideTimer = wx.Timer(None)
        self.slideTimer.Bind(wx.EVT_TIMER, self.update)

        self.layout()

        #self.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)
        #self.Bind(wx.EVT_LEFT_DOWN, self.LeftClick)

    #----------------------------------------------------------------------
    def layout(self):

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.imagePanel = ImagePanel(self,self.picPaths[self.currentPicture])
        self.mainSizer.Add(self.imagePanel,1,wx.EXPAND|wx.ALL,5)

        self.imageLabel = wx.StaticText(self, label=os.path.basename(self.picPaths[self.currentPicture]))
        #self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.image))
        #self.bitmap = wx.BitmapFromImage(self.image)

        if len(self.picPaths) > 1:
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
    def loadImage(self, imgFile):
        print("LoadImage")
        image_name = os.path.basename(imgFile)

        self.imagePanel.UpdateImage(imgFile)

        self.imageLabel.SetLabel(image_name)
        self.mainSizer.Layout()
        self.Refresh()

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

        if self.currentPicture == self.totalPictures-1:
            self.currentPicture = 0
        else:
            self.currentPicture += 1
        self.loadImage(self.picPaths[self.currentPicture])

    #----------------------------------------------------------------------
    def onPrevious(self, event):

        if self.currentPicture == 0:
            self.currentPicture = self.totalPictures - 1
        else:
            self.currentPicture -= 1
        self.loadImage(self.picPaths[self.currentPicture])

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

    #----------------------------------------------------------------------

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    app = wx.App(redirect=False)
    ViewerFrame(None, ["/tmp/toto.png",
                       "/tmp/titi.png",
                       "/tmp/tata.jpg"], 0)
    app.MainLoop()

    self.Show()
