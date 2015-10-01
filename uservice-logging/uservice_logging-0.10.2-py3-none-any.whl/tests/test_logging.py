# uservice-logging
# Copyright (C) 2015 Canonical
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Tests for the logging code."""

import datetime
import json
import logging
import os.path
import subprocess
import sys
import tempfile
import threading

from textwrap import dedent

from fixtures import Fixture
from testtools import TestCase
from testtools.matchers import (
    Contains,
    Equals,
    FileContains,
    IsInstance,
    Not,
)

import uservice_logging
import uservice_logging.logging as util_logging


class LoggingConfigurationTests(TestCase):

    """Tests for the logging configuration functions.

    These tests all spawn subprocesses to examine the effect of the logging
    configuration.

    """
    def run_script(self, script_contents, run_dir, env={}):
        testfile = os.path.join(run_dir, 'test.py')
        with open(testfile, 'wt') as test_file:
            test_file.write(script_contents.format(basedir=run_dir))
        pythonpath = os.path.abspath(
            os.path.join(uservice_logging.__file__, '..', '..')
        )
        process = subprocess.Popen(
            [sys.executable, testfile],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(PYTHONPATH=pythonpath, **env),
        )
        try:
            out, err = process.communicate(timeout=10)
            return process.returncode, out.decode(), err.decode()
        except subprocess.TimeoutExpired:
            process.kill()
            raise

    def test_defaults_to_stderr(self):
        with tempfile.TemporaryDirectory() as run_dir:
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging.logging import configure_service_logging

                    configure_service_logging()
                    logging.info("Hello World")
                    """
                ),
                run_dir
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Contains("Hello World"))

    def test_fallbacks_to_stderr(self):
        with tempfile.TemporaryDirectory() as run_dir:
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging.logging import configure_service_logging

                    configure_service_logging("{basedir}/nonexistant/some.file")
                    logging.info("Hello World")
                    """
                ),
                run_dir
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Contains("Hello World"))

    def test_supports_logstash(self):
        with tempfile.TemporaryDirectory() as run_dir:
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging.logging import configure_service_logging

                    logstash_config = dict(
                        host='127.0.0.1', port='5959', version='1')
                    configure_service_logging(
                        "{basedir}/nonexistant/some.file", logstash_config)
                    logging.info("Hello World")
                    """
                ),
                run_dir
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Contains("Hello World"))

    def test_can_log_to_file(self):
        with tempfile.TemporaryDirectory() as run_dir:
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging.logging import configure_service_logging

                    configure_service_logging("{basedir}/logfile")
                    logging.info("Hello World")
                    """
                ),
                run_dir
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Equals(""))
            self.expectThat(out, Equals(""))
            self.assertThat(
                os.path.join(run_dir, 'logfile'),
                FileContains(matcher=Contains("Hello World"))
            )

    def test_silences_requests(self):
        with tempfile.TemporaryDirectory() as run_dir:
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging.logging import configure_service_logging

                    configure_service_logging("{basedir}/nonexistant/some.file")
                    logging.getLogger('requests').info("Will not see")
                    logging.getLogger('requests').warning("Will see")
                    """
                ),
                run_dir
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Not(Contains("Will not see")))
            self.expectThat(err, Contains("Will see"))

    def test_configure_logging_w_LOG_DIR(self):
        with tempfile.TemporaryDirectory() as run_dir:
            log_dir = os.path.join(run_dir, 'mylogs')
            os.makedirs(log_dir)
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging import configure_logging

                    config_w_logstash = dict(logstash=dict(
                        host='127.0.0.1', port='5959', version='1'))
                    configure_logging(config_w_logstash, service='svc',
                                      solution='sol')
                    logging.info("Hello World")
                    """
                ),
                run_dir,
                dict(LOG_DIR=log_dir)
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Equals(""))
            self.expectThat(out, Equals(""))
            self.assertThat(
                os.path.join(log_dir, 'svc.log'),
                FileContains(matcher=Contains("Hello World"))
            )

    def test__configure_service_logging__log_level(self):
        with tempfile.TemporaryDirectory() as run_dir:
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging.logging import configure_service_logging

                    configure_service_logging(level=logging.DEBUG)
                    logging.debug("Hello World")
                    """
                ),
                run_dir
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Contains("Hello World"))

    def test__configure_logging__log_level(self):
        with tempfile.TemporaryDirectory() as run_dir:
            rc, out, err = self.run_script(
                dedent(
                    """
                    import logging
                    from uservice_logging.logging import configure_logging

                    configure_logging(dict(), 'svc', logging.DEBUG)
                    logging.debug("Hello World")
                    """
                ),
                run_dir
            )
            self.expectThat(rc, Equals(0))
            self.expectThat(err, Contains("Hello World"))


class LoggerClassFixture(Fixture):

    """A fixture that sets a new logging class for the duration of a test."""

    def __init__(self, new_class):
        self._new_class = new_class

    def setUp(self):
        super().setUp()
        old_logger_class = logging.getLoggerClass()
        logging.setLoggerClass(self._new_class)
        self.addCleanup(logging.setLoggerClass, old_logger_class)


class TestingLogFilter(logging.Filter):

    """A filter that passes everything, but logs everything."""
    def __init__(self):
        self.log_records = []

    def filter(self, record):
        self.log_records.append(record)
        return 1  # Log this record.


