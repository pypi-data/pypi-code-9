"""Complete destroys the environment:

    * remove all created images and container (like reset command)
    * removes the directory
"""
from __future__ import print_function
import os
import shutil

from . import reset


NEEDS_ENVIRONMENT = True


class _ResetOptions(object):
    def __init__(self,
                 config_file,
                 environment_path,
                 quiet=False,
                 hard_reset=True):
        self.quiet            = quiet
        self.hard_reset       = hard_reset
        self.config_file      = config_file
        self.environment_path = environment_path


def run_command(options):
    if os.path.exists(options.environment_path):
        reset_options = _ResetOptions(
            options.config_file, options.environment_path)
        reset.run_command(reset_options)
        print("Destroying %s" % options.environment_path)
        shutil.rmtree(options.environment_path)

