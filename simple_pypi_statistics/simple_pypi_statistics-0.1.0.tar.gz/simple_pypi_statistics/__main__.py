"""simple-pypi-statistics

Usage:
  simple-pypi-statistics [options] [verbose|json] <pypi-package>...
  simple-pypi-statistics (-h | --help)
  simple-pypi-statistics --version

Options:
  --no-honeypot   Do not use honeypot for correcting bot/mirror pollution
                  [default: False]
  -h --help       Show this screen.
  --version       Show version.

Examples:
  simple-pypi-statistics docopt  # Outputs everything about docopt
  simple-pypi-statistics docopt==0.1  # Outputs a specific version
  simple-pypi-statistics json docopt==0.1  # In JSON!

Credits:
  Benjamin Bach -- updated script with honey pot corrections
  Alex Clark -- for making vanity, which this script is based on

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import locale

from docopt import docopt

logger = logging.getLogger('simple-pypi-statistics')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

from . import __version__
from . import api


if __name__ == '__main__':
    arguments = docopt(__doc__, version='simple-pypi-statistics ' + __version__)

    # Input:
    # package==0.1
    # package==0.2
    # Gives:
    # all_packages = {
    #     'package': {'0.1': ..., '0.2': ...}
    # }
    all_packages = {}

    for package in arguments['<pypi-package>']:
        result, grand_total, version = api.get_stats(package)
        if package not in all_packages:
            all_packages[package] = {}
        all_packages[package][version] = (result, grand_total)

    if not arguments['--no-honeypot']:
        pass
        # honey_pot = api.get_stats('python-bogus-project-honeypot')

    if arguments['json']:

        print(json.dumps(all_packages))

    # Be verbose by default
    else:
        for package, versions in all_packages.items():
            for version, (stats, grand_total) in versions.items():
                # http://stackoverflow.com/questions/873327/\
                # pythons-most-efficient-way-to-choose-longest-string-in-list
                releases = []
                for item in stats['releases']:
                    downloads = locale.format("%d", item['downloads'], grouping=True)
                    releases.append(
                        '%s    %s    %9s' % (
                            item['filename'], item['upload_time'], downloads
                        )
                    )
                longest = len(max(releases, key=len))
                for item in releases:
                    logger.debug(item.rjust(longest))
                logger.debug('-' * longest)
                if grand_total != 0:
                    if version:
                        logger.debug(
                            '%s %s has been downloaded %s times!' %
                            (package, version, locale.format(
                                "%d", grand_total, grouping=True)))
                    else:
                        logger.debug(
                            '%s has been downloaded %s times!' %
                            (package, locale.format("%d", grand_total, grouping=True)))
                else:
                    if version:
                        logger.debug('No downloads for %s %s.' % (package, version))
                    else:
                        logger.debug('No downloads for %s.' % package)

                # Add a blank line for read-ability
            print("")
