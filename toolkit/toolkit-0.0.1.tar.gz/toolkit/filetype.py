# coding=utf8

"""
Helper function for file types.
"""

from toolkit import ToolkitException

class FiletypeException(ToolkitException):
    pass


class FiledetException(FiletypeException):
    pass


_file_type_map = {
    '.py': 'python',
    '.sh': 'bash',
}


def filedet(name, fobj=None, suffix=None):
    """
    Detect file type by filename.

    :param name: file name
    :param fobj: file object
    :param suffix: file suffix like ``py``, ``.py``
    :return: file type full name, such as ``python``, ``bash``
    """
    name = name or (fobj and fobj.name) or suffix
    separated = name.split('.')
    if len(separated) == 1:
        raise FiledetException('file name error.')

    key = '.' + separated[-1]
    return _file_type_map.get(key)
