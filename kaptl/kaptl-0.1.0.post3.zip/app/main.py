#!/usr/bin/env python

"""Usage: kaptl new [--backend=mvc] --frontend=angular [<rules> | --rules-file=RULESFILE ] [--ast]
        kaptl -h | --help
        kaptl --version

"""

from kaptl import Kaptl
from docopt import docopt

from autoupgrade import *


def main():
    try:
        AutoUpgrade("kaptl").upgrade_if_needed(True, True)  # update the deps as well and then restart the app
    except NoVersionsError:
        pass
    args = docopt(__doc__)
    kaptl = Kaptl(args)
    """
    Parse parameters and launch the proper operation
    :type arguments: object
    """
    if args["new"]:
        kaptl.create_new_app()


if __name__ == '__main__':
    "Main entry point for KAPTL CLI"
    main()
