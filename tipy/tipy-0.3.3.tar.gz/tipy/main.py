#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The main file parse the command line and run the program in the desired way.

There's three possible runing options:
    - -c or --cmdl: Run the program using the command line interface (not
        really suitable)
    - -g or --gui: Run the program using the graphic user interface.
    - -p or --profile: Simulate the predictions computation for a sample
        string and print the profiling statistics for the session. This is
        useful to see what part of the program took the largest part of the
        program's execution time.

Examples of profiling use::
    tipy -p '' -l 10
        -> Simulate the input and predction of ten consecutive inputs of the
           'hello world' string (default string).

    tipy -p 'the seasons wither'
        -> Simulate the input and predction of the 'the seasons wither'
           string.

@note: You must specify your own test string after -p or --profile, if
    none are specified a default one will be used.
@note: The option -l or -loop indicate how many times the profiling
    operation have to be carried out.

@todo 0.1.0:
    Add memoize classes and decorators to improve performance.
"""

from PyQt5 import QtWidgets
from tipy.clbk import Callback
from tipy.drvr import Driver
from tipy.gui import MainWindow
from tipy.lg import lg
from sys import argv, exit
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from getopt import getopt, GetoptError
from cProfile import Profile, runctx
from pstats import Stats
from os import path, environ


CONFIG_FILE = ''


def set_config_file():
    """Look for the best directory where a config file can be."""
    global CONFIG_FILE
    locations = [
        path.join(path.expanduser("~"), '.config/tipy'),
        path.join(path.dirname(path.realpath(__file__)), 'cfg'),
        "/usr/share/tipy",
        environ.get("TIPY_CONFIG_PATH"),
    ]
    for loc in locations:
        try:
            if path.isfile(path.join(loc, "tipy.ini")):
                CONFIG_FILE = path.join(loc, "tipy.ini")
                lg.info('Using config file "%s/tipy.ini"' % loc)
                break
        except IOError:
            pass
        except TypeError:
            pass


def run_profile(string='hello world', profileLoops=1):
    """Initialize the Driver instance and start a cmdl REP loop."""
    for i in range(profileLoops):
        callback = Callback()
        driver = Driver(callback, CONFIG_FILE)
        for c in string:
            callback.update(c)
            suggestions = driver.predict()
            for p in suggestions:
                print(p)
            print('-- Context: %s<|>' % (driver.callback.left))


def run_cmdl():
    """Initialize the Driver instance and start a cmdl REP loop."""
    callback = Callback()
    driver = Driver(callback, CONFIG_FILE)
    while True:
        buffer = input('> ')
        callback.update(buffer)
        suggestions = driver.predict()
        for p in suggestions:
            print(p)
        print('-- Context: %s<|>' % (driver.callback.left))


def run_gui():
    """Initialize the Driver instance and run the """
    callback = Callback()
    driver = Driver(callback, CONFIG_FILE)
    app = QtWidgets.QApplication(argv)
    mySW = MainWindow(driver)
    mySW.show()
    exit(app.exec_())


def usage():
    """Print the usage message."""
    print('USAGE:   python3 main.py [-h -c -g -p <string> -l <loops>]\n')
    print('OPTIONS:')
    print('\t-h or --help: print the help')
    print('\t-c or --cmdl: use the command line version')
    print('\t-g or --gui: use the graphic user interface version')
    print('\t-p or --profile: use the profile module to evaluate program '
          'performance.')
    print('\t\t<string> is the string to use for prediction computation.')
    print('\t-l or --loops: run the profiling operation multiple times.')
    print('\t\t<loops> is the number of loops.')


def main():
    """The main function of the program.

    Take care of the command line options and run the program (gui or command
    line) or print the help.
    """
    try:
        opts, args = getopt(
            argv[1:], "hcgp:l:",
            ['help', 'cmdl', 'gui', 'profile=', 'loop='])
    except GetoptError as err:
        print(str(err))
        usage()
        exit(2)
    mode = 'gui'
    profileString = 'hello world'
    profileLoops = 1
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            exit()
        elif o in ("-c", "--cmdl"):
            mode = 'cmdl'
        elif o in ("-g", "--gui"):
            mode = 'gui'
        elif o in ("-p", "--profile"):
            mode = 'profile'
            if a:
                profileString = a
        elif o in ("-l", "--loop"):
            if a:
                profileLoops = int(a)
        else:
            assert False, "ERROR: Unrecognized option"
    set_config_file()
    if mode == 'cmdl':
        run_cmdl()
    elif mode == 'profile':
        pr = Profile()
        pr.enable()
        runctx(
            'run_profile(profileString, profileLoops)',
            {'profileString': profileString, 'run_profile': run_profile,
             'profileLoops': profileLoops}, locals())
        pr.disable()
        s = StringIO()
        ps = Stats(pr, stream=s).sort_stats('time')
        ps.print_stats()
        print(s.getvalue())
    else:
        run_gui()


if __name__ == "__main__":
    main()
