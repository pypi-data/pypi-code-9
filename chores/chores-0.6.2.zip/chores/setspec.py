

"""
Implement an include/exclude specification that lets strings
easily specify set inclusion/exclusion.

done|partial      : include=['done','partial']
done|previous     : include=['done','previous']
^partial|previous : exclude=['partial','previous']

Because the tags/statuses are disjoint (not overlapping)
we don't need to worry about more difficult cases specifying
both inclusions and exclusions simultaneously.
"""

import sys
_PY3 = sys.version_info[0] == 3
if _PY3:
    basestring = str

def splitwords(s, sep="|"):
    """
    Split the given string into parts on the given separator.
    Return each of the parts with possible starting and ending
    space stripped away.
    """
    return [w.strip() for w in s.strip().split(sep)]

def spec2list(spec):
    """
    Given a set specification, return a corresponding
    inclusion and exclusion list.
    """
    if not isinstance(spec, basestring):
        return spec

    spec = spec.strip()
    incl, excl = [], []
    if spec.startswith('^'):
        excl = splitwords(spec[1:])
    else:
        incl = splitwords(spec)
    return incl, excl
