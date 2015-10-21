import clr
clr.AddReferenceToFileAndPath("DDIY.dll")

import DDIY

class Clipboard:
    """ Wrapper for clipboard handling. """
    def __repr__(self):
        return "<DDIY.Clipboard wrapper>"

    def GetText(self):
        """ Returns text from clipboard. """
        return DDIY.Clipboard().GetText()

    def SetText(self, text):
        """ Puts text into clipboard. """
        DDIY.Clipboard().SetText(text)
