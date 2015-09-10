# -*- coding: utf-8 -*-
import sys
from time import sleep
from peltak.actions import actions
from peltak.core import git


@actions.register(
    'mr-cleanup',
    desc=("Cleanup after merged MR. It will remove the merged branch localy "
          "and remotely. If the user was on the deleted branch, it will "
          "checkout master first")
)
def mr_cleanup(app):
    sys.stdout.write('Pushing in 3..')
    sys.stdout.flush()
    sleep(1)
    sys.stdout.write('\rPushing in 2..')
    sys.stdout.flush()
    sleep(1)
    sys.stdout.write('\rPushing in 1..')
    sys.stdout.flush()
    sleep(1)
    sys.stdout.write('\r' + (' ' * 80) + '\r')
    sys.stdout.flush()
    sleep(1)
    git.push_current()

