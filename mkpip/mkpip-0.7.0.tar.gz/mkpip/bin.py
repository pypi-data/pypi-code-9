#!/usr/bin/env python
from datetime import datetime

def bumpv():
    from bumpy import main
    main()

def mkmod():
    from mkmod import main
    main()

def mkpip():
    import os
    import sys
    import argparse
    import fnmatch
    import shutil
    CONFIG_PATH = os.path.join(os.getenv('HOME'), '.mkpip.py')
    class Config(object):
        def __init__(self):
            self.AUTHOR = '[unknown]'
            self.EMAIL = '[unknown]'
            self.URL_PATTERN = '[unknown]/%s'
            self.COPYRIGHT_HOLDER = '[unknown]'
    config = Config()
    if os.path.isfile(CONFIG_PATH):
        d = {}
        execfile(CONFIG_PATH, d)
        config.AUTHOR = d['AUTHOR']
        config.EMAIL = d['EMAIL']
        config.URL_PATTERN = d['URL_PATTERN']
    else:
        # Using defaults defined in Config class
        print('Please create file %s and define AUTHOR, EMAIL, and '
        'URL_PATTERN' % CONFIG_PATH)
        print('URL_PATTERN should contain %s for the project name')
    parser = argparse.ArgumentParser()
    parser.add_argument('name',
        help='Name of project.')
    parser.add_argument('desc',
        help='Description of project. Will go in README.rst, setup.py, and '
        'license')
    parser.add_argument('--keywords', '-k', default='',
        help='keywords in setup.py')
    parser.add_argument('--dest', '-d', default=os.getcwd(),
        help='Destination directory that contains project folder '
        '(default .)')
    parser.add_argument('--author', '-a', default=config.AUTHOR,
        help='Author (default %s)' % config.AUTHOR)
    parser.add_argument('--email', '-e', default=config.EMAIL,
        help="Author's email (default %s)" % config.EMAIL)
    parser.add_argument('--year', '-y', default=str(datetime.now().year),
        help="copyright year (default %s)" % str(datetime.now().year))
    parser.add_argument('--copyright-holder', '-c', default=config.COPYRIGHT_HOLDER,
        help="copyright holder (default %s)" % config.COPYRIGHT_HOLDER)
    parser.add_argument('--license-path', '--lp',
        help='custom license template path')
    parser.add_argument('--license', '-l', default='GPLv3+',
        help='license in setup.py')
    parser.add_argument('--url', '-r', default=None,
        help="Url for project's repo (default from config's URL_PATTERN %% project_name)")
    args = parser.parse_args()
    if args.url is None:
        args.url = config.URL_PATTERN % args.name
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bp_dir = os.path.join(base_dir, 'boilerplate')
    pip_dir = os.path.join(args.dest, args.name)
    bad_mkpip_dir = os.path.join(pip_dir, 'mkpip')
    if os.path.exists(pip_dir):
        print('%s already exists.' % pip_dir)
        sys.exit(1)
    shutil.copytree(bp_dir, pip_dir)
    if os.path.isdir(bad_mkpip_dir):
        shutil.rmtree(bad_mkpip_dir)
    for root, dirnames, filenames in os.walk(pip_dir):
        for filename in fnmatch.filter(filenames, '*.pyc'):
            os.remove(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, 'bin.*'):
            os.remove(os.path.join(root, filename))
    if args.license.startswith('GPL'):
        license_long = '\'License :: OSI Approved :: GNU General Public License v3 or later (%s)\',' % args.license
    elif args.license.startswith('BSD'):
        license_long = '\'License :: OSI Approved :: BSD License\','
    else:
        license_long = ''
    rewrite = {
        'name': args.name,
        'desc': args.desc,
        'keywords': args.keywords,
        'underline': len(args.name) * '=',
        'author': args.author,
        'email': args.email,
        'url': args.url,
        'year': args.year,
        'copyright_holder': args.copyright_holder,
        'license': args.license,
        'license_long': license_long
    }
    files = [
        '.gitignore', 
        'setup.pyt',
        'README.rst',
        'MANIFEST.in',
        'LICENSE',
        'name/__init__.pyt',
    ]
    for name in files:
        path = os.path.join(pip_dir, name)
        with open(path) as f:
            r = f.read()
        new = r % rewrite
        with open(path, 'w') as f:
            f.write(new)
    if args.license_path:
        path = os.path.join(pip_dir, 'LICENSE')
        with open(args.license_path) as f:
            r = f.read()
        new = r % rewrite
        with open(path, 'w') as f:
            f.write(new)
    for name in files:
        path = os.path.join(pip_dir, name)
        if path.endswith('.pyt'):
            shutil.move(path, path[:-1])
    name_dir = os.path.join(pip_dir, 'name')
    new_dir = os.path.join(pip_dir, rewrite['name'])
    os.system('mv %s %s' % (name_dir, new_dir))

