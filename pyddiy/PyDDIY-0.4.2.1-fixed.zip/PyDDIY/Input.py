import clr
clr.AddReferenceToFileAndPath("DDIY.dll")

import DDIY

class Input:
    """ Wrapper for DDIY.DirectInput and DDIY.VirtualInput. """
    def __init__(self, inputType = "directinput"):
        self.SetInputType(inputType)

    def __repr__(self):
        if isinstance(self._input, DDIY.DirectInput):
            return "<DDIY.DirectInput wrapper>"
        elif isinstance(self._input, DDIY.VirtualInput):
            return "<DDIY.VirtualInput wrapper>"

        return "<Unknown DDIY.Input wrapper>"

    def SetInputType(self, inputType):
        """ Sets input type method. Possible inputType is "directinput" or "virtualinput". """
        if inputType.lower() == "directinput":
            self._input = DDIY.DirectInput()
        elif inputType.lower() == "virtualinput":
            self._input = DDIY.VirtualInput()
        else:
            raise ValueError("Only \"directinput\" and \"virtualinput\" supported.")

    def GetKey(self, code):
        """ Returns key number. Code parameter expects:
            http://www.flint.jp/misc/?q=dik&lang=en for DDIY.DirectInput aka "directinput"
            https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx for DDIY.VirtualInput aka "virtualinput"
        """
        return self._input.GetKeyCodes()[code]

    def SetDelay(self, delay):
        """ Sets inter-command delay. Eg. delay between drag and drop. """
        self._input.Delay = delay

    def Text(self, text):
        """ Simulates text writing. """
        self._input.Text(text)

    def PressKey(self, key1, key2=None, key3=None, key4=None):
        """ Simulates pressing up to 4 keys. Expects code number obtained from Input.GetKey(code). """
        if key1 and not key2 and not key3 and not key4:
            self._input.Key(key1)
        elif key1 and key2 and not key3 and not key4:
            self._input.Key(key1, key2)
        elif key1 and key2 and key3 and not key4:
            self._input.Key(key1, key2, key3)
        elif key1 and key2 and key3 and key4:
            self._input.Key(key1, key2, key3, key4)

    def LeftClick(self, x, y):        
        self._input.LeftMouseClick(x, y)

    def RightClick(self, x, y):
        self._input.RightMouseClick(x, y)

    def Drag(self, sourceX, sourceY, destinationX, destinationY):
        """ Simulates left mouse button press on source position and left mouse button release on destination position. """
        self._input.MouseDraw( sourceX, sourceY, destinationX, destinationY)

    def Move(self, x, y):
        """ Moves mouse cursor to specified position. """
        self._input.MouseMove( x, y)
