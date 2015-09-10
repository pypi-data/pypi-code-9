# -*- coding: utf-8 -*-
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
