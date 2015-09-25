import os
import giwyn.lib.settings.settings

from os.path import expanduser

from giwyn.lib.config.config import open_config_file
from giwyn.lib.config.config import add_new_path
from giwyn.lib.config.config import close_config_file

def scan():
    """
    Function to scan the directory from the home dir, or the repository given as parameter by the user
    """

    #Update the field which contains all directories from the home dir of the user, or the directory to scan
    if giwyn.lib.settings.settings.ARGS.scan == "~" or giwyn.lib.settings.settings.ARGS.rescan:
        default_walk_from = os.walk(expanduser("~"))
    else:
        default_walk_from = os.walk(giwyn.lib.settings.settings.ARGS.scan) or os.walk(giwyn.lib.settings.settings.ARGS.rescan)

    #Open the configuration file
    f = open_config_file()

    for path, dirs, files in default_walk_from:
        for d in dirs:
            if giwyn.lib.settings.settings.ARGS.debug:
                print("current : {0}".format(os.path.join(path, d)))
            if d == ".git":
                if not path in giwyn.lib.settings.settings.CONFIG_FILE_CONTENT:
                    add_new_path(f, path)
                #If debug mod, print out the path file
                if giwyn.lib.settings.settings.ARGS.debug:
                    print("\t FIND {0}".format(os.path.join(path, d)))

    #Close the configuration file
    close_config_file(f)
