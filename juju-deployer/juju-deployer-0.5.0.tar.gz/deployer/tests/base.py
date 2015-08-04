import inspect
import logging
import os
import unittest
import shutil
import StringIO
import tempfile

import deployer
from deployer.config import ConfigStack


# Skip during launchpad recipe package builds (DEB_BUILD_ARCH) or if explicitly
# requested with 'TEST_OFFLINE=1'
TEST_OFFLINE = ("DEB_BUILD_ARCH" in os.environ or "TEST_OFFLINE" in os.environ)
TEST_OFFLINE_REASON = "Requires configured bzr launchpad id and network access"
skip_if_offline = unittest.skipIf(TEST_OFFLINE, TEST_OFFLINE_REASON)


class Base(unittest.TestCase):

    test_data_dir = os.path.join(
        os.path.dirname(inspect.getabsfile(deployer)), "tests", "test_data")

    @classmethod
    def setUpClass(cls):
        os.environ["JUJU_HOME"] = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.environ["JUJU_HOME"])

    def get_named_deployment_v3(self, file_name, stack_name):
        """ Get v3 deployment from a test_data file.
        """
        return ConfigStack(
            [os.path.join(
                self.test_data_dir, file_name)]).get(stack_name)

    def get_deployment_v4(self, file_name):
        """Get v4 deployment from a test_data file.
        """
        f = os.path.join(self.test_data_dir, 'v4', file_name)
        return ConfigStack([f]).get(f)

    def capture_logging(self, name="", level=logging.INFO,
                        log_file=None, formatter=None):
        if log_file is None:
            log_file = StringIO.StringIO()
        log_handler = logging.StreamHandler(log_file)
        if formatter:
            log_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(log_handler)
        old_logger_level = logger.level
        logger.setLevel(level)

        @self.addCleanup
        def reset_logging():
            logger.removeHandler(log_handler)
            logger.setLevel(old_logger_level)
        return log_file

    def mkdir(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        return d

    def change_environment(self, **kw):
        """
        """
        original_environ = dict(os.environ)

        @self.addCleanup
        def cleanup_env():
            os.environ.clear()
            os.environ.update(original_environ)

        os.environ.update(kw)