class ExtraLoggerTests(TestCase):

    def test_can_set_logger_class(self):
        self.useFixture(LoggerClassFixture(util_logging.ExtraLogger))
        logger = logging.getLogger(__name__)
        self.assertThat(logger, IsInstance(util_logging.ExtraLogger))

    def create_log_with_filter(self, name=__name__,
                               logger_class=util_logging.ExtraLogger):
        self.useFixture(LoggerClassFixture(logger_class))
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        filt = TestingLogFilter()
        logger.addFilter(filt)
        self.addCleanup(logger.removeFilter, filt)
        return logger, filt

    def test_can_set_extra_details(self):
        logger, filt = self.create_log_with_filter()
        logger.add_extra_args(dict(foo='bar'))
        logger.info("Testing")

        self.assertThat(filt.log_records[0].foo, Equals('bar'))

    def test_extra_args_via_subclass(self):
        class XLogger(util_logging.ExtraLogger):
            extra_args = dict(bar='baz')
        logger, filt = self.create_log_with_filter(__name__ + '.x', XLogger)
        self.assertThat(logger, IsInstance(XLogger))
        logger.info("Testing")

        self.assertThat(filt.log_records[0].bar, Equals('baz'))

    def test_extra_args_prefix_via_subclass(self):
        class XLogger(util_logging.ExtraLogger):
            prefix = 'z.'
            extra_args = dict(bar='baz')
        logger, filt = self.create_log_with_filter(__name__ + '.x.z', XLogger)
        logger.info("Testing", extra=dict(a='bar'))

        self.assertThat(filt.log_records[0].bar, Equals('baz'))
        self.assertThat(getattr(filt.log_records[0], 'z.a'), Equals('bar'))

    def test_extra_args_can_be_mixed(self):
        logger, filt = self.create_log_with_filter()
        logger.add_extra_args(dict(foo='bar'))
        logger.info("Testing", extra=dict(bar='baz'))

        self.assertThat(filt.log_records[0].foo, Equals('bar'))
        self.assertThat(filt.log_records[0].bar, Equals('baz'))

    def test_log_method_extra_args_take_priority(self):
        logger, filt = self.create_log_with_filter()
        logger.add_extra_args(dict(foo='bar'))
        logger.info("Testing", extra=dict(foo='baz'))

        self.assertThat(filt.log_records[0].foo, Equals('baz'))

    def test_extra_args_additive_and_reset(self):
        class XLogger(util_logging.ExtraLogger):
            extra_args = dict(bar='baz')
        logger, filt = self.create_log_with_filter(__name__ + '.x.add', XLogger)
        logger.add_extra_args(dict(foo='bar'))
        logger.info("Testing")

        self.assertThat(filt.log_records[0].bar, Equals('baz'))
        self.assertThat(filt.log_records[0].foo, Equals('bar'))

        logger.reset_extra_args()
        logger.info("Testing")

        self.assertThat(filt.log_records[1].bar, Equals('baz'))
        self.assertFalse(hasattr(filt.log_records[1], 'foo'))

    def test_extra_args_thread_safe(self):
        class XLogger(util_logging.ExtraLogger):
            extra_args = dict(bar='baz')
        logger, filt = self.create_log_with_filter(__name__ + '.x.safe', XLogger)
        logger.add_extra_args(dict(foo='from1'))

        def t2():
            logger.add_extra_args(dict(foo='from2'))
            logger.info("Testing")
        th2 = threading.Thread(target=t2)
        th2.start()
        th2.join()
        logger.info("Testing")

        self.assertThat(filt.log_records[0].bar, Equals('baz'))
        self.assertThat(filt.log_records[0].foo, Equals('from2'))
        self.assertThat(filt.log_records[1].bar, Equals('baz'))
        self.assertThat(filt.log_records[1].foo, Equals('from1'))


class SafeEncodingTests(TestCase):
    """Test the safe encoder.

    Always decode to check equality so order is not a problem.
    """

    def test_simple(self):
        raw = util_logging.safe_serializer(dict(foo='bar'))
        resp = json.loads(raw.decode('utf8'))
        self.assertEqual(resp, {"foo": "bar"})

    def test_datetime_simple(self):
        dt = datetime.datetime(2015, 8, 20)
        raw = util_logging.safe_serializer(dict(foo='bar', date=dt))
        resp = json.loads(raw.decode('utf8'))
        self.assertEqual(resp, {"foo": "bar", "date": "2015-08-20T00:00:00"})

    def test_datetime_deep(self):
        dt = datetime.datetime(2015, 8, 20)
        raw = util_logging.safe_serializer(dict(foo='bar', info=dict(date=dt)))
        resp = json.loads(raw.decode('utf8'))
        self.assertEqual(resp, {"foo": "bar", "info": {"date": "2015-08-20T00:00:00"}})

    def test_whatever_object(self):
        class Whatever(object):
            def __repr__(self):
                return 'test repr'

        raw = util_logging.safe_serializer(dict(foo='bar', obj=Whatever()))
        resp = json.loads(raw.decode('utf8'))
        self.assertEqual(resp, {"foo": "bar", "obj": "test repr"})

    def test_crashing_repr(self):
        class Whatever(object):
            def __repr__(self):
                return ValueError("pumba")

        raw = util_logging.safe_serializer(dict(foo='bar', obj=Whatever()))
        unrep_msg = json.loads(raw.decode('utf8'))['obj']
        self.assertIn("Unrepresentable", unrep_msg)
        self.assertIn("Whatever", unrep_msg)
