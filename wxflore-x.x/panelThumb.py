import os
import re
import wx
import functools

import bota
import mkthumb

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Panel(wx.lib.scrolledpanel.ScrolledPanel):

    #-------------------------------------------------------------------------------
    def __init__(self,parent,options):

        self.options = options
        self.parent = parent
        self.colors = self.parent.apps.colors

        #wx.Panel.__init__(self,parent,size=(-1,-1))
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self,parent,size=(-1,200))
        #,style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER|wx.HSCROLL)
        self.SetBackgroundColour(self.colors.normal[1])

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
        self.Bind(wx.EVT_RIGHT_DOWN, self.RightClick)

    #-------------------------------------------------------------------------------
    def RightClick(self,event):

        self.popupID_REFRESH = wx.NewId()
        self.popupID_DUPLICATE = wx.NewId()
        self.popupID_DOWNLOAD = wx.NewId()

        menu = wx.Menu()
        menu.Append(self.popupID_REFRESH, "Remame and Refresh thumb gallery")
        menu.Append(self.popupID_DUPLICATE, "Check Duplicate pictures")
        menu.Append(self.popupID_DOWNLOAD, "Download")
        menu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.RightClickMenu)

        self.PopupMenu(menu)
        menu.Destroy()

    #-------------------------------------------------------------------------------
    def RightClickMenu(self,event):

        #-------------------------------------------------------------------------------
        def duplicate():
            duplicates = mkthumb.check_duplicate(self.options,self.name_reduced)

            if duplicates != []:

                msg = "Remove this duplicates pictures ?\n\n" + "\n".join(duplicates)
                dlg = wx.MessageDialog(None, msg, "Duplicated Photos",wx.YES_NO | wx.ICON_QUESTION)
                retCode = dlg.ShowModal()

                if (retCode == wx.ID_YES):
                    #print("Remove {}".format(filename))
                    for photo in duplicates:
                        print("Removing {} ...".format(photo))
                        os.remove(photo)

                    mkthumb.mkthumb(self.options,self.name_reduced)
                    self.update = True

        #-------------------------------------------------------------------------------
        print("ThumbPanel.RightClickMenu()")
        s=""

        if event.GetId() == self.popupID_REFRESH:
            mkthumb.number(self.options,self.name_reduced)
            mkthumb.mkthumb(self.options,self.name_reduced)
            self.Update()

        elif event.GetId() == self.popupID_DUPLICATE:
            print("CHECK_DUPLICATE")
            duplicate()
            if self.update:
                self.Update()

        elif event.GetId() == self.popupID_DOWNLOAD:

            if not wx.TheClipboard.IsOpened():  # may crash, otherwise
                do = wx.TextDataObject()
                wx.TheClipboard.Open()
                success = wx.TheClipboard.GetData(do)
                wx.TheClipboard.Close()
                if success:
                    link = do.GetText()
                    if re.match("https?://",link):
                        mkthumb.download(self.options,self.name_reduced,link)
                        print("download done")
                        mkthumb.number(self.options,self.name_reduced)
                        mkthumb.mkthumb(self.options,self.name_reduced)
                        self.update = True

            duplicate()
            if self.update:
                self.Update()

    #-------------------------------------------------------------------------------
    def onSize(self, evt):
        size = self.GetSize()
        vsize = self.GetVirtualSize()
        self.SetVirtualSize((size[0], vsize[1]))
        evt.Skip()

    #-------------------------------------------------------------------------------
    def Update(self,struct=None):

        if struct != None:
            self.struct = struct

        self.name_reduced = bota.ReduceName(self.struct["NL"])

        thumb_dir = os.path.join(self.options.paths.img,"photos.thumb",self.name_reduced)
        photo_dir = os.path.join(self.options.paths.img,"photos",self.name_reduced)

        print thumb_dir
        print photo_dir

        self.thumbSizer.DeleteWindows()
        #self.thumbSizer = wx.BoxSizer(wx.HORIZONTAL)

        if os.path.exists(thumb_dir):
            print(self.name_reduced)

            n=0
            self.pictPaths = []
            locale = wx.Locale(wx.LANGUAGE_DEFAULT)
            sorted_thumb_paths = sorted(os.listdir(thumb_dir))
            if len(sorted_thumb_paths) and not re.match(".*\.00.jpg",sorted_thumb_paths[0]):
                image = wx.Image(self.options.wxflore_png_nodefault, wx.BITMAP_TYPE_PNG)
                imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))

                #self.thumbSizer.Add(imageBitmap, 0, wx.ALIGN_LEFT|wx.ALL, 8)
                self.thumbSizer.Add(imageBitmap, 0, wx.ALL|wx.EXPAND, 8)

            for img_name in sorted_thumb_paths:
                #print img_name
                thumb_path = os.path.join(thumb_dir,img_name)
                photo_path = os.path.join(photo_dir,img_name)

                self.pictPaths.append(photo_path)

                image = wx.Image(thumb_path, wx.BITMAP_TYPE_ANY)
                imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image))
                imageBitmap.Bind(wx.EVT_LEFT_DOWN, functools.partial(self.onPhotoClick,n))
                imageBitmap.Bind(wx.EVT_RIGHT_DOWN, functools.partial(self.onPictureRightClick,n))

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
    def onPictureRightClick(self,n,evt):
        print "onPhotoRightClick"

        filename = self.pictPaths[n]

        menu = wx.Menu()

        self.popupID_DELETE = wx.NewId()
        self.popupID_RENAME = wx.NewId()
        self.popupID_SET_DEFAULT = wx.NewId()

        menu.AppendSeparator()
        menu.Append(self.popupID_DELETE, "Delete thic picture")
        menu.Append(self.popupID_RENAME, "Rename this picture")
        menu.Append(self.popupID_SET_DEFAULT, "Set this picture as Default (index '00')")

        self.Bind(wx.EVT_MENU, functools.partial(self.RightClickPictureMenu,filename))

        self.PopupMenu(menu)
        menu.Destroy()

    #-------------------------------------------------------------------------------
    def RightClickPictureMenu(self,filename,event):
        print("ThumbPanel.RightClickMenu()")

        update = 0

        if event.GetId() == self.popupID_DELETE:
            print("DELETE")

            msg = u'Are you sure you want to delete  "{}" ?'.format(filename)
            dlg = wx.MessageDialog(None, msg, "Please confirm ...",wx.YES_NO | wx.ICON_QUESTION)

            retCode = dlg.ShowModal()
            if (retCode == wx.ID_YES):
                print("Remove {}".format(filename))
                os.remove(filename)
                update = 1
            else:
                print "no"


        elif event.GetId() == self.popupID_RENAME:
            print("RENAME",filename)

            path,name = os.path.split(filename)
            dlg = wx.FileDialog(self, message="Rename as  ...",
                                defaultDir=path,
                                defaultFile=name, wildcard="*", style=wx.SAVE)

            if dlg.ShowModal() == wx.ID_OK:
                newfilename = dlg.GetPath()
                os.rename(filename,newfilename)
                update = 1

            dlg.Destroy()


        elif event.GetId() == self.popupID_SET_DEFAULT:
            print("SET_DEFAULT")
            mkthumb.setdefault(self.options,self.name_reduced, os.path.split(filename)[-1])
            update = 1

        if update:
            mkthumb.mkthumb(self.options,self.name_reduced)
            self.Update()
            self.parent.Refresh()

#-------------------------------------------------------------------------------
