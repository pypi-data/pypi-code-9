'''dhp transforms library'''

import re

RE_FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
RE_ALL_CAP = re.compile('([a-z0-9])([A-Z])')


def to_snake(buf):
    '''pythonize the name contained in buf'''
    # attribution: http://stackoverflow.com/questions/1175208
    intermediate = RE_FIRST_CAP.sub(r'\1_\2', buf)
    intermediate = RE_ALL_CAP.sub(r'\1_\2', intermediate).lower()
    return intermediate.replace('__', '_')
