import argparse
import lib.settings.settings
import os

from os.path import expanduser

from lib.git.commands import list_git_projects
from lib.git.commands import push_ready_projects

from lib.scan import scan

from lib.config.config import open_config_file
from lib.config.config import clean_config_file
from lib.config.config import close_config_file
from lib.config.config import delete_path_from_config_file

from lib.git.git import GitObj

def load_paths_from_config_file():
    f = open_config_file()
    lib.settings.settings.CONFIG_FILE_CONTENT = f.readlines()
    close_config_file(f)

def save_git_objects():
    for entry in lib.settings.settings.CONFIG_FILE_CONTENT:
        try:
            lib.settings.settings.GIT_OBJECTS.append(GitObj(entry))
        except Exception as e:
            if lib.settings.settings.ARGS.debug:
                print("[MAIN] Exception for {0}: {1}".format(entry[:-1], e))
            f = open_config_file()
            print("Git repository {0} not found...".format(entry[:-1]))
            delete_path_from_config_file(f, entry)
            close_config_file(f)

def main():

    parser = argparse.ArgumentParser(description="Program to visualize any changes about .git projects")

    #For files
    parser.add_argument("--scan", "-s", help="Scan from the argument directory to find any git projects, and add them into the hidden configuration file")
    parser.add_argument("--rescan", "-rs", help="Rescan from the argument directory to find any git projects - this command will replace the data in the hidden configuration file by the result of the scan")

    #Action on git files
    parser.add_argument("--list", "-l", help="List all git projects", action="store_true")
    parser.add_argument("--stats", "-st", help="Get stats for each project", action="store_true")
    parser.add_argument("--push", "-p", help="Push repos which have, for a clean repository, some commits not pushed", action="store_true")

    #Debug & version
    parser.add_argument("--debug", "-d", help="Debug mod - for developer only", action="store_true")
    parser.add_argument("--version", "-v", help="Version of the program", action="store_true")

    lib.settings.settings.init()

    lib.settings.settings.ARGS = parser.parse_args()

    lib.settings.settings.CONFIG_FILE_PATH = "{0}/{1}".format(expanduser('~'), lib.settings.settings.CONFIG_FILE_NAME)

    #Create an empty file if not exists
    if not os.path.exists(lib.settings.settings.CONFIG_FILE_PATH):
        os.mknod(lib.settings.settings.CONFIG_FILE_PATH)

    load_paths_from_config_file()

    if lib.settings.settings.ARGS.rescan:
        f = open_config_file()
        clean_config_file(f)
        close_config_file(f)
        scan()
        load_paths_from_config_file()

    if lib.settings.settings.ARGS.scan:
        scan()
        load_paths_from_config_file()

    save_git_objects()

    if lib.settings.settings.ARGS.list:
        list_git_projects()

    if lib.settings.settings.ARGS.push:
        push_ready_projects()

if __name__ == '__main__':
    main()
