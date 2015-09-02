#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################
#                   dependency_builder                      #
# Build & Push Docker Images in order based on dependencies #
#############################################################

import os
import sys
import yaml
import time
from optparse import OptionParser
from datetime import date
from subprocess import call, Popen, PIPE

CWD = os.getcwd()
SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

# sys.path.append(os.path.join(SCRIPTDIR, 'modules'))
from pyocker_modules.parse import parse_config
from pyocker_modules.validate import validate_config
from pyocker_modules.build import build
from pyocker_modules.push import push

def build_and_push(config, verbose=True, dry=True):
    if 'registry' in config:
        registry_str = "%s/" % config['registry']
    else:
        registry_str = ""
    for image in config['images']:
        if 'build' in image and image['build']:
            sys.stdout.write('Building image %s...\n' % image['name'])
            build(CWD, registry_str, image, verbose=verbose, dry=dry)
            sys.stdout.write('---\n')
        else:
            sys.stdout.write('Skipping `build` for image "%s"...\n' % image['name'])
            sys.stdout.write('---\n')
        if 'push' in image and image['push']:
            sys.stdout.write('Pushing image %s...\n' % image['name'])
            push(CWD, registry_str, image, verbose=verbose, dry=dry)
            sys.stdout.write('---\n')
        else:
            sys.stdout.write('Skipping `push` for image "%s"...\n' % image['name'])
            sys.stdout.write('---\n')

def main():
    parser = OptionParser()
    parser.set_defaults(verbose=True)
    parser.set_defaults(dry=False)
    parser.add_option("-f", "--file", dest="filename", type="string", metavar="FILE", help="Path to config file [default=`docker-dependency.yml`]", default="docker-dependency.yml", action="store")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Make lots of noise [default]")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", help="Make less noise")
    parser.add_option("--dry-run", dest="dry", action="store_true", help="Dry Run")
    (options, args) = parser.parse_args()

    config = parse_config(os.path.join(CWD, options.filename))
    validate_config(CWD, config, verbose=options.verbose)
    build_and_push(config, verbose=options.verbose, dry=options.dry)

if __name__=="__main__":
    main()
