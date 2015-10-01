# encoding: utf8

import math
import sys

from SundaysIron import colors


class ProgressBar(object):
    STATUS_OK = 0
    STATUS_ERROR = 1

    def __init__(self, name="Progress", max_value=40):
        self.name = name
        self.max_value = max_value
        self.__end = True

    def update(self, progress, status=STATUS_OK):
        sys.stdout.write('\r{color}{name} [{body}] {progress} %'.format(
            color=colors['fg']['green'] if status == self.STATUS_OK else colors['fg']['red'],
            name=self.name,
            body=('{}' * self.max_value).format(
                *['#' if i < math.ceil(progress * self.max_value / 100.0) else '.' for i in xrange(0, self.max_value)]),
            progress=progress))
        sys.stdout.flush()

    def end(self):
        if self.__end:
            print ''
        self.__end = False
