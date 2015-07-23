import sys
import string
from copy import copy
from getpass import getpass
from common import _Common

class _Render(_Common):
    """
    Private class used to handle rendering any messages set by the
    public feedback class.
    """
    def __init__(self):
        super(_Render, self).__init__()
        
        # Message / input response
        self.msg      = None
        self.response = None
    
    def get_response(self):
        """
        Return then clear the response variable.
        """
        _response = copy(self.response)
        self.response = None
        return _response
    
    def set_message(self, msg):
        """
        Set the internal message variable.
        """
        self.msg = msg
    
    def show(self, tag, **kwargs):
        """
        Format the message and render depending on the tag type and color.
        Center the tag to the width defined in the class constructor.
        """
        
        # Align and format the output string
        str_aligned = string.center(tag, self.width)
        str_refresh = '\r' if kwargs.get('refresh', False) else ''
        str_newline = '\n' if kwargs.get('newline', True) else ''
        
        # If outputting with colors
        if self.colors and kwargs.get('color'):
            msg = '{}[\x1b[1;{}m{}\x1b[0m]: {}{}'.format(str_refresh, kwargs.get('color'), str_aligned, self.msg, str_newline)
        
        # No colors
        else:
            msg = '{}[{}]: {}{}'.format(str_refresh, str_aligned, self.msg, str_newline)
        
        # If capturing input
        if kwargs.get('input_get'):
            msg_input = '[{}]: {}'.format(string.center('INPUT', self.width), self.msg)
            
            # If using a secure prompt
            if kwargs.get('input_secure'):
                
                # Confirm the input
                if kwargs.get('input_confirm'):
                    msg_confirm = '[{}]: Please re-enter the value: '.format(string.center('CONFIRM', self.width))
                    
                    # Input / confirmation prompts
                    prompt = lambda: (getpass(msg_input), getpass(msg_confirm))
        
                    # Get input and confirm
                    def _get_and_confirm_input():
                        val_one, val_two = prompt()
                        if not val_one == val_two:
                            sys.stdout.write('[\x1b[1;{}m{}\x1b[0m]: Values do not match, please try again...\n'.format(self.color['red'], string.center('ERROR', self.width)))
                            return _get_and_confirm_input()
                        return val_one
                    self.response = _get_and_confirm_input()
                    
                # No confirmation needed
                else:
                    self.response = getpass(prompt=msg_input)
                
            # Plain text prompt
            else:
                
                # If parsing a yes/no answer
                if kwargs.get('input_yn', False):
                    def _get_yn_response():
                        _response = raw_input(msg_input)
                        _response = _response.lower()
                        if _response != 'y' and _response != 'n': 
                            sys.stdout.write('[\x1b[1;{}m{}\x1b[0m]: Response must be "y" or "n"...\n'.format(self.color['red'], string.center('ERROR', self.width)))
                            return _get_yn_response()
                        return True if _response == 'y' else False
                    self.response = _get_yn_response()
                else:
                    self.response = raw_input(msg_input)
            
        # Write straight to stdout
        else:
            sys.stdout.write(msg)