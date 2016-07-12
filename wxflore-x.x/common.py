import wx.lib.newevent

(NoteUpdateEvent, EVT_NOTE_UPDATE_ID) = wx.lib.newevent.NewEvent()
(ObsUpdateEvent, EVT_OBS_UPDATE_ID) = wx.lib.newevent.NewEvent()
(PictGalleryEvent, EVT_PICT_GALLERY_ID) = wx.lib.newevent.NewEvent()
(DownloadEvent, EVT_DOWNLOAD_ID) = wx.lib.newevent.NewEvent()

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
