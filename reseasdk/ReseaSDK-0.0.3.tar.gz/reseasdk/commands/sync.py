import os
import subprocess
from glob import glob
from reseasdk.helpers import info, error


def sync():
    # XXX
    cwd = os.path.realpath(os.getcwd())
    os.chdir('packages')
    for d in glob('*'):
        os.chdir(d)
        if os.path.realpath(os.getcwd()) == cwd:
            continue

        info("git: pulling '{}'".format(d))
        p = subprocess.Popen(['git', 'pull'])
        p.wait()
        if p.returncode != 0:
            error("git: failed to pull '{}'".format(d))
        os.chdir('..')


def main(args):
    sync()
