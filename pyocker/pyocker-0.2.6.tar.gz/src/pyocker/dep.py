#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

CWD = os.getcwd()

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

def main(cwd, filename, verbose=True, dry=True):
    config = parse_config(os.path.join(cwd, filename))
    validate_config(cwd, config, verbose=verbose)
    build_and_push(config, verbose=verbose, dry=dry)
