import os
import logging

from . import loader
from nose import plugins

LOG = logging.getLogger('nose.' + __name__)


class NoseScriptUnit(plugins.Plugin):
    name = "jscriptunit"

    def options(self, parser, env):
        super(NoseScriptUnit, self).options(parser, env)
        parser.add_option("--jscriptunit-paths",
                          dest="require_paths",
                          action="append",
                          default=env.get('JSCRIPTUNIT_PATHS'),
                          help="allow requires from those paths")

    def wantFile(self, path):
        basename = os.path.basename(path)
        if basename.endswith('.js'):
            return bool(self.conf.testMatch.match(basename))

    def loadTestsFromFile(self, filename):
        return loader.TestRunner(filename, self.conf).load_tests()
