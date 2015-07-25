#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from easy_logger.config import DEFAULT_LEVEL, DEFAULT_FORMAT


class Logger(object):

    def __init__(self, level=DEFAULT_LEVEL, format=DEFAULT_FORMAT):
        self._level = level
        self._format = format
        self._formatter = logging.Formatter(self._format)

    def get_logger(self, name):
        return self.get_stream_logger(name)

    def get_stream_logger(self, name):
        """Get logger which has add streamHandler. Output log message to stream.

        :param str name: logger name
        """
        logger = logging.getLogger(name)
        logger.setLevel(self._level)

        if not self._has_stream_handler(logger):
            sh = logging.StreamHandler()
            sh.setFormatter(self._formatter)
            logger.addHandler(sh)

        return logger

    def get_file_logger(self, name, filepath):
        """Get logger which has add fileHandler. Output log message to specify file.

        :param str name: logger name
        :param str name: the log file path
        """
        logger = logging.getLogger(name)
        logger.setLevel(self._level)

        if not self._has_file_handler(logger):
            fh = logging.FileHandler(filepath)
            fh.setFormatter(self._formatter)
            logger.addHandler(fh)

        return logger

    def get_both_logger(self, name, filepath):
        """Get logger which has both add streamHandler and fileHandler.
        Output log message to stream and specify file.

        :param str name: logger name
        :param str name: the log file path
        """
        logger = logging.getLogger(name)
        logger.setLevel(self._level)

        if not self._has_stream_handler(logger):
            sh = logging.StreamHandler()
            sh.setFormatter(self._formatter)
            logger.addHandler(sh)

        if not self._has_file_handler(logger):
            fh = logging.FileHandler(filepath)
            fh.setFormatter(self._formatter)
            logger.addHandler(fh)

        return logger

    # Private functions

    def _has_stream_handler(self, logger):
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                return True
        return False

    def _has_file_handler(self, logger):
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                return True
        return False
