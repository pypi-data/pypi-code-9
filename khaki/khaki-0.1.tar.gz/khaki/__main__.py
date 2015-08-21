from signal import ITIMER_REAL, setitimer, signal, SIGALRM


class Event:
    def __init__(self):
        self.handlers = []

    def attach(self, handler):
        self.handlers.append(handler)

    def notify(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)


def events(*args):
    def add_methods(cls):
        def add_method(event):
            name = 'on_{}'.format(event)

            def on_event(obj, handler):
                attr = '_{}'.format(event)
                getattr(obj, attr).attach(handler)

            on_event.__name__ = name
            setattr(cls, name, on_event)

        for event in args:
            add_method(event)

    def add_members(cls):
        def add(obj):
            for event in args:
                setattr(obj, '_{}'.format(event), Event())

        old_init = cls.__init__

        def new_init(self, *args, **kwargs):
            add(self)
            old_init(self, *args, **kwargs)

        cls.__init__ = new_init

    def decorate(cls):
        add_members(cls)
        add_methods(cls)
        cls.decorated = True
        return cls

    return decorate


@events('tick', 'done')
class Timer:
    def __init__(self, inverted=False, top=9999):
        self._step = -1 if inverted else 1
        self._inverted = inverted
        self._set_top(top)
        self._paused = True
        self.clear()

    @property
    def top(self):
        return self._start if self._inverted else self._limit

    @top.setter
    def top(self, value):
        self._set_top(value)

    def read(self):
        return self._time

    def clear(self):
        self._set_time(self._start)

    def toggle(self):
        if self._paused:
            self.start()
        else:
            self.stop()

    def start(self):
        signal(SIGALRM, self._increment)
        setitimer(ITIMER_REAL, .1, .1)
        self._paused = False

    def stop(self):
        setitimer(ITIMER_REAL, 0)
        self._paused = True

    def _set_top(self, value):
        if value < 0:
            value = 0
        self.stop()
        self._limit = 0 if self._inverted else value
        self._start = value if self._inverted else 0
        self.clear()

    def _set_time(self, value):
        self._time = value
        self._tick.notify(self._time)

    def _increment(self, _, _2):
        self._set_time(self._time + self._step)
        if self._time == self._limit:
            self.stop()
            self._done.notify()


class Pomodoro(Timer):
    def __init__(self, time_work=15000, time_pause=3000):
        super().__init__(inverted=True, top=time_work)
        self._current = 0
        self.times = [time_work, time_pause]
        self.on_done(self.advance_timer)

    def advance_timer(self):
        self._current = (self._current + 1) % len(self.times)
        self.top = self.times[self._current]

    @property
    def top(self):
        return super().top

    @top.setter
    def top(self, value):
        self.times[self._current] = value
        self._set_top(value)


import curses
import pyglet


pyglet.options['audio'] = ('pulse', 'silent')
pyglet.resource.path=['@khaki', '.']
pyglet.resource.reindex()


class CursesScreen:
    def __init__(self, curses_window, timer):
        self._screen = curses_window
        self._timer = timer
        self.redraw_all()

    def redraw_all(self):
        self._screen.clear()
        height, width = self._screen.getmaxyx()
        self._timer_win = self._screen.derwin(1, 10, height//2, width//2-5)
        self._timer.on_tick(self.update)
        self.update(self._timer.read())

    def update(self, time):
        seconds, tenths = divmod(time, 10)
        minutes, seconds = divmod(seconds, 60)
        self._timer_win.addstr(0, 0, "{:4}:{:02}:{}".format(minutes,
                                                            seconds,
                                                            tenths))
        self._timer_win.refresh()


def main(stdscr):
    curses.use_default_colors()
    curses.curs_set(0)

    player = pyglet.media.Player()
    alarm = pyglet.resource.media('alarm.wav', streaming=False)

    def done():
        player.queue(alarm)
        player.play()

    def resize():
        screen.redraw_all()

    pomodoro = Pomodoro()

    screen = CursesScreen(stdscr, pomodoro)

    pomodoro.on_done(done)

    def up_top():
        pomodoro.top += 10

    def down_top():
        pomodoro.top -= 10

    key_handlers = {ord('p'): pomodoro.toggle,
                    ord('c'): pomodoro.clear,
                    ord('q'): lambda: exit(0),
                    ord('+'): up_top,
                    ord('-'): down_top,
                    curses.KEY_RESIZE: resize}

    while True:
        c = stdscr.getch()
        if c in key_handlers:
            key_handlers[c]()


def run():
    curses.wrapper(main)

if __name__ == '__main__':
    run()
