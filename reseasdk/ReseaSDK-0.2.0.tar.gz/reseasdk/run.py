import os
import sys
import atexit
import datetime
import subprocess
from termcolor import cprint, colored
from reseasdk.helpers import info, error

def lprint(s):
    try:
        if not s.startswith("["):
            raise ValueError
        app, rest = s.split(' ', 1)
        app = app.lstrip('[').rstrip(']')
        type_, rest = rest.split(':', 1)
        type_ = type_.rstrip(':')
        body = rest.strip()
    except ValueError:
        print(s)
    else:
        if type_ == 'TEST':
            if body in ['start', 'end']:
                return
            elif body.startswith("<pass>"):
                type_ = 'PASS'
            else:
                type_ = 'FAIL'
        t = {
            'INFO':  (' I ', 'white', 'on_blue'),
            'BUG':   (' B ', 'white', 'on_red'),
            'PANIC': (' P ', 'white', 'on_red'),
            'WARN':  (' W ', 'white', 'on_yellow'),
            'DEBUG': (' D ', 'grey',  'on_white'),
            'PASS':  (' T ', 'white', 'on_green'),
            'FAIL':  (' T ', 'white', 'on_red'),
        }.get(type_, (' ',))
        pad = ' ' * (12 - len(app))
        print('{} {} {}'.format(
            colored(pad + app, attrs=['bold']),
            colored(*t),
            body))

        if type_ == "PANIC":
            raise SystemExit


def try_parse(l):
    try:
        test = l.split("TEST: ")[1]
        result = test.split(" ", 2)[0].lstrip("<").rstrip(">")
    except IndexError:
        result = ""
    return result


def atexit_handler(p):
    info('ReseaSDK: terminating the executable...')
    try:
        if p.poll() is not None:
            p.kill()
    except ProcessLookupError:
        pass


def run_emulator(cmd, test=False, env=None, save_log=None):
    if save_log is None:
        save_log = "/dev/null"

    # prepend a header to the log file
    f = open(save_log, 'a')
    f.write('================ {} ================\n'.format(
            str(datetime.datetime.now())))

    # run test program speicified in HAL_RUN config
    envs = os.environ.copy()
    envs.update(env)
    p = subprocess.Popen(cmd, env=envs,
                         stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)

    atexit.register(atexit_handler, p)

    # parse log messages
    passed = 0
    failed = 0
    while True:
        l = p.stdout.readline().decode("utf-8").strip()

        if l == "":
            p.terminate()
            p.kill()
            if test:
                error("the test program finished without 'TEST: end'")
            sys.exit(0)

        result = try_parse(l)
        if result == "end":
            f.write(l + "\n")
            lprint(l)
            if test:
                if failed == 0:
                    cprint("ReseaSDK: All {} tests passed".format(passed), "green")
                else:
                    cprint("ReseaSDK: {} tests failed".format(failed), "red")
            p.terminate()
            p.kill()
            sys.exit(0)
        elif result == "pass":
            passed += 1
            f.write(l + "\n")
            lprint(l)
        elif result == "fail":
            failed += 1
            f.write(l + "\n")
            lprint(l)
        else:
            f.write(l + "\n")
            try:
                lprint(l)
            except SystemExit:
                # kernel panic
                p.terminate()
                p.kill()
                sys.exit(0)
