#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Script to deploy CW cubes necessary to start a new study:
    * The 'CW_CUBES_PATH' environment variable must be set to augment
      the default search path for cubes: one extra path expected
    * At least one json configuration file .conf containing version
      information and dependencies must be placed in the 'configs' folder.
    * Install logs are printed.
    * To get some help: python piws_setup.py -h.
"""

# System import
from __future__ import with_statement
import os
import platform
import sys
import subprocess
import logging
import optparse
import json
import apt
import glob
import shutil


# Define global map for the logging level
LEVELS = {
    "info": logging.INFO,
    "debug": logging.DEBUG
}


# Define the script logger
logger = logging.getLogger(os.path.basename(__file__))


# Parsing terminal
usage = "%prog [options]"
parser = optparse.OptionParser(usage=usage, version="%prog 1.0")
parser.add_option("-d", "--directory", dest="clone_directory",
                  help="Specify the directory where the cubes will be cloned.",
                  metavar="DIR", default=None)
parser.add_option("-l", "--level", dest="debug_level",
                  type="choice", choices=["debug", "info"],
                  help="Set the debug level.",
                  default="info")
(options, args) = parser.parse_args()


# Check a valid 'CW_CUBES_PATH' has been set
cubes_paths = os.environ.get("CW_CUBES_PATH", None)
if cubes_paths is None:
    raise Exception("The 'CW_CUBES_PATH' environment variable need to be set.")
platform = platform.system()
if platform == "Linux":
    cubes_paths = cubes_paths.split(":")
else:
    raise Exception("The '{0}' platform is not supported.".format(platform))
if len(cubes_paths) != 1:
    raise Exception("Only one extra path expected in the 'CW_CUBES_PATH' "
                    "({0}) environment variable.".format(cubes_paths))
cubes_path = cubes_paths[0]
if not os.access(cubes_path, os.W_OK):
    raise Exception(
        "No valid folder for writing found in '{0}'. The 'CW_CUBES_PATH' "
        "environment variable has not been set properly.".format(cubes_paths))

# Check the clone directory exists
if options.clone_directory is None or not os.path.isdir(options.clone_directory):
    raise ValueError(
        "'{0}' is not a valid folder, cubes can't be cloned.".format(
            options.clone_directory))

# Set logging options
logging.basicConfig(
    level=LEVELS[options.debug_level],
    format="{0}::%(asctime)s :: %(levelname)s :: %(message)s".format(
        logger.name))


def check_configuration_integrity(json_data, file_name):
    """ Checks the integrity of data loaded from a json configuration file
    according to expected keys and types.

    Parameters
    ----------
    json_data : dict
        data to be checked.
    file_name : string
        path to the file the json_data was loaded from.
    """
    expected_types = {
        "version": [unicode, None],
        "hg_cubes": [dict],
        "git_cubes": [dict],
        "pypi_tools": [list]
    }

    # Check all fields no matter what
    fails = 0   
    for field_name, field_types in expected_types.items():
        if field_name not in json_data:
            print("In file : {0} :"
                  " Key '{1}' is missing".format(file_name, key))
            fails += 1
        elif type(json_data[field_name]) not in field_types:
            print("In file : {0} : Wrong type for value associated "
                  "to key '{1}' : expected {2} got {3}.".format(
                      file_name, field_name, field_types,
                      type(json_data[field_name])))
            fails += 1

    # Exit if an error has occured
    if fails != 0:
        print("Config file data is corrupted!")
        sys.exit()


def load_configuration(file_name):
    """ Loads data from a json configuration file and checks its integrity.

    Parameters
    ----------
    file_name : string
        the path to the json file to be loaded.

    Returns
    -------
    json_data : dict
        the configuration object.
    """
    try:
        with open(file_name) as json_file:
            json_data = json.load(json_file)
    except IOError:
        logger.info("Unable to load Json file %s", file_name)
        sys.exit()
    else:
        check_configuration_integrity(json_data, file_name)
        return json_data


def choose_version_to_install(config_folder):
    """ Checks from config files and displays available version to be installed.
    Lets the user choose one if any.

    Parameters
    ----------
    config_folder : string
        the path to the folder containing .conf configuration files.

    Returns
    -------
    file_names : string
        the path to the chosen configuration file.
    """
    print("Loading configuration files in '{0}' ...".format(config_folder))

    # List all available configurations
    config_files = glob.glob(os.path.join(config_folder, "*.conf"))

    if config_files:

        # Get all the possible choices
        available_versions = []
        files_names = []
        for config_file in config_files:
            json_data = load_configuration(config_file)
            version = json_data["version"]
            available_versions.append(version)
            files_names.append(config_file)
        version_choices = dict(enumerate(available_versions))

        # Diplay user options
        print("Please choose the CubicWeb setup version:")
        print("CHOICE  -----  VERSION -----  CONFIG FILE")
        for key, value in version_choices.iteritems():
            print("< {0:2} >  -----  {1:6}  -----  {2:11}".format(
                key, value, os.path.basename(files_names[int(key)])))

        # Waiting for a valid choice
        while True:
            print("Please enter your choice:")
            user_input = raw_input()
            try:
                choice = version_choices[int(user_input)]
            except:
                print("'{0}' is not a valid choice!".format(user_input))
            else:
                print("Setup version '{0}'.".format(choice))
                return files_names[int(user_input)]
    else:
        print("No configuration file was found!")
        sys.exit()


def check_call_with_log(command, **kwargs):
    """ Performs a similar call as check_call but writes command output and
    status to the terminal with different logging levels.

    Parameters
    ----------
    command : string
        the command to be executed.
    kwargs : dict
        extra arguments passed to subprocess such as execution directory (cwd).
    """
    logger.debug("--- COMMAND ---")
    logger.debug(" ".join(command))
    logger.debug("CWD =" + kwargs.get("cwd", os.getcwd()))
    logger.debug("--- OUTPUT ---")

    # Call the command in a subprocess
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         **kwargs)
    stdout, stderr = p.communicate()

    # Log the process return set
    if stdout:
        logger.debug(stdout)
    if stderr:
        logger.error(stderr)
    logger.debug("--- COMMAND STATUS = %s ---", p.returncode)

    # Reproduce the check_call behaviour
    if p.returncode:
        raise subprocess.CalledProcessError(p.returncode, command)


def hg_dl(package_url, package_name, package_version, package_folder):
    """ Clone a mercurial reporsitory and set the required version.

    Parameters
    ----------
    package_url : string
        the package url.
    package_name : string
        the package name.
    package_version: string
        the package version.
    package_folder: string
        the path where the package is cloned.
    """
    # Clone the repository
    cmd = ["hg", "clone", package_url, package_folder]
    check_call_with_log(cmd)

    # Update to specified version
    if package_version is not None:
        cmd = ["hg", "update", "--cwd", package_folder, package_version]
        check_call_with_log(cmd)


def git_dl(package_url, package_name, package_version, package_folder):
    """ Clone a git reporsitory and set the required version.

    Parameters
    ----------
    package_url : string
        the package url.
    package_name : string
        the package name.
    package_version: string
        the package version.
    package_folder: string
        the path where the package is cloned.
    """
    # Clone the repository
    cmd = ["git", "clone", package_url, package_folder]
    check_call_with_log(cmd)

    # Update to specified version
    if package_version is not None:
        cmd = ["git", "checkout", package_version]
        check_call_with_log(cmd, cwd=package_folder)


############################################################################
# Script global parameters
############################################################################

# Get configuration directory: also works if the script is called from
# another script
config_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "configs")


############################################################################
# Display user options
############################################################################

# Checking configuration files and choosing one
json_file = choose_version_to_install(config_folder)


############################################################################
# Load installation metadata
############################################################################

# Loading data from configuration file
json_data = load_configuration(json_file)
version = json_data["version"]
hg_cubes = json_data["hg_cubes"]
git_cubes = json_data["git_cubes"]
pypi_tools = json_data["pypi_tools"]


############################################################################
# Cubes setup
############################################################################

# > install pypi extra tools
logger.info("Installing python modules...")
for tool_name in pypi_tools:
    logger.info("    > %s.", tool_name)
    cmd = ["pip", "install", tool_name]
    check_call_with_log(cmd)

# > export extra cubes
logger.info("Exporting cubes in '%s'...", cubes_path)
for repo_type, cubes in [("hg", hg_cubes), ("git", git_cubes)]:
    for package_url, package_item in cubes.items():
        package_name, package_version, cube_relative_path = package_item
        cube_folder = os.path.join(cubes_path, package_name)
        package_folder = os.path.join(options.clone_directory, package_name)
        package_cube_folder = os.path.join(package_folder, cube_relative_path)
        logger.info("    > %s (version %s).", package_name, package_version)
        if not os.path.lexists(cube_folder):
            if not os.path.isdir(package_folder):
                if repo_type == "hg":
                    hg_dl(package_url, package_name, package_version,
                          package_folder)
                elif repo_type == "git":
                    git_dl(package_url, package_name, package_version,
                           package_folder)
                else:
                    raise Exception(
                        "Unknown '{0}' repository type.".format(repo_type))
            else:
                pkginfo = os.path.join(package_cube_folder, "__pkginfo__.py")
                if os .path.isfile(pkginfo):
                    cube_info = {}
                    execfile(pkginfo, cube_info)
                    logger.info("Cube '%s' already cloned with version '%s', "
                                "skip...", package_name, cube_info["version"])
                else:
                    raise Exception("'{0}' folder do not contain a cube, please "
                                    "investigate.".format(package_cube_folder))
            logger.debug("symlink: %s -> %s.", package_cube_folder, cube_folder)
            os.symlink(package_cube_folder, cube_folder)
        else:
            pkginfo = os.path.join(cube_folder, "__pkginfo__.py")
            if os .path.isfile(pkginfo):
                cube_info = {}
                execfile(pkginfo, cube_info)
                logger.info("Cube '%s' already exported with version '%s', "
                            "skip...", package_name, cube_info["version"])
            else:
                raise Exception("'{0}' folder do not contain a cube, please "
                                "investigate.".format(cube_folder))
