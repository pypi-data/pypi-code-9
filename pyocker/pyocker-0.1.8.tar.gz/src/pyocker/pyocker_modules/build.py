# -*- coding: utf-8 -*-

import os
import sys
from datetime import date
from subprocess import call, Popen, PIPE

DATE = date.today()
DATE_STR = str(DATE.year).zfill(4) + '.' + str(DATE.month).zfill(2) + '.' + str(DATE.day).zfill(2)

def single_build(directory, commands, verbose=True, dry=True):
    if dry:
        sys.stdout.write(' * [dry-run] Building image "%s".\n' % commands[-2])
    else:
        p = Popen(commands, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=directory)
        output, err = p.communicate()
        rc = p.returncode
        if verbose:
            sys.stdout.write("%s\n" % output)
            sys.stderr.write("%s\n" % err)
        if rc == 0:
            sys.stdout.write(' * Building image "%s" succeeded.\n' % commands[-2])
        else:
            sys.stderr.write(' * Building image "%s" failed.\n' % commands[-2])
            exit()

def build(cwd, registry_str, image, verbose=True, dry=True):
    # Build dependencies first
    if 'dependencies' in image:
        for dep in image['dependencies']:
            build(os.path.join(cwd, dep['name']), registry_str, dep, verbose=verbose)

    # Build this image
    directory = os.path.join(cwd, image['name'])
    if 'build' in image and image['build']:
        commands_base = ['docker', 'build']
        if 'use_cache' in image and not image['use_cache']:
            commands_base.append('--no-cache')
        commands_base.append('-t')
        if 'tags' in image:
            for tag in image['tags']:
                commands = list(commands_base)
                tag = tag.replace('$date', DATE_STR)
                commands.append('%s%s:%s' % (registry_str, image['name'], tag))
                commands.append('.')
                single_build(directory, commands, verbose=verbose, dry=dry)
        else:
            commands = list(commands_base)
            commands.append('%s%s' % (registry_str, image['name']))
            commands.append('.')
            single_build(directory, commands, verbose=verbose, dry=dry)

    return
