from os.path import isabs, expanduser, realpath, join as path_join
from os import getcwd, getpid
from subprocess import call
from tempfile import gettempdir
import atexit

def get_outfolder(outfolder, r_pid, create_folder=True):
    # the create_folder arg is just to allow the unit tests avoid having side
    # effects

    # if no outfolder use tempdir and delete afterwards
    if not outfolder:
        process_id = str(getpid())
        outfolder = path_join(gettempdir(), "widediaper", r_pid)
        atexit.register(lambda: call("rm -rf {}".format(outfolder), shell=True))

    # if outfolder relative path store in directory of calling script + relative path
    if not isabs(outfolder):
        outfolder = handle_dots_and_tildes_in_path(outfolder)
        outfolder = path_join(getcwd(), outfolder)
    # if path was absolute do nothing

    if create_folder:
        call("rm -rf {}".format(outfolder), shell=True)
        call("mkdir -p {}".format(outfolder), shell=True)

    return outfolder


def get_df_path(session_folder, description, name):

    basename = "_".join([description, name]) + ".csv"

    return path_join(session_folder, basename)


def handle_dots_and_tildes_in_path(outfolder):

    if outfolder.startswith("~"):
        outfolder = expanduser(outfolder)
    elif outfolder.startswith("."):
        outfolder = realpath(outfolder)

    return outfolder
