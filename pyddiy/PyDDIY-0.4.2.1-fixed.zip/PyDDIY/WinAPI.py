import clr
clr.AddReferenceToFileAndPath("DDIY.dll")

import DDIY

class WinAPI:
    """ Wrapper for winapi handling. """
    def __init__(self):
        self._winapi = DDIY.API.Win.WinAPI()

    def __repr__(self):
        return "<DDIY.API.Win.WinAPI wrapper>"

    def CaptureScreen(self):
        """ Returns printscreen in System.Drawing.Image. """
        return self._winapi.CaptureScreen()

    def GetWindowRectangle(self, processOrNameOrId):
        """ Returns process rectangle(position and size) in System.Drawing.Rectangle """
        return self._winapi.GetWindowRectangle(processOrNameOrId)

    def FocusWindow(self, processOrNameNameOrId):
        """ Focuses main window of specified process.
            Returns True if successful. Otherwise False. """
        return self._winapi.FocusWindow(processOrNameOrId)

    def BlockInput(self):
        """ Blocks all user input unless CTRL+ALT+DEL is pressed.
            App has to run under ADMINISTRATOR!!! """
        self._winapi.BlockInput(True)

    def UnblockInput(self):
        """ Unblocks all previously blocked input.
            App has to run under ADMINISTRATOR!!! """
        self._winapi.BlockInput(False)
