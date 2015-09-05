#!/usr/bin/env python
# coding: utf-8

import os, time
import asyncio

from pymongo import *

import argparse
import shutil


parser = argparse.ArgumentParser()


parser.add_argument('-project', '-startproject', '-p', type=str, help='Create project' )
parser.add_argument('-app', '-startapp', '-a',         type=str, help='Create app'     )
args = parser.parse_args()

if args.project != None:
    print(args.project)
    # os.mkdir('./'+str(args.project)+'/')
    shutil.copytree( os.path.dirname(__file__)[:-5]+'/sites/daoerp', './'+str(args.project) )
    set_file = """
#!/usr/bin/env python
# coding: utf-8

#debug = True
debug = False

root = '%s'

database={"login":"admin", "pass":"test_passwd", "host":["127.0.0.1:27017"], "port":"", 'name':'test'}
	""" % os.path.dirname(__file__)[:-5] 

    with open(os.path.join( str(args.project) , 'settings.py'), 'w') as f: f.write(set_file)
    print('ppp', os.getcwd()[:-5])
elif args.app != None:
    print( "=======================================",  os.path.dirname(__file__), "==============", os.getcwd()  )
    print(args.app)

    # os.mkdir('./'+str(args.app)+'/')
    
    print( os.getcwd())
    shutil.copytree( os.path.dirname(__file__)[:-5]+'/apps/app', './'+str(args.app) )

    print('aaa', os.getcwd()[:-5] )

print( args )























# os.mkdir('/backups2/')
# import shutil
# shutil.copytree('/home/smirnov/test', '/home/smirnov/wsd/test')



# set_file = """
# 	import os, sys
# 	sys.path.append('/home/user/workspace/django/dj')
# 	os.environ['DJANGO_SETTINGS_MODULE'] = 'dj.settings'
# 	import django.core.handlers.wsgi
# 	application = django.core.handlers.wsgi.WSGIHandler()
# """
# with open(os.path.join(pr_path, prog_name, 'settings.py'), 'w') as f: f.write(set_file)

