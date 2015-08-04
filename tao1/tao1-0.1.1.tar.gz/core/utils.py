#!/usr/bin/env python
# coding: utf-8
import time

def locale_date(format, dt, loc = 'en_US.UTF-8'):
	""" dt - кортеж """
	import locale
	lc = locale.getdefaultlocale()
	# lc = locale.getlocale(locale.LC_ALL)
	locale.setlocale(locale.LC_ALL, loc)
	res = time.strftime(format, dt)
	locale.setlocale(locale.LC_ALL, lc)
	return res
