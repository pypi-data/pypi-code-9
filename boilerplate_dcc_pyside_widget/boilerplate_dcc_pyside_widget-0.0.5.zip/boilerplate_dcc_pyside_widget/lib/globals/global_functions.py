# Import
# ----------------------------------------------------
# python
import os
import sys
import logging
import shutil


# logger
# ------------------------------------------------------------------
logger = logging.getLogger(__name__)
logging_level = logging.DEBUG
logger.setLevel(logging_level)


# Globals
# ------------------------------------------------------------------


# OS
# ----------------------------------------------------

def check_interpreter(keyword):
    """Check interpreter path for keyword and return boolean value indicating if found or not.

    :param keyword: Keyword to check in interpreter path.
    :type keyword: str or unicode
    :return: Boolean value based on wether or not sub-string was found.
    :rtype: bool
    """

    # current_interpreter_path
    current_interpreter_path = sys.executable

    # session is mayapy
    if (keyword in current_interpreter_path):
        return True

    return False


def get_user():
    """Get name of currently logged in user.

    :return: Currently logged in user
    :rtype: str
    """

    return os.environ.get('USERNAME')


def copy_file(source_file, source_dir, destination_dir):
    """Copy source_file in source_dir to destination_dir.

    :param source_file: Name of source file
    :type source_file: str
    :param source_dir: Directory of source file
    :type source_dir: str
    :param destination_dir:
    :type destination_dir: Directory to copy to
    :return:
    """

    source = source_dir + '/' + source_file
    shutil.copy(source, destination_dir)
