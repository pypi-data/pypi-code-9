# -*- coding: utf-8 -*-
from time import sleep


def dfs(C, s, delay=1):
    """
    DFS algorithm implementation (client/server)

    Parameters:
    -----------
    C : GraphAlVizSimpleClient object with loaded graph
    s : starting vertex

    """
    C.set_v_color(s, 'w')
    sleep(delay)
    for vertex in C.neighbors(s):
        if C.get_v_color(vertex) != 'w':
            dfs(C, vertex)
