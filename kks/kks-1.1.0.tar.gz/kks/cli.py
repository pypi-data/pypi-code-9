# coding=utf8

"""
    kks.cli
    ~~~~~~~

    kks's commandline interface.
"""

import sys
import datetime
import logging
from subprocess import call
from os.path import dirname, exists

from . import __version__
from . import src_ext
from .daemon import daemon
from .exceptions import SourceDirectoryNotFound
from .generator import generator
from .logger import logger
from .models import Post
from .server import server
from .utils import join

from docopt import docopt


usage = """Usage:
  kks [-h|-v]
  kks post [<name>]
  kks (deploy|build|clean)
  kks (serve|start) [<port>]
  kks (stop|status)


Options:
  -h --help         show help
  -v --version      show version

Commands:
  post              create a new post
  deploy            create new blog in current directory
  build             build source files to htmls
  serve             start a HTTP server and watch source changes
  clean             remove all htmls rux built
  start             start http server and rebuilder in the background
  stop              stop http server and rebuilder daemon
  status            report the daemon's status
  restart           restart the daemon
  """


def deploy_blog():
    """Deploy new blog to current directory"""
    logger.info(deploy_blog.__doc__)
    # `rsync -aqu path/to/res/* .`
    call(
        'rsync -aqu ' + join(dirname(__file__), 'res', '*') + ' .',
        shell=True)
    logger.success('Done')
    logger.info('Please edit config.toml to meet your needs')


def new_post(name):
    """Touch a new post in src/"""
    logger.info(new_post.__doc__)
    filepath = join(Post.src_dir, name + src_ext)
    # check if `src/` exists
    if not exists(Post.src_dir):
        logger.error(SourceDirectoryNotFound.__doc__)
        sys.exit(SourceDirectoryNotFound.exit_code)
    # write sample content to new post
    content = (
        'Title\n'
        'Time\n'
        'Tag\n'
        '---\n'
        'Markdown content ..'
    )
    f = open(filepath, 'w')
    f.write(content)
    f.close()
    logger.success('New post created: %s' % filepath)


def clean():
    """Clean htmls kks built: `rm -rf post page index.html`"""
    logger.info(clean.__doc__)
    paths = ['post', 'page', 'index.html']
    call(['rm', '-rf'] + paths)
    logger.success('Done')


def main():
    arguments = docopt(usage, version=__version__)
    logger.setLevel(logging.INFO)  # !important

    # valiad port argument
    port = arguments['<port>'] or '8888'
    # valiad name argument
    name = arguments['<name>'] or 'www.bcmeng.com'

    if (not port.isdigit()) or (not 0 < int(port) < 65535):
        logger.error('Port must be an integer in 0-65535.')
        sys.exit(1)
    else:
        port = int(port)

    if arguments['post']:
        new_post(name)
    elif arguments['deploy']:
        deploy_blog()
    elif arguments['build']:
        generator.generate()
    elif arguments["serve"]:
        server.run(port)
    elif arguments['clean']:
        clean()
    elif arguments['start']:
        daemon.start(port)
    elif arguments['stop']:
        daemon.stop()
    elif arguments['status']:
        daemon.status()
    else:
        exit(usage)


if __name__ == '__main__':
    main()
