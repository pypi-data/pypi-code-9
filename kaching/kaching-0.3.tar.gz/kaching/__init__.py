from os.path import join, dirname, realpath
from sys import stderr, argv, exit
from subprocess import Popen, PIPE
from random import randint
from os import listdir


PASS_DIR = join(dirname(realpath(__file__)), "pass")
FAIL_DIR = join(dirname(realpath(__file__)), "fail")
START_DIR = join(dirname(realpath(__file__)), "start")


def play_sound_file(sound_file):
    """Play specified sound file or raise error if mplayer doesn't work."""
    try:
        Popen(["mplayer", "-msglevel", "all=-1", sound_file], stdout=PIPE, stderr=PIPE)
    except OSError:
        stderr.write("Couldn't run mplayer. Do you have it installed?\n")
        exit(1)

def print_usage():
    """Print CLI usage."""
    stderr.write("Usage: kaching [pass | fail | start]\n")
    exit(1)


def run():
    """Run kaching."""
    wins = listdir(PASS_DIR)
    fails = listdir(FAIL_DIR)
    starts = listdir(START_DIR)

    if len(argv) == 2:
        if argv[1] == "pass":
            play_sound_file(join(PASS_DIR, wins[randint(0, len(wins) - 1)]))
        elif argv[1] == "fail":
            play_sound_file(join(FAIL_DIR, fails[randint(0, len(fails) - 1)]))
        elif argv[1] == "start":
            play_sound_file(join(START_DIR, starts[randint(0, len(starts) - 1)]))
        else:
            print_usage()
    else:
        print_usage()
