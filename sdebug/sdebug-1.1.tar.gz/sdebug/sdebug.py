# -*- coding: utf-8 -*-
#    Copyright (C) 2015 by
#    Moreno Bonaventura <morenobonaventura@gmail.com>
#    This is Free Software - You can use and distribute it under
#    the terms of the GNU General Public License, version 3 or later.
"""
simple debug
"""
__author__ = 'Moreno Bonaventura (morenobonaventura@gmail.com)'
__all__ = ['DEBUG','DEBUGn','DEBUGr','clockSLEEP']

import sys,time
import sdebug

def DEBUG(s):
     sys.stderr.write(str(s))

def DEBUGn(s):
     sys.stderr.write(str(s)+'\n')

def DEBUGr(s):
     sys.stderr.write(str(s)+'\r')

def clockSLEEP(t):
	for i in range(0,t):
		DEBUGr(str(i)+'-----')
		time.sleep(1)

	
