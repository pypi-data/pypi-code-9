#!/usr/bin/env python

import os
import sys

from django.core.management.base import BaseCommand


class ProgressdCommand(BaseCommand):
    help = 'Start progressd application'

    options = BaseCommand.option_list
    skip_opts = ['--app', '--loader', '--config', '--no-color']
    requires_model_validation = False
    keep_base_opts = False
    stdout, stderr = sys.stdout, sys.stderr

    def run_from_argv(self, argv):
        self.handle_default_options(argv[2:])
        return super(ProgressdCommand, self).run_from_argv(argv)

    def handle_default_options(self, argv):
        acc = []
        broker = None
        for i, arg in enumerate(argv):
            # --settings and --pythonpath are also handled
            # by BaseCommand.handle_default_options, but that is
            # called with the resulting options parsed by optparse.
            if '--settings=' in arg:
                _, settings_module = arg.split('=')
                os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
            elif '--pythonpath=' in arg:
                _, pythonpath = arg.split('=')
                sys.path.insert(0, pythonpath)
            elif '--broker=' in arg:
                _, broker = arg.split('=')
            elif arg == '-b':
                broker = argv[i + 1]
            else:
                acc.append(arg)
        if broker:
            self.set_broker(broker)
        return argv if self.keep_base_opts else acc

    def run_from_argv(self, argv):
        argv = self.handle_default_options(argv)
        if self.requires_model_validation:
            self.validate()
        base.execute_from_commandline(
            ['{0[0]} {0[1]}'.format(argv)] + argv[2:],
            )
