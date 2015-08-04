#!/usr/bin/env python
# coding: utf-8

# from app.user_site import *
# from app.perm.perm import *
# from app.tree.tree import *

import asyncio
import aiohttp_jinja2
import jinja2


@asyncio.coroutine
def page(request):
	# dump()
	# die ( request )
	# print ( request )
	# aaa = ''
	return templ('apps.app:index', request, {'key':'val'})


# @asyncio.coroutine
# def page2(request):
	# return templ('./user_app/users_app/index.tpl', request, {'key':'val'})
	# return templ('index', request, {'key':'val'})

	# return aiohttp_jinja2.render_template('./user_app/users_app/index.tpl', request, {'key':'val'})






























