import os
import fnmatch

def find_files_by_ending_in_directory(ending, directory):
    """Return paths to all files with `ending` in subfolders of `directory`"""
    file_list = [os.path.join(dirpath, f)
                 for dirpath, dirnames, files in os.walk(directory)
                 for f in fnmatch.filter(files, "*.{}".format(ending))]
    return file_list
