from __future__ import print_function
import functools
import signal
import sys
import traceback
import threading


lock = threading.Lock()

def _call_once(function):
    @functools.wraps(function)
    def call_function(*args, **kwargs):
        if hasattr(function, 'called'):
            return
        try:
            return function(*args, **kwargs)
        finally:
            setattr(function, 'called', True)
    return call_function


def _dump_data():
    with lock:
        sys_err = open('/dev/stderr', 'w')
        if sys.version_info.major > 2:
            log = functools.partial(print, file=sys_err, flush=True)
        else:
            log = functools.partial(print, file=sys_err)
        threads = {thread.ident: thread for thread in threading.enumerate()}
        for ident, frame in sys._current_frames().items():
            log('=' * 80)
            log('Thead', threads[ident].name, ident)
            log(''.join(traceback.format_stack(frame)))
            log('=' * 80, '\n\n\n')


@_call_once
def setup_dumpper():
    def dump_data(*args, **kwargs):
        threading.Thread(target=_dump_data).start()

    signal.signal(signal.SIGQUIT, dump_data)
