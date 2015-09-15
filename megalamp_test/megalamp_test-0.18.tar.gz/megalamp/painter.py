# encoding=utf-8

import curses
import sys
from loggers import logger


class Painter(object):

    LIGHT_COLOR_NUM = 10
    OFF_COLOR = (100, 100, 100)
    ON_COLOR = (255, 255, 255)

    def __init__(self):
        self.init_curses()
        self.draw_lamp(self.OFF_COLOR)

    def on(self):
        self.color(self.ON_COLOR)

    def off(self):
        self.color(self.OFF_COLOR)

    def color(self, rgb):
        self.draw_lamp(rgb)
        logger.info('Change color to {}'.format(rgb))

    def init_curses(self):
        self.win = curses.initscr()
        curses.noecho()
        self.win.nodelay(1)
        curses.start_color()
        sys.stdout = NullDevice()
        sys.stderr = NullDevice()
        self.crash_if_colors_not_supported()

    def crash_if_colors_not_supported(self):
        if not curses.has_colors():
            self.destroy()
            error = (
                "It seems your terminal does not support colors.\n"
                "Change terminal's settings and try again.\n"
                "For example, you can do it with 'export TERM=xterm-256color'\n"
            )
            raise RuntimeError(error)

    def destroy(self):
        curses.endwin()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stdout__

    def draw_lamp(self, light_rgb):
        try:
            self.do_draw_lamp(light_rgb)
        except Exception as e:
            logger.exception(e.message)
            self.destroy()
            raise

    def do_draw_lamp(self, light_rgb):

        self.win.clear()
        curses.init_color(self.LIGHT_COLOR_NUM, *light_rgb)

        curses.init_pair(
            self.LIGHT_COLOR_NUM,
            self.LIGHT_COLOR_NUM,
            self.LIGHT_COLOR_NUM,
        )

        self.win.addstr(1, 6, "This quare is a Lamp")
        lamp_points = [
            (1, 1),
            (2, 1),
        ]
        for x, y in lamp_points:
            self.win.addstr(
                x, y, "****",
                curses.color_pair(self.LIGHT_COLOR_NUM)
            )
        self.win.refresh()


class NullDevice():
    def write(self, s):
        pass
