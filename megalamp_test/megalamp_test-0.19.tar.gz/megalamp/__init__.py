# encoding=utf-8

import functools
import signal
import tornado.ioloop

from configs import config
from lamp import Lamp


def main():

    lamp = Lamp(config.host, config.port)

    on_exit = functools.partial(_on_exit, lamp)
    signal.signal(signal.SIGTERM, on_exit)
    signal.signal(signal.SIGINT, on_exit)

    lamp.start()
    tornado.ioloop.IOLoop.current().start()


def _on_exit(lamp, signum, stack):
    lamp.finish()
    tornado.ioloop.IOLoop.current().stop()
