#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = '0.1'
from getpass import getpass
from common import _Common
from render import _Render

class Feedback(_Common):
    def __init__(self):
        super(Feedback, self).__init__()
        
        # Render manager / handler
        self.render   = _Render()
    
    def get_response(self):
        """
        Return then clear the response variable.
        """
        return self.render.get_response()
        
    def success(self): 
        """
        Display a success message on the screen.
        """
        self.render.show('SUCCESS', color=self.color['green'])
        
    def warn(self): 
        """
        Display a warning message on the screen.
        """
        self.render.show('WARNING', color=self.color['yellow'])
        
    def error(self): 
        """
        Display an error message on the screen.
        """
        self.render.show('ERROR', color=self.color['red'])

    def block(self, label='INFO'):
        """
        Display a block of indented text.
        """
        self.render.show(label, newline=False)

    def input(self, secure=False, confirm=False, yes_no=False):
        """
        Display an input prompt on the screen.
        """
        self.render.show('INPUT', input_get=True, input_secure=secure, input_confirm=confirm, input_yn=yes_no)

    def info(self): 
        """
        Display an informational message on the screen.
        """
        self.render.show('INFO')

    def set(self, msg=None, **kwargs):
        """
        Set the message to display with the chosen rendering method.
        
        :param  msg: The message to display
        :type   msg: str
        :rtype: self
        """
        if isinstance(msg, str):
            _msg = msg
        elif isinstance(msg, list):
            indent   = self.width + 4
            count    = 0
            _msg = ''
            for line in msg:
                indent_str = '' if count == 0 else ' ' * indent
                _msg += '{}{}\n'.format(indent_str, line)
                count += 1
        else:
            return self
        
        # Pass the message to the rendering handler
        self.render.set_message(_msg)
        
        # Return this object
        return self