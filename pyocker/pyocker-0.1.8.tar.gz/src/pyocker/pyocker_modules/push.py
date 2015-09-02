# -*- coding: utf-8 -*-

import os
import sys
from datetime import date
from subprocess import call, Popen, PIPE

DATE = date.today()
DATE_STR = str(DATE.year).zfill(4) + '.' + str(DATE.month).zfill(2) + '.' + str(DATE.day).zfill(2)

def single_push(directory, commands, verbose=True, dry=True):
    if dry:
        sys.stdout.write(' * [dry-run] Pushing image %s.\n' % commands[-1])
    else:
        p = Popen(commands, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=directory)
        output, err = p.communicate()
        rc = p.returncode
        if verbose:
            sys.stdout.write("%s\n" % output)
            sys.stderr.write("%s\n" % err)
        if rc == 0:
            sys.stdout.write(' * Pushing image "%s" succeeded.\n' % commands[-1])
        else:
            sys.stderr.write(' * Pushing image "%s" failed.\n' % commands[-1])
            exit()

def push(cwd, registry_str, image, verbose=True, dry=True):
    # Push dependencies first
    if 'dependencies' in image:
        for dep in image['dependencies']:
            push(os.path.join(cwd, dep['name']), registry_str, dep, verbose=verbose)

    # Push this image
    directory = os.path.join(cwd, image['name'])
    if 'push' in image and image['push']:
        commands_base = ['docker', 'push']
        if 'tags' in image:
            for tag in image['tags']:
                commands = list(commands_base)
                tag = tag.replace('$date', DATE_STR)
                commands.append('%s%s:%s' % (registry_str, image['name'], tag))
                single_push(directory, commands, verbose=verbose, dry=dry)
        else:
            commands = list(commands_base)
            commands.append('%s%s' % (registry_str, image['name']))
            single_push(directory, commands, verbose=verbose, dry=dry)

    return
