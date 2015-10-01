#!/usr/bin/env python

import os
import sys
import yaml
import shlex
import argparse
import subprocess


PILLOW_EXTERNAL_DEPENDENCIES = []
SCRIPTS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'scripts')
SETTINGS_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'settings')
for setting_file in os.listdir(SETTINGS_DIR):
    if setting_file.endswith('.yml'):
        filepath = os.path.join(SETTINGS_DIR, setting_file)
        PILLOW_EXTERNAL_DEPENDENCIES.append(
            yaml.load(open(filepath, 'r')))


def get_conf(distro):
    conf = {}
    for SECTIONS in PILLOW_EXTERNAL_DEPENDENCIES:
        for section in SECTIONS:
            section = SECTIONS[section]
            etc_issue = section.get('etc-issue')
            if distro == etc_issue:
                conf = section
    return conf


def get_gnu_linux_distro_conf(filepath="/etc/issue"):
    """Returns:
        - A list [] of dependencies packages to install
        - Gnu/Linux distro name and version (ex: Debian 7)
    """

    if not os.path.isfile(filepath):
        raise Exception("This Gnu/Linux distribution is not supported.")

    with open(filepath, "r") as fp:
        etc_issue = fp.readline()
        gnu_linux_distro = " ".join((
            [x for x in etc_issue.split() if not x.startswith('\\')]))

    conf = get_conf(gnu_linux_distro)
    if not conf:
        raise Exception("Unknown Gnu/Linux distribution.")

    return conf


def install_pillow_dependencies(interactive, drymode=False):
    """Install Pillow dependencies. Returns stderr, stdout.
    """

    conf = get_gnu_linux_distro_conf()
    distro = conf.get("name")
    distro_version = conf.get("version")
    pkg_cmd = conf.get('pkg-cmd')['interactive'] if interactive else \
        conf.get('pkg-cmd')['non-interactive']
    dependencies = conf.get("dependencies") + \
        conf.get("py{0}-base-deps".format(sys.version[0]))

    if not drymode:
        print("Running {0} {1}\nLets install the following dependencies:".format(
            distro, distro_version))
        for dep in dependencies:
            print("".join(("- ", dep)))

    dependencies = " ".join((dep for dep in dependencies))
    cmd = " ".join((pkg_cmd, dependencies))

    if interactive:
        confirm = raw_input('\nContinue?(Y/n) ')
        if confirm.lower() == 'y':
            stderr = stdout = exec_cmd(cmd, as_root=True)
        else:
            sys.exit(0)
    else:
        stderr, stdout = exec_cmd(cmd, as_root=True, drymode=drymode)

    if stderr:
        err_msg = "".join((
            "Error while installing Pillow external dependencies.",
            "{0}\n".format(stderr)))
        print(err_msg)
        sys.exit(1)

    return stderr, stdout


def install_pillow(interactive, drymode=False):
    """Install Pillow dependencies, then install Pillow."""
    if drymode:
        print('Run the following command as root to install needed dependencies:')
    install_pillow_dependencies(interactive, drymode)
    if drymode:
        print('To have jpeg support, run as root the following script:')
    install_openjpeg2(drymode)

    pip_executable = get_pip_executable()
    if pip_executable is None:
        raise Exception('pip not found, please install it')

    cmd = " ".join((pip_executable, "install Pillow"))
    if drymode:
        print('Finally install Pillow with the following command:')
    stderr, stdout = exec_cmd(cmd, drymode=drymode)

    return stderr, stdout


def install_openjpeg2(drymode=False):
    """Install JPEG2000 libraries."""
    script = os.path.join(SCRIPTS_DIR, 'install-openjpeg.sh')
    stderr, stdout = exec_cmd(script, as_root=True, drymode=drymode)

    if stderr:
        err_msg = "".join((
            "Error while installing openjpeg2 library.",
            "{0}\n".format(stderr)))
        print(err_msg)
        sys.exit(1)

    return stderr, stdout


def get_pip_executable():
    """Returns the fullpath to pip or None."""
    py_executable_root = os.path.split(sys.executable)[0]
    pip_path = os.path.join(py_executable_root, 'pip')
    pip_path = pip_path if os.path.exists(pip_path) else None
    return pip_path


def exec_cmd(command, as_root=None, drymode=False):
    if as_root is True and os.getuid() != 0:
        command = 'su -c "{0}"'.format(command)

    if drymode:
        print(command)
        print('')
        stderr = stdout = ''
        return stderr, stdout 

    command = shlex.split(command)

    process = subprocess.Popen(
        command,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        bufsize=1
    )
    for line in iter(process.stdout.readline, b''):
        print(line.strip())

    stderr, stdout = process.communicate()
    return stderr, stdout


def main():
    parser = argparse.ArgumentParser(
        description="Pimp My Pillow")
    parser.add_argument('install',
                        help="Install Pillow")
    parser.add_argument('--interactive',
                        action='store_true',
                        help="Be interactive")
    parser.add_argument('--drymode',
                        action='store_true',
                        help="Dumps cli commands but dont install anything")
    args_ = parser.parse_args()
    stderr = ''

    if args_.install:
        stderr, stdout = install_pillow(args_.interactive, drymode=args_.drymode)

    if stderr:
        err_msg = "".join((
            "Error while installing Pillow external dependencies.",
            "{0}\n".format(stderr)))
        print(err_msg)
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
