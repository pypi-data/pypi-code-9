#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PySide import QtCore
from digs.logger import Logger
from digs.worker import scraper


log = Logger.log


class Start(QtCore.QThread):
    FLAG = True

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        log.debug('created QThread for Start')
        opts = self.window.options()

        url = opts.get('<url>', None)
        if not url or not url.startswith('http'):
            self.window.on_show_info("URL must contain http:// or https://")
            log.error("URL must contain http:// or https://")
            self.exit()
            return

        to = opts.get('--to', None)
        if not to or not os.path.exists(to):
            self.window.on_show_info(
                "The directory to save results does not exist.")
            log.error("The directory to save results does not exist.")
            self.exit()
            return

        try:
            scraper(opts['<url>'], opts['--depth'],
                    opts['--to'], opts['--sameroot'], opts['-o'])
        except Exception, e:
            log.error(e)
        self.exit()
        return
