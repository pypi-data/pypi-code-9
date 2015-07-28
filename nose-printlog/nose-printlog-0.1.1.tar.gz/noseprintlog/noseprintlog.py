"""Print log to stderr. Enabled by --with-printlog"""

import logging
import os
import sys

from nose.plugins import Plugin
log = logging.getLogger('nose.plugins.printlog')


class PrintLog(Plugin):
    name = 'printlog'
    _handler_prefix = 'nose_printlog_'

    def options(self, parser, env=os.environ):
        super(PrintLog, self).options(parser, env=env)

    def configure(self, options, conf):
        super(PrintLog, self).configure(options, conf)
        if not self.enabled:
            return

    @classmethod
    def _get_handler_id(cls, test):
        return cls._handler_prefix + repr(test)

    def beforeTest(self, test):
        sys.stderr.write('\n')  # Make sure not to append to other lines
        root_logger = logging.getLogger()
        handler = logging.StreamHandler(sys.stderr)
        handler.set_name(self._get_handler_id(test))
        root_logger.addHandler(handler)

    def afterTest(self, test):
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            if handler.get_name() == self._get_handler_id(test):
                root_logger.removeHandler(handler)
                return
