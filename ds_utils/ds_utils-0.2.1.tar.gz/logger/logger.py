import json
import logging
import sys
import boto
import random
import warnings
import socket


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def silence(name):
    logging.getLogger(name).handlers = []
    logging.getLogger(name).addHandler(logging.NullHandler())


class KinesisHandler(logging.Handler):
    """
    Handler class for sending events to Kinesis
    """
    def __init__(self, stream):
        logging.Handler.__init__(self)

        self.conn = self.get_connection()
        self.stream = stream
        self.partition_key = self.get_partition_key()

        ip = socket.gethostbyname(socket.gethostname())
        log_format = "%(asctime)s [%(levelname)s] [%(name)s] [{0}] [%(process)d] %(message)s".format(ip)
        formatter = logging.Formatter(log_format)
        self.setFormatter(formatter)

    def get_connection(self):
        try:
            conn = boto.connect_kinesis()
        except boto.exception.NoAuthHandlerFound as err:
            warnings.warn("No IAM role or AWS credential environment variables found. Check your environment variables.")
            raise err
        return conn

    def get_partition_key(self):
        s = self.conn.describe_stream(self.stream)
        shard = random.choice(s.get('StreamDescription').get('Shards'))
        return shard.get('ShardId')

    def emit(self, record):
        try:
            data = self.format(record)
            self.conn.put_record(self.stream,
                                 data,
                                 self.partition_key)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class Logger(object):
    def __init__(self, name, kinesis=None):
        """
        Constructor for a Logger
        Sets up format and streams
        :param name: basic logger name
        :param kinesis: Kinesis logger name, or None if not using Kinesis
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.log_format = "%(asctime)s [%(levelname)s] [%(name)s] [%(process)d] %(message)s"

        self.formatter = logging.Formatter(self.log_format)
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(self.formatter)

        self.setLevel(logging.INFO)
        self.addHandler(self.stream_handler)

        if kinesis:
            self.addHandler(KinesisHandler(kinesis), empty_first=False)

        self.default_message = {}

    def setup(self, **kwargs):
        self.default_message = kwargs

    def _prepare_message(self, message_dict):
        for key, value in self.default_message.iteritems():
            if key not in message_dict:
                message_dict[key] = value
        return json.dumps(message_dict)

    def setLevel(self, level):
        self.logger.setLevel(level)

    def addHandler(self, handler, empty_first=True):
        if empty_first:
            self.logger.handlers = []
        self.logger.addHandler(handler)

    def debug(self, **kwargs):
        msg = self._prepare_message(kwargs)
        self.logger.debug(msg)

    def info(self, **kwargs):
        msg = self._prepare_message(kwargs)
        self.logger.info(msg)

    def warning(self, **kwargs):
        msg = self._prepare_message(kwargs)
        self.logger.warning(msg)

    def error(self, **kwargs):
        msg = self._prepare_message(kwargs)
        self.logger.error(msg)

    def critical(self, **kwargs):
        msg = self._prepare_message(kwargs)
        self.logger.critical(msg)
