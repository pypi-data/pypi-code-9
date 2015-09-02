#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import os, click, logging, coloredlogs

from . import manager, utils, exceptions, version

log = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(short_help=__name__, context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--debug/--no-debug', default=False)
@click.option('-v', '--verbose/--no-verbose', default=False)
@click.option('-s', '--storage-dir', type=click.Path(),
        help='where to store files')
@click.option('-l', '--link-dir', type=click.Path(),
        help='where to link stored files')
@click.pass_context
def cli(ctx, debug, verbose, storage_dir, link_dir):
    """
    Store files in a git repository and replace them with links while keeping
    the original structure.
    """
    if debug:
        loglevel = logging.DEBUG
    elif verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    coloredlogs.install(level=loglevel, show_timestamps=False,
                                        show_hostname=False,
                                        show_name=debug)

    if storage_dir is None:
        storage_dir = os.path.expanduser('~/.ltg')
    if link_dir is None:
        link_dir = os.path.expanduser('~/')

    ctx.obj['manager'] = manager.Manager(storage_dir, link_dir)

# store

@cli.command(short_help='add a new files to storage')
@click.argument('files', type=click.Path(exists=True), nargs=-1, required=False)
@click.option('--relative-to', type=click.Path())
@click.option('-c', '--category', default='general')
@click.option('-f', '--force/--no-force', default=False)
@click.pass_context
def store(ctx, files, relative_to, category, force):
    """
    Store a new file in the storage directory, leave the original.
    """
    ctx.obj['manager'].store(files, relative_to, category, force)

# link

@cli.command(short_help='link stored files')
@click.option('-f', '--force/--no-force', default=False)
@click.pass_context
def link(ctx, force):
    """
    Link all stored files to the linker directory.
    """
    ctx.obj['manager'].link(force)

# add (store + link)

@cli.command(short_help='add and link new files')
@click.argument('files', type=click.Path(exists=True), nargs=-1, required=False)
@click.option('--relative-to', type=click.Path())
@click.option('-c', '--category', default='general')
@click.option('-f', '--force/--no-force', default=False)
@click.pass_context
def add(ctx, files, relative_to, category, force):
    """
    Store a new file in the storage directory and replace the original with a
    link.
    """
    ctx.obj['manager'].store(files, relative_to, category, force)
    ctx.obj['manager'].link(True)

# unlink

@cli.command(short_help='unlink files or categories')
@click.argument('files', type=click.Path(), nargs=-1)
@click.option('-c', '--category')
@click.option('-r', '--recursive/--non-recursive', default=False)
@click.pass_context
def unlink(ctx, files, category, recursive):
    """
    Replace linked files with their original.
    """
    ctx.obj['manager'].unlink(files)

# rm

@cli.command(short_help='remove stored files or categories')
@click.argument('files', type=click.Path(), nargs=-1)
@click.option('-r', '--recursive/--no-recursive', default=False)
@click.option('-f', '--force/--no-force', default=False)
@click.pass_context
def rm(ctx, files, recursive, force):
    """
    Remove files from the storage directory.

    WARNING: Not yet implemented!
    """
    ctx.obj['manager'].remove(files, recursive, force)

# mv

@cli.command(short_help='move stored files')
@click.argument('src', type=click.Path(exists=True))
@click.argument('dst', type=click.Path())
@click.option('-f', '--force/--no-force', default=False)
@click.pass_context
def mv(ctx, src, dst, force):
    """
    Move files from one place to the other.

    WARNING: This does not yet work for directories!
    """
    ctx.obj['manager'].move(src, dst, force)

# git

@cli.command(short_help='run git commands in storage dir')
@click.argument('args', nargs=-1)
@click.pass_context
def git(ctx, args):
    """
    Send commands to git, use '--' to avoid ltg interpreting commands as its own:

    $ ltg git -- commit --interactive

    """
    ctx.obj['manager'].git(*args)

# info

@cli.command(short_help='print general information')
@click.pass_context
def info(ctx):
    """
    Print version and used directories.
    """
    print('ltg %s' % version.__version__)
    print('storage: %s' % ctx.obj['manager'].storage_dir())
    print('linker: %s' % ctx.obj['manager'].linker_dir())

###############

def exception_msg(exception):
    """exception_msg

    :param exception:
    """
    return "%s: %s" % (exception.__class__.__name__, exception)

def run():
    """run"""
    try:
        cli(obj={})
    except exceptions.FileExistsError as e:
        log.error("file exists, use --force to ovewrite: %s", e)
        exit(1)
    except (NotImplementedError, exceptions.LTGException) as e:
        log.error(exception_msg(e))
        exit(1)
    except Exception as e:
        log.exception(e)
        exit(1)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
