from __future__ import with_statement
from plumbum.path.base import Path
from plumbum.lib import six
from plumbum.machines.local import local, LocalPath


def delete(*paths):
    """Deletes the given paths. The arguments can be either strings,
    :class:`local paths <plumbum.path.local.LocalPath>`,
    :class:`remote paths <plumbum.path.remote.RemotePath>`, or iterables of such.
    No error is raised if any of the paths does not exist (it is silently ignored)
    """
    for p in paths:
        if isinstance(p, Path):
            p.delete()
        elif isinstance(p, six.string_types):
            local.path(p).delete()
        elif hasattr(p, "__iter__"):
            delete(*p)
        else:
            raise TypeError("Cannot delete %r" % (p,))

def _move(src, dst):
    ret = copy(src, dst)
    delete(src)
    return ret

def move(src, dst):
    """Moves the source path onto the destination path; ``src`` and ``dst`` can be either
    strings, :class:`LocalPaths <plumbum.path.local.LocalPath>` or
    :class:`RemotePath <plumbum.path.remote.RemotePath>`; any combination of the three will
    work. 
    
    .. versionadded:: 1.3
        ``src`` can also be a list of strings/paths, in which case ``dst`` must not exist or be a directory.
    """
    if not isinstance(dst, Path):
        dst = local.path(dst)
    if isinstance(src, (tuple, list)):
        if not dst.exists():
            dst.mkdir()
        elif not dst.isdir():
            raise ValueError("When using multiple sources, dst %r must be a directory" % (dst,))
        for src2 in src:
            move(src2, dst)
        return dst
    elif not isinstance(src, Path):
        src = local.path(src)

    if isinstance(src, LocalPath):
        if isinstance(dst, LocalPath):
            return src.move(dst)
        else:
            return _move(src, dst)
    elif isinstance(dst, LocalPath):
        return _move(src, dst)
    elif src.remote == dst.remote:
        return src.move(dst)
    else:
        return _move(src, dst)

def copy(src, dst):
    """
    Copy (recursively) the source path onto the destination path; ``src`` and ``dst`` can be
    either strings, :class:`LocalPaths <plumbum.path.local.LocalPath>` or
    :class:`RemotePath <plumbum.path.remote.RemotePath>`; any combination of the three will
    work.

    .. versionadded:: 1.3
        ``src`` can also be a list of strings/paths, in which case ``dst`` must not exist or be a directory.
    """
    if not isinstance(dst, Path):
        dst = local.path(dst)
    if isinstance(src, (tuple, list)):
        if not dst.exists():
            dst.mkdir()
        elif not dst.isdir():
            raise ValueError("When using multiple sources, dst %r must be a directory" % (dst,))
        for src2 in src:
            copy(src2, dst)
        return dst
    elif not isinstance(src, Path):
        src = local.path(src)

    if isinstance(src, LocalPath):
        if isinstance(dst, LocalPath):
            return src.copy(dst)
        else:
            dst.remote.upload(src, dst)
            return dst
    elif isinstance(dst, LocalPath):
        src.remote.download(src, dst)
        return dst
    elif src.remote == dst.remote:
        return src.copy(dst)
    else:
        with local.tempdir() as tmp:
            copy(src, tmp)
            copy(tmp / src.basename, dst)
        return dst


