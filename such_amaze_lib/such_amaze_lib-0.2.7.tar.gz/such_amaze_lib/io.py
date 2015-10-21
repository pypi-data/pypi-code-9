"""
    This module contain useful function file managing or logging
"""
import os
import re


def purge(directory, pattern):
    """
        Delete recursively all the files that match the current pattern

            :Example:
                >>> # will delete all *.foobar file in the current working directory
                >>> file_name = 'foo.foobar'
                >>> with open(file_name, 'w') as f:
                ...     f.write('foo bar')
                ...     f.close()
                ... 
                >>> os.path.exists(file_name)
                True
                >>> purge('.', '.*\.foobar')
                >>> os.path.exists(file_name)
                False


    :param directory: the directory to scan
    :param pattern: the matching pattern
    """

    for root, _, files in os.walk(directory):
        for f in os.listdir(root):
            if re.search(pattern, f):
                os.remove(os.path.join(root, f))


def create_dirs_if_not_exists(the_path):
    """
     Create all the directory tree of not exists

    :param the_path: the path to create if not exists
    """
    if not os.path.exists(os.path.abspath(the_path)):
        os.makedirs(the_path)
