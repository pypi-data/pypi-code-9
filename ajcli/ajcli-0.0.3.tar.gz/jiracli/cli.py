#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import click, logging

from . import service

log = logging.getLogger('jiracli')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--pretty/--ugly', default=True)
@click.option('--host', required=True)
@click.option('-u', '--user', prompt=True)
@click.password_option()
@click.pass_context
def cli(ctx, host, user, password, pretty):
    """TODO: Docstring for jiracli."""
    ctx.obj['service'] = service.Service(host, user, password, 'rest/api/2', pretty)

list_choices = ['issues', 'users']

@cli.command()
@click.pass_context
def myself(ctx):
    print(ctx.obj['service'].myself())

@cli.command()
@click.option('--max-results', default=-1)
@click.option('-f', '--field', multiple=True)
@click.argument('filter', nargs=-1)
@click.pass_context
def issues(ctx, max_results, field, filter):
    """TODO: Docstring for issues.

    :ctx: TODO
    :max_results: TODO
    :project: TODO
    :returns: TODO

    """
    print(ctx.obj['service'].issues(max_results, field, filter))

@cli.command()
@click.option('--max-results', default=-1)
@click.argument('filter', nargs=-1)
@click.pass_context
def worklog(ctx, max_results, filter):
    """TODO: Docstring for issues.

    :ctx: TODO
    :max_results: TODO
    :project: TODO
    :returns: TODO

    """
    print(ctx.obj['service'].worklog(max_results, filter))

@cli.command()
@click.option('--max-results', default=-1)
@click.pass_context
def projects(ctx, max_results):
    """TODO: Docstring for issues.

    :ctx: TODO
    :max_results: TODO
    :project: TODO
    :returns: TODO

    """
    jira = ctx.obj['service']

    print(jira.projects(max_results))

@cli.command()
@click.option('--max-results', default=-1)
@click.pass_context
def users(ctx, max_results):
    """TODO: Docstring for issues.

    :ctx: TODO
    :max_results: TODO
    :project: TODO
    :returns: TODO

    """
    jira = ctx.obj['service']

    print(jira.users(max_results))

def run():
    # logging.basicConfig(level=logging.DEBUG)
    cli(obj={})

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
