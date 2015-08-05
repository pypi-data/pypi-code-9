""" goulash.docs
"""
import os
import shutil

import addict
from fabric import api
from fabric.colors import red
from peak.util.imports import lazyModule

fileserver = lazyModule('goulash.fileserver')
inspect = lazyModule('goulash._inspect')
boiler = lazyModule('goulash.boiler')

from goulash._os import copy_tree
from goulash.decorators import require_bin
from goulash.version import __version__ as version


def _get_ctx(args):
    args.docroot = os.path.abspath(args.docroot)
    DOCS_ROOT = args.docroot
    SRC_ROOT = os.path.dirname(args.docroot)
    DOCS_URL = 'http://localhost:8000'
    DOCS_API_ROOT = os.path.join(DOCS_ROOT, 'api')
    DOCS_SITE_DIR = os.path.join(DOCS_ROOT, 'site')
    PROJECT_NAME = inspect._main_package(
        SRC_ROOT, default=os.path.dirname(os.path.abspath(SRC_ROOT)))
    ctx = locals().copy()
    ctx.pop('args')
    return ctx


def docs_handler(args):
    """ """
    if args.version:
        print version.__version__
        raise SystemExit()
    elif args.boilerplate:
        args.docroot = os.path.dirname(args.docroot)
        args.dir = os.path.dirname(args.docroot)
        return boiler.gen_docs(args)
    elif args.refresh:
        return refresh(args)
    elif args.deploy:
        return deploy(args)
    elif args.show:
        return handle_show(args)


def docs_deploy(DOCS_ROOT=None, **ctx):
    """ """
    import mkdocs
    from mkdocs.config import load_config
    from mkdocs.gh_deploy import gh_deploy
    mkdocs_config = os.path.join(DOCS_ROOT, 'mkdocs.yml')
    assert os.path.exists(mkdocs_config)
    os.chdir(DOCS_ROOT)
    try:
        config = load_config(
            config_file=mkdocs_config,
        )
        gh_deploy(config)
    except mkdocs.exceptions.ConfigurationError as e:
        # Avoid ugly, unhelpful traceback
        raise SystemExit('\n' + str(e))

def skip_api_docs():
    if os.environ.get('GOULASH_DOCS_API', 'true').lower() == 'false':
        print red('skipping API documentation')
        return True
    return False

def _refresh_api_docs(PROJECT_NAME=None,
                      DOCS_ROOT=None,
                      DOCS_API_ROOT=None,
                      DOCS_SITE_DIR=None, **ctx):
    if skip_api_docs():
        return
    err = ('Missing required command.  '
           '"pip install pdoc" and try again')
    require_bin('pdoc', err)
    cmd = 'pdoc {0} --html --overwrite'
    err = 'refresh requires --project'
    assert PROJECT_NAME is not None, err
    cmd = cmd.format(PROJECT_NAME)
    with api.lcd(DOCS_API_ROOT):
        api.local(cmd)
        src = os.path.join(DOCS_API_ROOT, PROJECT_NAME)
        copy_tree(src, DOCS_API_ROOT)
        shutil.rmtree(os.path.join(DOCS_API_ROOT, PROJECT_NAME))
    if os.path.exists(DOCS_SITE_DIR):
        print red(str([DOCS_API_ROOT, DOCS_SITE_DIR]))
        src = DOCS_API_ROOT
        dest = os.path.join(DOCS_SITE_DIR, 'api')
        copy_tree(src, dest)
        dest = os.path.join(DOCS_ROOT, 'docs', 'api')
        copy_tree(src, dest)
    print red(".. finished generating api docs")


def _refresh_docs(DOCS_ROOT=None, **ctx):
    with api.lcd(DOCS_ROOT):
        api.local('mkdocs build --clean')


def docs_refresh(**ctx):
    _refresh_docs(**ctx)
    _refresh_api_docs(**ctx)

import webbrowser


def handle_show(args):
    refresh(args)
    ctx = _get_ctx(args)
    if 'docs' in os.listdir(ctx['DOCS_ROOT']):
        print red('.. found read-the-docs style documentation')
        webbrowser.open('http://localhost:8000')
        fileserver(addict.Dict(
            port=None, dir=os.path.join(
                args.docroot, 'site')))
    else:
        print red("Not sure what to do with this style of documentation")


def refresh(args):
    print red('refreshing docs..')
    docs_refresh(**_get_ctx(args))


def deploy(args):
    print red('deploying docs..')
    docs_deploy(**_get_ctx(args))
