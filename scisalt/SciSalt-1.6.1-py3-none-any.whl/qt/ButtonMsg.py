import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    from PyQt4 import QtGui, QtCore
    import numpy as _np
from .get_app import get_app

__all__ = ['Button', 'getDouble', 'ButtonMsg', 'getOpenFileName', 'getExistingDirectory']


class Button(object):
    def __init__(self, *args, **kwargs):
        self.standardbutton = None
        self.text           = None
        self.ButtonRole     = None

        self.button_default = kwargs.pop('default', False)
        self.button_escape = kwargs.pop('escape', False)

        if kwargs == {}:
            argnum = _np.size(args)
        else:
            argnum  = _np.size(args) + _np.size(kwargs.values())
        allargs = _np.array(args, dtype=object)
        allargs = _np.append(allargs, kwargs.values())

        if argnum == 1:
            if isinstance(allargs[0], QtGui.QMessageBox.StandardButton):
                self.standardbutton = allargs[0]
            else:
                self.text       = allargs[0]
                self.ButtonRole = QtGui.QMessageBox.AcceptRole
        elif argnum == 2:
            self.text       = allargs[0]
            self.ButtonRole = allargs[1]
        else:
            raise ValueError('Incorrect arguments: {}'.format(allargs))


class getDouble(QtGui.QWidget):
    def __init__(self, **kwargs):
        app = get_app()  # noqa
        super(getDouble, self).__init__()

        title = kwargs.pop('title', '')
        text = kwargs.pop('text', 'Double number:')

        self._input, self._ok = QtGui.QInputDialog.getDouble(self, title, text, **kwargs)

    @property
    def input(self):
        if self._ok:
            return self._input
        else:
            raise IOError('User may have cancelled')


class ButtonMsg(QtGui.QMessageBox):
    def __init__(self, maintext, buttons, title=None, infotext=None):
        self._clicked = None
        self._buttons = buttons
        app = get_app()  # noqa

        super(ButtonMsg, self).__init__()

        self.msgbox = QtGui.QMessageBox()
        self.msgbox.setText(maintext)

        if infotext is not None:
            self.msgbox.setInformativeText(infotext)

        if (title is not None):
            self.msgbox.setWindowTitle(title)

        if (buttons is not None):
            self.btnarray = _np.empty(_np.size(buttons), dtype=object)
            for i, val in enumerate(buttons):
                if not isinstance(val, Button):
                    val = Button(val)
                self.btnarray[i] = self._addbutton(val)
                
                if val.button_default:
                    self.msgbox.setDefaultButton(self.btnarray[i])
                if val.button_escape:
                    self.msgbox.setEscapeButton(self.btnarray[i])
        self.msgbox.exec_()

    def _addbutton(self, button):
        if (button.standardbutton is None):
            added_button = self.msgbox.addButton(button.text, button.ButtonRole)
        else:
            added_button = self.msgbox.addButton(button.standardbutton)
        
        return added_button

    def clickedButton(self):
        return self.msgbox.clickedButton()

    @property
    def clickeditem(self):
        return self._buttons[self.clicked]

    @property
    def clicked(self):
        if self._clicked is None:
            for i, val in enumerate(self.btnarray):
                if (self.clickedButton() == val):
                    self._clicked = i
        
        return self._clicked

    @property
    def clickedArray(self):
        clicked = _np.empty(_np.size(self.btnarray), dtype=_np.bool_)
        for i, val in enumerate(self.btnarray):
            clicked[i] = (self.clickedButton() == val)
            
        return clicked


def getOpenFileName(*args, **kwargs):
    app = get_app()  # noqa

    filepath = QtGui.QFileDialog.getOpenFileName(*args, **kwargs)
    if filepath == '':
        errorstr = 'No valid file selected'
        QtGui.QMessageBox.warning(None, errorstr, errorstr)
        raise IOError(errorstr)

    return str(filepath)


def getExistingDirectory(*args, **kwargs):
    app = get_app()  # noqa

    filepath = QtGui.QFileDialog.getExistingDirectory(*args, **kwargs)
    if filepath == '':
        errorstr = 'No valid directory selected'
        QtGui.QMessageBox.warning(None, errorstr, errorstr)
        raise IOError(errorstr)

    return str(filepath)
