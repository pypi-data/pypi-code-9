# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

# install_requires of ruamel.base is not really required but the old
# ruamel.base installed __init__.py, and thus a new version should
# be installed at some point

null = None
_package_data = {   # JSON
    "full_package_name": "ruamel.std.shutil",
    "version_info": [0, 1, 0],
    "author": "Anthon van der Neut",
    "author_email": "a.van.der.neut@ruamel.eu",
    "description": "backports of shutil rounes (get_terminal_size)",
    "entry_points": null,
    "license": "Copyright Ruamel bvba 2007-2015",
    # "status": "α",
    # "data_files": "",
    # "universal": 1,
    "install_requires": {
        # "py27": ["ruamel.ordereddict"],
        "any": []
    }
}   # JSON


def _convert_version(tup):
    """Create a PEP 386 pseudo-format conformant string from tuple tup."""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    for x in tup[1:]:
        if isinstance(x, int):
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            ret_val += '.post' if first_letter == 'p' else '.dev'
    return ret_val


version_info = _package_data['version_info']
__version__ = _convert_version(version_info)


del _convert_version

import sys
from shutil import *

if sys.version_info < (3, 3):
    from .getterminalsize import *

