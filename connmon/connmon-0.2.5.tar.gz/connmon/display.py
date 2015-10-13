import curses
import functools
import operator
import re
import time
import sys

from zkcluster import util


COLOR_MAP = {
    "K": curses.COLOR_BLACK,
    "R": curses.COLOR_RED,
    "B": curses.COLOR_BLUE,
    "C": curses.COLOR_CYAN,
    "G": curses.COLOR_GREEN,
    "M": curses.COLOR_MAGENTA,
    "R": curses.COLOR_RED,
    "W": curses.COLOR_WHITE,
    "Y": curses.COLOR_YELLOW,
    "D": -1
}

_TEXT_RE = re.compile(r'(#.+?)&', re.M)


class Display(object):
    def __init__(self, stat, client):
        self.columns = [
            ('hostname (#R&[dis]#G&connected#d&)', "%s", .20, "L"),
            ('progname', "%s", .20, "L"),
            ('nproc', "%d", .08, "R"),
            ('conn', "%d", .08, "R"),
            ('ckout', "%d", .08, "R"),
            ('maxnproc', "%d", .12, "R"),
            ('maxconn', "%d", .12, "R"),
            ('maxckout', "%d", .12, "R"),
        ]
        self.stat = stat
        self.client = client  # zkconfig.client.LocalClient

        self._winsize = None
        self._x_positions = None

    def _calc_x_positions(self):
        x = 0
        widths = []
        midline = False
        for idx, col in enumerate(self.columns):
            cname = col[0]
            width = col[2]
            just = col[3]
            charwidth = max(len(cname), int(self._winsize[1] * width))
            if just == "L":
                widths.append((x, charwidth))
                x += charwidth
            else:
                width = sum(
                    max(len(col[0]), int(self._winsize[1] * col[2]))
                    for col in self.columns[idx:]
                )
                x = self._winsize[1] - width
                if not midline:
                    midline = True
                    midline_at = widths[-1][0] + widths[-1][1]
                    midline_over = midline_at - x
                    if midline_over > 0:
                        widths[-1] = \
                            widths[-1][0], widths[-1][1] - midline_over
                widths.append((x, charwidth))

        self._x_positions = widths

    def _refresh_winsize(self):
        old_winsize = self._winsize

        self._winsize = self.window.getmaxyx()
        if old_winsize != self._winsize or \
                curses.is_term_resized(*old_winsize):
            curses.resize_term(*self._winsize)
            self._calc_x_positions()

    def start(self):
        self.enabled = True
        window = curses.initscr()

        curses.noecho()
        window.erase()
        window.nodelay(1)
        curses.start_color()
        curses.use_default_colors()
        self._color_pairs = {}
        for i, (k, v) in enumerate(COLOR_MAP.items(), 1):
            curses.init_pair(i, v, -1)
            self._color_pairs[k] = curses.color_pair(i)
        self._color_pairs['b'] = curses.A_BOLD
        self._color_pairs['n'] = curses.A_NORMAL
        window.refresh()
        self.window = window
        self._refresh_winsize()

        try:
            with util.stop_on_keyinterrupt():
                self._redraw()
        finally:
            self.stop()

    def _redraw(self):
        render_timer = util.periodic_timer(.5)
        while self.enabled:
            time.sleep(.1)
            if render_timer(time.time()):
                self._render()
            self._handle_cmds()

    def _handle_cmds(self):
        char = self.window.getch()
        if char in (ord('Q'), ord('q')):
            self.stop()
        elif char == curses.KEY_RESIZE:
            # NOTE: this char breaks if you import readline, which
            # is implicit if you use Python cmd.Cmd() in its default
            # mode
            self._refresh_winsize()

    def stop(self):
        self.enabled = False
        curses.endwin()

    def _get_color(self, color):
        try:
            return self._color_pairs[color]
        except KeyError:
            assert len(color) > 1
            mapped = functools.reduce(
                operator.or_,
                [self._color_pairs[char] for char in color]
            )
            self._color_pairs[color] = mapped
            return mapped

    def _render_str(self, y, x, text, default_color="D", max_=None):
        if x < 0:
            x = self._winsize[1] - len(_TEXT_RE.sub('', text))

        current_color = dflt = self._get_color(default_color)
        if max_:
            max_x = x + max_
        else:
            max_x = self._winsize[1]
        for token in _TEXT_RE.split(text):
            if token.startswith("#"):
                ccode = token[1:]
                if ccode == "d":
                    current_color = dflt
                else:
                    current_color = self._get_color(ccode)
            else:
                self.window.addstr(y, x, token[:max_x - x], current_color)
                x += len(token)
                if x > max_x:
                    break

    def _render_row(self, row, y):
        x_positions = iter(self._x_positions)
        for elem, col in zip(row, self.columns):
            cname, fmt, width, justify = col
            elem = fmt % (elem, )
            x, charwidth = next(x_positions)
            self._render_str(y, x, elem, max_=charwidth - 1)

    def _render(self):
        self.window.erase()

        self._render_str(
            0, 0,
            "#Bb&[Connmon]#Dn& [%s:%s | %s:%s]" % (
                self.client.servicename,
                self.client.nodename, self.client.host, self.client.port
            )
        )
        self._render_str(
            0, -1,
            "#D&Commands: #Y&(Q)#D&uit"
        )

        self._render_str(
            2, 0,
            "#Mb&Hosts: #Dn&[%d / %d max]  #Mb&Processes: #Dn&[%d / %d max]  "
            "#Mb&Connections: #Dn&[%d / %d max]  "
            "#Mb&Checkouts: #Dn&[%d / %d max]" % (
                self.stat.host_count,
                self.stat.max_host_count,
                self.stat.process_count,
                self.stat.max_process_count,
                self.stat.connection_count,
                self.stat.max_connection_count,
                self.stat.checkout_count,
                self.stat.max_checkout_count
            ),
            "Wb"
        )

        top = 5

        x_positions = iter(self._x_positions)
        for col in self.columns:
            cname, fmt, width, justify = col
            x, charwidth = next(x_positions)
            self._render_str(top, x, cname, "Cb")

        rows = []
        hostprogs = list(self.stat.hostprogs.values())
        hostprogs.sort(
            key=lambda hostprog: (hostprog.hostname, hostprog.progname)
        )
        for hostprog in hostprogs:
            is_connected = bool(hostprog.process_count)
            rows.append((
                "#%s&%s" % (
                    "G" if is_connected else "R",
                    hostprog.hostname,
                ),
                "#%s&%s" % (
                    "G" if is_connected else "R",
                    hostprog.short_progname,
                ),
                hostprog.process_count,
                hostprog.connection_count,
                hostprog.checkout_count,
                hostprog.max_process_count,
                hostprog.max_connections, hostprog.max_checkedout
            ))

        for y, row in enumerate(rows, top + 1):
            self._render_row(row, y)
        self.window.refresh()

