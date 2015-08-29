# coding: utf-8

from __future__ import print_function

# install_requires of ruamel.base is not really required but the old
# ruamel.base installed __init__.py, and thus a new version should
# be installed at some point

null = None
_package_data = {   # JSON
    "full_package_name": "ruamel.pdfdouble",
    "version_info": [0, 1, 2],
    "author": "Anthon van der Neut",
    "author_email": "a.van.der.neut@ruamel.eu",
    "description": "scan and find double PDF files, by creating a hash database",  # NOQA
    "entry_points": 1,
    "install_requires": {
        "any": ["ruamel.base>=1.0.0", "ruamel.appconfig"]
    },
    "entry_points": ["pdfdbl = ruamel.pdfdouble:main"],
    "universal": 1
}   # JSON


# < from ruamel.util.new import _convert_version
def _convert_version(tup):
    """create a PEP 386 pseudo-format conformant string from tuple tup"""
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


# <
version_info = _package_data['version_info']
__version__ = _convert_version(version_info)

del _convert_version


def main():
    # No direct import of pdf_double in order not to pollute namespace.
    # If other utility 'bodies' exist in this directory a module level
    # import here, would get you all of its initialisations/imports as well
    from pdfdouble import main as util_main
    util_main()
