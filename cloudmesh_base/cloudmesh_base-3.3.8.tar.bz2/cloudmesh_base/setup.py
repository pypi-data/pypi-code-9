from __future__ import print_function

from cloudmesh_base.Shell import Shell
import os
import pip
import sys


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def os_execute(commands):
    for command in commands.split("\n"):
        command = command.strip()
        print(command)
        os.system(command)


def get_version_from_git():
    r = Shell.git('tag').split("\n")[-1]
    return r


def check_pip():
    major = int(pip.__version__.split(".")[0])
    if major < 7:
        print("")
        print("    ERROR: Pip version", pip.__version__, "is to old.")
        print("    Tip:   Please update pip with ")
        print("")
        print("             pip install pip -U")
        print("")
        sys.exit()
