#!/usr/bin/env python
''' abyss.server
Abyss HTTP API server
'''

class Route(object):
    BASE = '/'
    USER = '/user/<username>'

def route(attr):
    val = getattr(Route, attr.upper())
    return val.replace('<', '{').replace('>', '}')

def main():
    from abyss.server.app import main
    main()
