# encoding: UTF-8
# Copyright (C) 2009-2010, Stefan Schwarzer

"""
"Converters" to render directory/file paths to HTML.

The function `converter` in this module takes a path and returns an
appropriate converter callable. This takes a single argument, an
instance of `document.Document`.
"""

import mimetypes
import os

import archive_converter
import directory_converter
import feature
import image_converter
import text_converter


class InvalidPath(Exception):
    pass


# support methods for file pane rendering
def _is_image_path(path):
    """Return `True` if the `path` presumably represents an image,
    else return `False`. Also return `False` if the file can't be
    read.

    If the path denotes a directory, the behavior is undefined.
    """
    mime_type = mimetypes.guess_type(path)[0]
    if mime_type is None:
        return False
    return mime_type.split("/", 1)[0] == "image"

def _is_binary_path(path):
    """Return `True`, if `data` assumedly represents binary data,
    not text data. Else return `False`. Also return `False` if the
    file can't be read.

    If the path denotes a directory, the behavior is undefined.
    """
    # number of bytes to read to test for binary data
    binary_test_size = 1024
    try:
        with open(path, "rb") as fobj:
            data = fobj.read(binary_test_size)
    except IOError:
        return False
    if not data:
        return False
    # assume binary data if over 5 % control codes
    threshold = 0.05
    control_codes = [byte for byte in data
                          if ord(byte) < 32 and not byte in "\n\r\t"]
    return (len(control_codes) / float(len(data)) > threshold)


def converter(path):
    """Return a suitable converter for filesystem path `path`.
    
    The returned converter may actually be a chain of converters which
    can be used as a simple function.
    """
    if os.path.isfile(path):
        if _is_image_path(path):
            return image_converter.html
        elif mimetypes.guess_type(path)[0] == 'application/x-tar':
            return archive_converter.tar_file
        elif mimetypes.guess_type(path)[0] == 'application/zip':
            return archive_converter.zip_file
        elif _is_binary_path(path):
            return text_converter.hexdump
        else:
            if feature.pygments:
                return text_converter.highlighted_html
                return text_converter.link_includes_html
            else:
                return text_converter.simple_html
    elif os.path.isdir(path):
        return directory_converter.directory_listing
    else:
        # neither file nor directory, so we have an invalid path
        raise InvalidPath('invalid path "%s"' % path)

