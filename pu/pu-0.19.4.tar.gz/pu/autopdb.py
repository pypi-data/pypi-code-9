# -*- coding: utf-8 -*-
"""产生异常时自动进入调试状态

参考:

- https://docs.python.org/3.4/library/sys.html#sys.ps1
- http://code.activestate.com/recipes/65287-automatically-start-the-debugger-on-an-exception/
"""
import sys


def info(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        # we are in interactive mode or we don't have a tty-like
        # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback, pdb
        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        pdb.pm()


sys.excepthook = info
