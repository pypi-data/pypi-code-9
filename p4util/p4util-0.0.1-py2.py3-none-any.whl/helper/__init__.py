'''
Utility functions that are not Perforce related
'''

import sys
import logging as log
log.basicConfig(level=log.DEBUG)

from subprocess import Popen, PIPE

## Yucky bits to handle Python2 and Python3 differences
PY2 = sys.version_info[0] == 2  # sys.version_info.major won't work until 2.7 :(
PY3 = sys.version_info[0] == 3

def bail(msg=None):
    if msg:
        log.fatal(msg)
    sys.exit(1)

def check_output(*args, **kws):
    '''mimic subprocess.check_output for pre-Python 3.1'''
    if 'stdout' not in kws:
        kws['stdout'] = PIPE
    pipe = Popen(*args, **kws)
    rv = pipe.communicate()[0]
    if PY3 and type(rv)==bytes:
        rv = rv.decode(self.charset or self.encoding or 'utf8')
    return rv
