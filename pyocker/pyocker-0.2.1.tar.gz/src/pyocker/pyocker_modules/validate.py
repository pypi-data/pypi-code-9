#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

def validate_image_directive(image):
    valid = True
    if 'name' not in image:
        sys.stderr.write(' * Cannot find `name` for image.\n')
        valid = False

    return valid

def validate_config(cwd, config, verbose=True):
    valid = True
    if 'images' not in config:
        sys.stderr.write(' * Cannot find `images` directive.\n')
        valid = False
    else:
        for image in config['images']:
            if not validate_image_directive(image):
                valid = False

    if not is_files_exist(cwd, config['images']):
        valid = False

    if not valid:
        sys.stderr.write("Validation failed.\n")
        exit()
    else:
        sys.stdout.write("Validation succeeded.\n")
        sys.stdout.write('---\n')

    return

def is_files_exist(cwd, images):
    valid = True
    for image in images:
        if 'build' in image and image['build']:
            if not os.path.exists(os.path.join(cwd, image['name'], 'Dockerfile')):
                sys.stderr.write('* Cannot find Dockerfile for %s\n' % image['name'])
                valid = False
            if 'dependencies' in image:
                if not is_files_exist(cwd, image['dependencies']):
                    valid = False
    return valid
