#!/usr/bin/env python
# encoding: utf-8

import sys
ver = sys.version_info.major
if ver == 3:
    from .api import md, td, StrategyBase, get_strerror, get_version
    from .enums import *
    from . import util
    from .gm import Cash, Position, Order, ExecRpt, Tick, Bar, DailyBar, Indicator
else:
    from api import md, td, StrategyBase, get_strerror, get_version
    from enums import *
    import util
    from gm import Cash, Position, Order, ExecRpt, Tick, Bar, DailyBar, Indicator
