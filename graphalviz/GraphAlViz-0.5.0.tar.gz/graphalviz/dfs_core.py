# -*- coding: utf-8 -*-
from time import sleep


def dfs(G, s, delay=1):
    """
    DFS algorithm implementation

    Parameters:
    -----------
    G : GraphAlViz type object
    s : starting vertex

    """
    G.set_v_color(s, 'w')
    sleep(delay)
    for vertex in G.neighbors_iter(s):
        if G.get_v_color(vertex) != 'w':
            dfs(G, vertex)
