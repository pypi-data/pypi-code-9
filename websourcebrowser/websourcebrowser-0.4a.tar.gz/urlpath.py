# encoding: UTF-8
# Copyright (C) 2007-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
Convert filesystem paths to URL paths and vice versa.
"""

import os

# Websourcebrowser modules
import coding
import tools


# separator in URLs
SEP = "/"


def to_url(path, root):
    """Return an absolute URL (starting with a slash, without host and
    port part) which is derived from the absolute file system path
    `path`. The argument `root` is the document root (a file system
    path) to take into account. The function's result is an
    ASCII-encoded string, not a unicode string.

    Trailing path separators on the `path` or `root` are ignored.

    If the `path` isn't part of the `root`, raise a
    `tools.NotUnderRoot` exception.
    """
    if not tools.is_safe_path(path, root):
        raise tools.NotUnderRoot('path "%s" isn\'t under root directory "%s"' %
                                 (path, root))
    path = tools.normalize_path(path)
    root = tools.normalize_path(root)
    if root == path:
        return "/"
    # `rootless_path` is not yet an URL but instead contains the
    #  platform-specific path separator
    rootless_path = path[len(root):]
    # after this, `rootless_path` in any case has a single leading slash
    if tools.is_file_system_root(root):
        rootless_path = "/" + rootless_path
    url = rootless_path.replace(os.sep, SEP)
    url = coding.encode(url)
    return coding.encode_uri(url)

def to_file_system(url, root):
    """Return a file system path (with the proper separator for the
    used platform) derived from `url` and `root`. Whereas `url` is
    an absolute URL (with leading slash, without host name), `root`
    is the document root directory. The argument `url` is an
    ASCII-encoded string; both `root` and the result of the function
    are unicode strings.

    Trailing path separators on the `url` or `root` are ignored.

    If the `path` isn't part of the `root`, raise a
    `tools.NotUnderRoot` exception.
    """
    assert isinstance(url, str), "url must be a bytestring"
    # convert %-entities to their "real" counterparts
    url = coding.decode_uri(url)
    rootless_path = url.replace(SEP, os.sep)
    root = tools.normalize_path(root)
    path = os.path.join(root, rootless_path[1:])
    path = tools.normalize_path(path)
    if not tools.is_safe_path(path, root):
        raise tools.NotUnderRoot('path "%s" isn\'t under root directory "%s"' %
                                 (path, root))
    return path

