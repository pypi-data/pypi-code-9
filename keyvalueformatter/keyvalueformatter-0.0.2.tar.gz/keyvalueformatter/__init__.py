'''
This library is provided to allow standard python logging
to output log data as key/value formatted strings.

Based on: https://github.com/madzak/python-json-logger
'''
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import logging
import re
import traceback

from six import iteritems

# Support order in python 2.7 and 3
try:
    from collections import OrderedDict
except ImportError:
    pass

# skip natural LogRecord attributes
# http://docs.python.org/library/logging.html#logrecord-attributes
RESERVED_ATTRS = (
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'module',
    'msecs', 'message', 'msg', 'name', 'pathname', 'process',
    'processName', 'relativeCreated', 'thread', 'threadName',
    'stack_info', 'extra')

RESERVED_ATTR_HASH = dict(zip(RESERVED_ATTRS, RESERVED_ATTRS))


def merge_record_extra(record, target, reserved=RESERVED_ATTR_HASH):
    """
    Merges extra attributes from LogRecord object into target dictionary

    :param record: logging.LogRecord
    :param target: dict to update
    :param reserved: dict or list with reserved keys to skip
    """
    for key, value in record.__dict__.items():
        # This allows to have numeric keys
        if (key not in reserved
            and not (hasattr(key, "startswith")
                     and key.startswith('_'))):
            target[key] = value
    return target


class KeyValueFormatter(logging.Formatter):
    """
    A custom formatter to format logging records as key value pair strings.
    """

    def __init__(self, *args, **kwargs):
        """
        :param prefix: an optional string prefix added at the beginning of
            the formatted string
        """
        self.prefix = kwargs.pop("prefix", "")
        # super(KeyValueFormatter, self).__init__(*args, **kwargs)
        logging.Formatter.__init__(self, *args, **kwargs)
        self._required_fields = self.parse()
        self._skip_fields = dict(zip(self._required_fields,
                                     self._required_fields))
        self._skip_fields.update(RESERVED_ATTR_HASH)

    def parse(self):
        """Parses format string looking for substitutions"""
        standard_formatters = re.compile(r'\((.+?)\)', re.IGNORECASE)
        return standard_formatters.findall(self._fmt)

    def add_fields(self, log_record, record, message_dict):
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)
        log_record.update(message_dict)
        merge_record_extra(record, log_record, reserved=self._skip_fields)

    def process_log_record(self, log_record):
        """
        Override this method to implement custom logic
        on the possibly ordered dictionary.
        """
        return log_record

    def kv_repr(self, val, response):
        ''' Slunk plays nicer with double quotes around values, and repr uses
            single quotes without a clean way to change this.
        '''
        try:
            return "{0}{1}{0}".format('"', str(val).replace('"', r'\"').
                                      replace('\n', r'\n'))
        except:
            # Surface the fact custom formatting failed
            response.append('kv_repr_error="True"')
            return repr(val)

    def format(self, record):
        """Formats a log record and serializes to key pairs"""
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = None
        else:
            record.message = record.getMessage()
        # only format time if needed
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        self.add_fields(log_record, record, message_dict)
        log_record = self.process_log_record(log_record)

        response = [self.prefix]

        sorted_entries = sorted([(k, v) for k, v in iteritems(log_record)])
        for key, value in sorted_entries:
            if key == 'exc_info' and value and len(value) is 3:
                exc_type = self.kv_repr(value[0], response)
                exc_line = self.kv_repr(value[1], response)
                exc_tb = traceback.extract_tb(value[2])
                response.append('{}={}'.format('exc_info', exc_type))
                response.append('{}={}'.format('exc_info_1', exc_line))
                for i, v in enumerate(exc_tb):
                    response.append('{}={}'.format("exc_tb_{}".format(i),
                                                   self.kv_repr(v, response)))
            elif key == 'exc_text' and value is not None:
                response.append('{}={};'.format('exc_text', "True"))
                for i, v in enumerate(value.split('\n')):
                    response.append('{}={}'.format("exc_text_{}".format(i),
                                                   self.kv_repr(v, response)))
            else:
                response.append('{}={}'.format(key, self.kv_repr(value,
                                                                 response)))
        return ";".join(response)
