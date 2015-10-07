"""
==============================================
Extend login Interface for fogbugz
Parts of this code comes from the fborm project
==============================================
"""

import getpass
import contextlib
import os
import re

__version__ = (0,2,0)
__version_string__ = '.'.join(str(x) for x in __version__)

__author__ = 'Nicolas Morales'
__email__ = 'portu.github@gmail.com'

def get_credentials(hgrc, hgPrefix, interactive):
    """When credentials are not provided in the constructor, get them from hgrc or prompt user
       hgrc: Path to hgrc file
       hgPrefix: prefix for user and password. Useful if the hgrc is used for multiple servers
                 with different credentials
       interactive: If credentials not found in hgrc and this is set, prompt the user
    """
    #Search whether there is an hgrc file. Default: ~/hgrc
    username = None
    password = None
    if not hgrc:
        hgrc = os.path.join(os.path.expanduser("~"), '.hgrc')
    if os.path.isfile(hgrc):
        for line in open(hgrc):
            line = line.split('#')[0]
            if hgPrefix + 'username' in line:
                res = re.search('username\s*=\s*(\S+)', line)
                username = res.group(1)
            elif hgPrefix + 'password' in line:
                res = re.search('password\s*=\s*(\S+)', line)
                password = res.group(1)
    if interactive:
        if not username:
            username = raw_input('user: ')
        if not password:
            password = getpass.getpass('password: ')# Same as raw_input but does not print what user types
    return username, password

def FogBugz(fbConstructor, hostname, token=None, username=None, password=None, hgrc=None, hgPrefix='',
            interactive=True, storeCredentials=False):
    """Calls the constructor specified by fbConstructor (hence, despite this being a function use CapWords naming convention)

       fbConstructor: Fogbugz constructor class. Typically fogbugz.FogBugz, fborm.FogBugzORM or kiln.Kiln
       hostname: passed directly to the fbInterface
       token, username, password: input credentials
       hgrc, hgPrefix, interactive: Passed to method get_credentials
       storeCredentials: If active, create attributes token, username and password. This opens the door to using it for login to other
                         system, which is convenient, but the programmer can also do what he wants with the password (which is bad).
       TODO: Support passing a list of args to fbConstructor
    """
    if token and (username or password):
        raise TypeError("if you supply 'token' you cannot supply 'username' or 'password'")
    if (username and not password) or (not username and password):
        raise TypeError("You must supply both 'username' and 'password'")
    if not username and not token:
        username, password = get_credentials(hgrc, hgPrefix, interactive)
    if not username and not password: # If still no credentials available, raise
        raise TypeError("You must provide either 'username' and 'password' or token")

    fb = fbConstructor(hostname, token=token)
    if username:
        fb.logon(username, password)

    if storeCredentials:
        fb.token = token
        fb.username = username
        fb.password = password

    return fb

@contextlib.contextmanager
def FogBugz_cm(fbConstructor, hostname, **kwargs):
    '''Context manager with logOff functionality'''
    fb = FogBugz(fbConstructor, hostname, **kwargs)
    yield fb

    fb.logoff()
