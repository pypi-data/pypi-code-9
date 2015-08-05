""" goulash.boiler
"""
from __future__ import print_function
import shutil
import os

import addict
from fabric import api
from fabric.colors import red
from jinja2 import Template
from goulash import goulash_data
from goulash._os import copy_tree, copy_file
from goulash._os import touch, makedirs
from goulash._inspect import _main_package
from goulash.decorators import require_bin
from goulash.docs import _refresh_docs, _refresh_api_docs


def gen_docs(args):
    """ """
    SRC_ROOT = args.dir or '.'
    DOCS_ROOT = os.path.join(SRC_ROOT, 'docs')
    print(red('.. generating docs boilerplate:'), DOCS_ROOT)
    DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
    DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')
    PROJECT_NAME = _main_package(
        SRC_ROOT, default=os.path.dirname(os.path.abspath(SRC_ROOT)))
    assert PROJECT_NAME
    ctx = locals().copy()
    ctx.pop('args')
    create_docs(**ctx)


def create_docs(PROJECT_NAME=None, DOCS_ROOT=None, **ctx):
    """ """
    if not os.path.exists(DOCS_ROOT):
        msg = red('..docs root ') +\
            '"{0}"'.format(DOCS_ROOT) + \
            red(' does not exist, creating it')
        print(msg)
        api.local('mkdir -p "{0}"'.format(DOCS_ROOT))
    else:
        msg = '.. docs root already exists:'
        print(red(msg) + ' {0}'.format(DOCS_ROOT))
    shutil.copy(
        os.path.join(goulash_data, 'docs_requirements.txt'),
        os.path.join(DOCS_ROOT, 'requirements.txt'))
    _create_docs(PROJECT_NAME=PROJECT_NAME,
                 DOCS_ROOT=DOCS_ROOT, **ctx)
    _create_api_docs(
        DOCS_ROOT=DOCS_ROOT,
        PROJECT_NAME=PROJECT_NAME,
        **ctx)


def _create_docs(PROJECT_NAME=None, DOCS_ROOT=None, **ctx):
    mkdocs_config = os.path.join(DOCS_ROOT, 'mkdocs.yml')
    assert PROJECT_NAME
    def dl_bp():
        shutil.copy(
            os.path.join(goulash_data,
                         'mkdocs.yml'),
            mkdocs_config)
        with open(mkdocs_config, 'r') as fhandle:
            tmp = fhandle.read().format(project_name=PROJECT_NAME)
        with open(mkdocs_config, 'w') as fhandle:
            fhandle.write(tmp)
    require_bin('mkdocs',
                'Missing required command.  "pip install mkdocs" and try again')
    print(red(".. generating mkdocs: ") + DOCS_ROOT)
    if not os.path.exists(DOCS_ROOT):
        msg = red('.. mkdocs dir at "{0}" '.format(DOCS_ROOT)) + \
            red(' does not exist, creating it')
        print(msg)
        os.mkdir(DOCS_ROOT)
    cmd = ('mkdocs new {0}').format(DOCS_ROOT)
    api.local(cmd)

    print(red("creating placeholder for API documentation.."))
    makedirs(os.path.join(DOCS_ROOT, 'docs', 'api'))
    touch(os.path.join(DOCS_ROOT, 'docs', 'api', 'index.html'))

    if not os.path.exists(mkdocs_config):
        print(red(' .. {0} not found '.format(mkdocs_config)))
        print(red(' .. no config for docs, using standard boilerplate'))
        dl_bp()
    with open(mkdocs_config, 'r') as fhandle:
        if fhandle.read().strip().endswith('My Docs'):
            msg = red(' .. brand new docs!')
            msg += ' using standard boilerplate'
            print(msg)
            #default_config = True
            dl_bp()
    print(red(".. copying custom mkdocs theme"))

    src = os.path.join(goulash_data, 'glsh')
    dest = os.path.join(DOCS_ROOT, 'glsh')
    copy_tree(src, dest)
    print(red(".. refreshing docs"))
    _refresh_docs(DOCS_ROOT=DOCS_ROOT, **ctx)
    print(red(".. finished with mkdocs"))
from goulash.docs import skip_api_docs
def _create_api_docs(DOCS_API_ROOT=None, **ctx):
    if skip_api_docs():
        return
    msg = red("..generating api documentation to")
    msg += " {0}".format(DOCS_API_ROOT)
    print(msg)
    if not os.path.exists(DOCS_API_ROOT):
        msg = red('.. api dir at "{0}" '.format(DOCS_API_ROOT))
        msg += red(' does not exist, creating it')
        print(msg)
        os.mkdir(DOCS_API_ROOT)
    _refresh_api_docs(DOCS_API_ROOT=DOCS_API_ROOT, **ctx)


def gen_project(args):
    SRC_ROOT = args.dir or '.'
    SRC_ROOT = os.path.abspath(SRC_ROOT)
    if not os.path.exists(SRC_ROOT):
        makedirs(SRC_ROOT)
        print(red(".. source root created:"), SRC_ROOT)
    else:
        print(red(".. source root already exists: "), SRC_ROOT)
    guess_name = os.path.split(SRC_ROOT)[-1]
    gen_pkg(addict.Dict(
        dir=os.path.join(SRC_ROOT, guess_name),
        pkg=True,
        pkg_name=args.pkg_name or guess_name,
        project_name=guess_name))
    #gen_docs(addict.Dict(dir=SRC_ROOT, docs=True))


def gen_tox(args):
    pass


def gen_pkg(args):
    from goulash import goulash_data
    PKG_ROOT = args.dir
    PKG_ROOT = os.path.abspath(PKG_ROOT)
    PKG_NAME = args.pkg_name.replace('-', '_').replace(' ', '')
    SRC_ROOT = os.path.dirname(PKG_ROOT)
    if not os.path.exists(PKG_ROOT):
        makedirs(PKG_ROOT)
        print(red(".. pkg root created:"), PKG_ROOT)
    else:
        print(red(".. pkg root already exists: "), PKG_ROOT)
    src = os.path.join(goulash_data, 'pkg')
    dest = os.path.join(PKG_ROOT)
    copy_tree(src, dest, update=True)
    dest = setup_py = os.path.join(SRC_ROOT, 'setup.py')
    copy_file(os.path.join(goulash_data, 'setup.py'), dest)  # , update=True)
    print(red(".. copied setup.py: "), dest)
    with open(setup_py, 'rw') as fhandle:
        content = fhandle.read()
    with open(setup_py, 'w') as fhandle:
        new_content = Template(content).render(
            author=args.author,
            project_name=args.project_name,
            pkg_name=args.package_name,
        )
        fhandle.write(new_content)
    print(red(".. filling setup.py from template"), setup_py)


def boiler_handler(args):
    """ """
    if args.project:
        gen_project(args)
    elif args.docs:
        gen_docs(args)
    elif args.pkg:
        gen_pkg(args)
