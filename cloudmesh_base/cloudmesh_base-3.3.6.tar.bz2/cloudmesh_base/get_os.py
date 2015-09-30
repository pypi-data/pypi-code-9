import os
import platform

def get_os():
    """
    if called in powershell returns "powershell"
    if called in cygwin returns "cygwin"
    if called in darwin/osx returns "osx"
    for linux returns "linux"
    """
    env = os.environ
    p = platform.system().lower()
    terminal = p
    
    operating_system = p
    if p == 'windows':
        terminal = "powershell"
        if 'TERM' in env:
            terminal = env['TERM'] 
    if p == 'darwin':
        terminal = 'osx'
    return terminal
    
# print get_os()
