#!/usr/bin/env python
# coding: utf-8

# from app.user_site import *
# from app.perm.perm import *
# from app.tree.tree import *

import sys, os
import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web import Application, Response, MsgType, WebSocketResponse

# from core.utils import connect
from pymongo import *
from gridfs import GridFS
from aiohttp_session import get_session
import time
# print (sys.path) 

# from core.utils import *


@asyncio.coroutine
def test_db(request):
    print( 'bbbbbbbbbbbbbb' )

    session = yield from get_session(request)
    session['last_visit'] = time.time()
    request.db.doc.save({"_id":"test", "val":"test_db", "status":"success"})
    val = request.db.doc.find_one({"_id":"test"})
    return templ('apps.app:db_test', request, {'key':val})


# @asyncio.coroutine
def page(request):
	return templ('apps.app:index', request, {'key':'val'})

@asyncio.coroutine
def ws(request):
	return templ('apps.app:chat', request, {} )

@asyncio.coroutine
def ws_handler(request):
    print ('111111', request.scheme )
    ws = web.WebSocketResponse()
    ws.start(request)
    while True:
        print ('while' )
        msg = yield from ws.receive()
        print ('post while', msg )
        print('text')
        # print('text', aiohttp.MsgType.text)
        if msg.tp == MsgType.text:
            print ('1if', msg )
            if msg.data == 'close':
                print ('if', msg )
                yield from ws.close()
            else:
                print ('else', msg )
                ws.send_str(msg.data + '/answer')
        elif msg.tp == aiohttp.MsgType.close: print('websocket connection closed')
        elif msg.tp == aiohttp.MsgType.error: print('ws connection closed with exception %s', ws.exception())
    return ws	


# @asyncio.coroutine
# def page2(request):
	# return templ('./user_app/users_app/index.tpl', request, {'key':'val'})
	# return templ('index', request, {'key':'val'})

	

@asyncio.coroutine
def test_db1(request):
    # db = connect()
    # print( 'db' )

    # mongo = MongoClient('localhost', 27017)
    # print( mongo)
    # db = mongo['tok']
    # db.authenticate('admin', 'Gthcgtrnbdf')

    # print( db )
    # val = db['doc'].find_one({})

    # val = yield from request.db.doc.find_one({})
    val = request.db.doc.find_one({})
    # val = request['db'].doc.find_one({})
    return templ('apps.app:db_test', request, {'key':val})



























