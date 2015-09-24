import wx
import os
import re
import time

import gcal2gcal

class LoginDialog(wx.Dialog):
    def __init__(
        self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
        style=wx.DEFAULT_DIALOG_STYLE):
        
        wx.Dialog.__init__(self,parent,ID,title,pos,size,style)

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Google Calendar Login Information")
        label.SetHelpText("Please enter your google account info here")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Google User Name:")
        label.SetHelpText("Google User Name")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.uname = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.uname.SetHelpText("Enter Your Google User Name")
        box.Add(self.uname, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Google Password")
        label.SetHelpText("Enter your Google Password")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.password = wx.TextCtrl(self, -1, "", size=(80,-1), style=wx.TE_PASSWORD)
        self.password.SetHelpText("Enter your Google Password")
        box.Add(self.password, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog.")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)                        
        
class WxGC2GC(wx.Frame):
    """Main Frame"""
    def __init__(self, options, prefs, *args, **kwargs):
        print 'starting up...'
        wx.Frame.__init__(self, None, *args, **kwargs)
        self.SetTitle("GCal2GCal")
        self.SetSize((600,500))
        self.prefs = prefs
        self.options = options
        self.wow = gcal2gcal.WoWDir(prefs,options.wowdir)

        vbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox = wx.BoxSizer(wx.VERTICAL)
        self.uploadButton = wx.Button(self, -1, "Upload Calendar")
        self.uploadButton.Enable(False);
        self.Bind(wx.EVT_BUTTON, self.upload, self.uploadButton)
        hbox.Add(self.uploadButton)
        vbox.Add(hbox)
        
        self.addonDirPath = wx.StaticText(self, -1, "WoW Directory: %s" % self.wow.getPath())
        vbox.Add(self.addonDirPath,1,wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5)
        self.dirPicker = wx.DirPickerCtrl(self, -1,
                                          message="Select World of Warcraft Directory",
                                          style=wx.DIRP_DIR_MUST_EXIST)
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.dirPicked, self.dirPicker)
        vbox.Add(self.dirPicker,0,wx.ALIGN_RIGHT|wx.ALL,1)
        
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(vbox,0,wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Account Name")
        self.list.InsertColumn(1, "Calendar File Modified At")
        self.list.SetColumnWidth(0, 200)
        self.list.SetColumnWidth(1, 300)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.itemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.itemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.upload, self.list)
        box.Add(self.list,1,wx.ALIGN_CENTER|wx.ALL|wx.EXPAND,5)

        self.SetSizer(box)

        self.wow.scanPath()
        self.updateAccountList()
        #self.setShowAll(True)

    def updateAccountList(self):
        for account in self.wow.getAccounts():
            index = self.list.InsertStringItem(self.list.GetItemCount(), account)
            self.list.SetStringItem(index,1,time.ctime(os.path.getmtime(self.wow.getFilePath(account))))
    
    def dirPicked(self, evt):
        path = evt.GetPath();
        self.addonDirPath.SetLabel("WoW Directory: %s",path)
        if not self.wow.setPath(path):
            print >>sys.stderr,"Invalid WoW Path"
            self.addonDirPath.SetLabel("WoW Directory: <Unknown>")
        else:
            self.prefs.savePrefs()
            self.updateAccountList()        

    def itemSelected(self,evt):
        self.uploadButton.Enable(True)

    def itemDeselected(self,evt):
        self.uploadButton.Enable(False)
        
    def upload(self, evt):
        item = -1
        item = self.list.GetNextItem(item,
                                     wx.LIST_NEXT_ALL,
                                     wx.LIST_STATE_SELECTED);
        dlg = LoginDialog(self, -1, "Google Account Dialog", size=(400, 200),
                         #style=wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME,
                         style=wx.DEFAULT_DIALOG_STYLE)
        dlg.CenterOnParent()
        login = self.prefs.getPref('GoogleLogin', None, self.options.login)
        if login:
            dlg.uname.SetValue(login)

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        
        if val == wx.ID_OK:
            print dlg.uname.GetValue(),dlg.password.GetValue()
            g = gcal2gcal.GC2GC(self.prefs, self.options.gcal, self.options.daysBack, self.options.daysForward)
            g.login(dlg.password.GetValue(), dlg.uname.GetValue())
        dlg.Destroy()
    
def main():
    (options,prefs) = gcal2gcal.readoptions()
    app = wx.App(redirect=0)
    frame = WxGC2GC(options, prefs)
    frame.Show()
    
    app.MainLoop()

if __name__ == '__main__':
    main()

