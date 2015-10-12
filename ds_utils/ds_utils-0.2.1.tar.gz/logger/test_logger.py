import logging
import StringIO
import unittest
import boto
from moto import mock_kinesis

from . import logger


class TestLogger(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.logger = logger.Logger("test")
        cls.logger.setup()
        cls.stream = StringIO.StringIO()
        cls.handler = logging.StreamHandler(cls.stream)
        cls.handler.setFormatter(cls.logger.formatter)
        cls.logger.addHandler(cls.handler)

    def test_setup_no_kwargs(self):
        self.logger.info(hello="world")
        log = self.stream.getvalue()
        self.assertIn("hello", log)

    def test_setup_with_kwargs(self):
        self.logger.setup(foo="bar")
        self.logger.addHandler(self.handler)
        self.logger.info(hello="world")
        log = self.stream.getvalue()
        self.assertIn("hello", log)
        self.assertIn("foo", log)

    def test_silence(self):
        logger.silence("test")
        self.logger.info(hello="world")
        log = self.stream.getvalue()
        self.assertEqual("", log)

    def test_debug(self):
        self.logger.setLevel(logger.DEBUG)
        self.logger.debug(hello="world")
        log = self.stream.getvalue()
        self.assertIn("DEBUG", log)

    def test_warning(self):
        self.logger.warning(hello="world")
        log = self.stream.getvalue()
        self.assertIn("WARNING", log)

    def test_error(self):
        self.logger.error(hello="world")
        log = self.stream.getvalue()
        self.assertIn("ERROR", log)

    def test_critical(self):
        self.logger.critical(hello="world")
        log = self.stream.getvalue()
        self.assertIn("CRITICAL", log)


class TestKinesisHandler(unittest.TestCase):

    def setUp(self):
        self.logger = logger.Logger("test")
        self.logger.setup()

    def create_context(self):
        """
        This can't be done in setUp, as it needs to be called within the mock_kinesis context
        of each test.
        """
        conn = boto.connect_kinesis()
        conn.create_stream('test', 1)
        self.stream = conn.describe_stream('test')

        # Note that formatting will be removed as it will be handled in Logger class
        self.log_format = "%(asctime)s [%(levelname)s] [%(name)s] [%(process)d] %(message)s"
        self.formatter = logging.Formatter(self.log_format)
        self.handler = logger.KinesisHandler(
                        self.stream['StreamDescription']['StreamName'])
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    @mock_kinesis
    def test_can_get_connection(self):
        c = self.create_context()
        conn = self.handler.get_connection()
        self.assertIn('KinesisConnection', str(conn))

    @mock_kinesis
    def test_can_get_partition_key(self):
        c = self.create_context()
        partition_key = self.handler.get_partition_key()
        self.assertIn("shardId", partition_key)

    @mock_kinesis
    def test_can_log_and_retrieve_log(self):
        c = self.create_context()
        self.logger.error(hello='world')
        conn = boto.connect_kinesis()
        shard_iterator = conn.get_shard_iterator(
                            self.stream['StreamDescription']['StreamName'],
                            shard_id=self.handler.partition_key,
                            shard_iterator_type="TRIM_HORIZON").get('ShardIterator')
        records = conn.get_records(shard_iterator).get('Records')
        self.assertEqual(1, len(records))
        self.assertIn('ERROR', records[0].get('Data'))
        self.assertIn('{"hello": "world"}', records[0].get('Data'))
