# -*- coding: utf-8 -*-
import sys


if sys.argv and sys.argv[0] == '-c':
    # python -m vebootstrap hogehoge.py
    pass
else:
    # vebootstrap imported from [pyfile]
    from . import context
    c = context.Context(sys.executable, sys.argv[0])
    c.bootstrap(sys.argv[1:])

