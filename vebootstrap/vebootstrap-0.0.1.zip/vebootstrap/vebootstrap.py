# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
from os import path


MAIN_DIR = path.dirname(path.abspath(sys.argv[0]))
MAJOR_VERSION = sys.version_info[0]
REQUIREMENTS = "requirements.txt"
REQUIREMENTS_PATH = path.join(MAIN_DIR, REQUIREMENTS)
DEVNULL = open(os.devnull, 'w')


#
# os detection
#
if os.name == 'nt':
    BIN_PATH = "Scripts"
    PATH_SEPARATOR = ";"
    SHELL = True
else:
    BIN_PATH = "bin"
    PATH_SEPARATOR = ":"
    SHELL = False


def shell_execute(cmd, env=None, stdout=None):
    new_env = os.environ.copy()
    if env:
        new_env.update(env)
    return subprocess.call(cmd, env=new_env, shell=SHELL, stdout=stdout)


def create_venv(pyvenv_dir):
    virtualenv = "virtualenv" if MAJOR_VERSION == 2 else "venv"
    if shell_execute([sys.executable, "-m", virtualenv, pyvenv_dir]) != 0:
        raise Exception("cannot create virtualenv")

    if not os.access(REQUIREMENTS_PATH, os.F_OK):
        open(REQUIREMENTS_PATH, "wb").close()


def pip_install(pyvenv_dir):
    last_requirements = path.join(pyvenv_dir, REQUIREMENTS)
    shutil.copy(REQUIREMENTS_PATH, last_requirements)
    activate_venv(pyvenv_dir, ["pip", "install", "vebootstrap"])
    activate_venv(pyvenv_dir, ["pip", "install", "-r", REQUIREMENTS_PATH])


def pip_uninstall(pyvenv_dir):
    last_requirements = path.join(pyvenv_dir, REQUIREMENTS)
    activate_venv(pyvenv_dir, ["pip", "uninstall", "-r", last_requirements, "-y"])


def should_update_packages(pyvenv_dir):
    def get_updated_time(filename):
        from datetime import datetime
        stat = os.stat(filename)
        return stat.st_mtime

    old_package_updated_time = get_updated_time(path.join(pyvenv_dir, REQUIREMENTS))
    new_package_updated_time = get_updated_time(REQUIREMENTS_PATH)
    return old_package_updated_time < new_package_updated_time


def activate_venv(pyvenv_dir, cmd):
    return shell_execute(cmd,
        {"PATH": path.join(pyvenv_dir, BIN_PATH) + PATH_SEPARATOR + os.environ['PATH'],
            "VIRTUAL_ENV": path.abspath(pyvenv_dir)
            })


def bootstrap():
    BOOTSTRAP_OPTION = "--vebootstrapped-V8guR5ySAymI" # random string
    if BOOTSTRAP_OPTION in sys.argv:
        sys.argv.remove(BOOTSTRAP_OPTION)
        return

    sys.argv.append(BOOTSTRAP_OPTION)
    pyvenv_dir = path.join(MAIN_DIR, "__pyvenv__")

    if not os.access(pyvenv_dir, os.F_OK):
        create_venv(pyvenv_dir)
        pip_install(pyvenv_dir)
    elif should_update_packages(pyvenv_dir):
        pip_uninstall(pyvenv_dir)
        pip_install(pyvenv_dir)

    sys.exit(activate_venv(pyvenv_dir, ["python"] + sys.argv))


bootstrap()

