# -*- coding: utf-8 -*-
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def nonblank_lines(f):
    for l in f:
        line = l.strip()
        if line:
            yield line
