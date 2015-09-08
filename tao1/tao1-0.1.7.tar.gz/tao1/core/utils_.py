#!/usr/bin/env python
# coding: utf-8

import os, sys, time, argparse, shutil


def manage_console():
    parser = argparse.ArgumentParser()

    parser.add_argument('-project', '-startproject', '-p', type=str, help='Create project' )
    parser.add_argument('-app', '-startapp', '-a',         type=str, help='Create app'     )
    args = parser.parse_args()

    print( 'args.project', args.project)

    path_root = os.path.dirname(__file__)

    if '/core' in path_root:
        path_root = path_root[:-5]
    else:
        __import__('tao1')
        module = sys.modules['tao1']
        path_root = os.path.dirname(os.path.abspath(module.__file__))

    print ( 'path1', path_root )
    if args.project is not None:
        shutil.copytree(  os.path.join( path_root , 'sites', 'daoerp'), os.path.join( str(args.project) ) )
        set_file = """
    #!/usr/bin/env python
    # coding: utf-8

    #debug = True
    debug = False

    root = '%s'

    database={"login":"admin", "pass":"test_passwd", "host":["127.0.0.1:27017"], "port":"", 'name':'test'}
        """ % path_root

        with open(os.path.join( str(args.project) , 'settings.py'), 'w') as f: f.write(set_file)
    elif args.app != None:
        shutil.copytree( os.path.join( path_root, 'apps', 'app'), os.path.join( str(args.app) ) )

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

