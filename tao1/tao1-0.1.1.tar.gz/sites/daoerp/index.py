#!/usr/bin/env python
# coding: utf-8


import sys, os
assert sys.version >= '3.3', 'Please use Python 3.4 or higher.'

import asyncio
from aiohttp import web


import settings
sys.path.append(settings.root)
os.environ['TAO_PATH_ROOT'] = settings.root
path = os.path.dirname( __file__ )
sys.path.append( path )
# os.chdir(path)


# print( sys.path )
# os.environ['TAO_PATH_ROOT'] = settings.root
# print( os.environ )

from core.union import init

# app = web.Application()

# app = web.Application(middlewares=[toolbar_middleware_factory])
# aiohttp_debugtoolbar.setup(app)

loop = asyncio.get_event_loop()
loop.run_until_complete( init( loop ) )
try: loop.run_forever()
except KeyboardInterrupt:  loop.run_until_complete( handler.finish_connections() )




