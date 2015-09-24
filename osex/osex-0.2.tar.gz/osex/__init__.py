import os
import sys

def append_to_name(source_path, suffix):
    dest_path_prefix = source_path + suffix
    dest_path = dest_path_prefix
    dest_index = 0
    while os.path.lexists(dest_path):
        dest_index += 1
        dest_path = dest_path_prefix + str(dest_index)
    os.rename(source_path, dest_path)

def symlink(source, link_name, relative = False, override = False, backup = True, backup_suffix = "~"):
    if relative:
        source = os.path.relpath(source, os.path.dirname(link_name))
    # os.path.lexists() returns True if path refers to an existing path and 
    # True for broken symbolic links. 
    if override and os.path.lexists(link_name):
        if backup:
            append_to_name(link_name, backup_suffix)
        else:
            if os.path.isdir(link_name):
                os.rmdir(link_name)
            else:
                os.remove(link_name)
    if not os.path.lexists(link_name) or os.readlink(link_name) != source:
        os.symlink(source, link_name)
