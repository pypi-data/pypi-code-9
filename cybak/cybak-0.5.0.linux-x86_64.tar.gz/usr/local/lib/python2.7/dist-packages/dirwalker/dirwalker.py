import os
from os.path import join, getsize
from os import path


# returns a list of files which are not in file_exceptions,
# nor is any part of their path in # dir_exceptions;
# hidden files and folders are ignored by default
def file_lister(source, ignore_hidden=True, file_exceptions=[],
                    dir_exceptions=[]):

    # save the current directory and then move to the source directory
    orig_dir = os.getcwd()
    os.chdir(source)

    # build the list of directories to exclude
    exception_list = []
    for exception in dir_exceptions:
        exception_list.append(user_parse(exception))

    # build the list of files to exclude
    ignore_files = []
    for item in file_exceptions:
        ignore_files.append(user_parse(item))

    # begin building the file list
    file_list = []
    for root, dirs, files in os.walk(source,topdown=True):
        dirs[:] = [d for d in dirs if join(root,d) not in exception_list]
        if ignore_hidden == True:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.startswith('.'):
                pass
            elif os.path.join(root, f) in ignore_files:
                pass
            else:
                file_list.append(join(root, f))

    # change back to the directory that this process was in at init
    os.chdir(orig_dir)

    return file_list


# a quick function to handle user directory shorthands in a string
def user_parse(file_path):
    item_path = None
    item_base = None
    item_path = os.path.expanduser(os.path.dirname(file_path))
    item_base = os.path.basename(file_path)
    return os.path.join(item_path, item_base)
