#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-07-06 00:38:55
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-07-06 21:55:09

import sys

from PySide import QtGui
from digs.logger import Logger
from window import Window


log = Logger.log
__all__ = ['run']


def run():
    app = QtGui.QApplication(sys.argv)
    wds = Window()
    wds.show()
    sys.exit(app.exec_())
    del wds


if __name__ == '__main__':
    run()
