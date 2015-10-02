"""
Build IDE required files from python folder structure.
"""
import os.path
from fnmatch import fnmatch
from .ideprocesses import vstudio_read, vstudio_write, none_read, none_write

PROCESSES = {
    "vstudio": [vstudio_read, vstudio_write],
    None : [none_read, none_write]
    }

def read_gitignore(source_path):
    """Read .gitignore file and return list of valid patterns."""
    path = os.path.join(source_path, ".gitignore")
    with open(path, 'r') as fgit:
        is_valid = lambda l: l and not l.startswith("#")
        return [l.strip() for l in fgit if is_valid(l.strip())]

def is_ignored(item, patterns):
    """Test if an item should be ignored according to the patterns."""
    return any([fnmatch(item, pattern) for pattern in patterns])

def traverse(source_path, process):
    """Traverse folder structure from source_path and apply process function
    to each step.
    Parameters:
    ------
    source_path: path to traverse
    process: function (level, root, dirs, files)
    Returns:
    actions: list of actions
    """
    patterns = read_gitignore(source_path)
    level = lambda path: path.count("\\") + path.count("/")
    base_level = level(source_path)
    actions = []
    for root, dirs, files in os.walk(source_path):
        remove_ignored(dirs, patterns, is_dir=True)
        remove_ignored(files, patterns)
        actions.extend(process(level(root) - base_level, root, dirs, files))
    return actions

def remove_ignored(alist, patterns, is_dir=False):
    """Remove ignored items from alist according to patterns."""
    checkdir = lambda x: x + "/" if is_dir else x
    to_ignore = [itm for itm in alist if is_ignored(checkdir(itm), patterns)]
    for toi in to_ignore:
        alist.remove(toi)

def build(source_path, overwrite=True, ide=None):
    """
    Traverse source_path folder structure and writes required IDE files.

    :param source_path: relative or full path of python code
    :param overwrite: it will overwrite existing solution and project files
    :param ide: {"vstudio", None}

    The resulting files are written to disk.
    """
    if not os.path.exists(source_path):
        raise IOError("source_path does not exist so not skeleton can be built")

    read_process, write_process = PROCESSES[ide]
    actions = traverse(source_path, read_process)

    return write_process(actions, source_path, overwrite)

