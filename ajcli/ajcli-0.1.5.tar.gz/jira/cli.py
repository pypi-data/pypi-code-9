#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

# TODO fix this thing!

import click, logging

from . import service, util

log = logging.getLogger('jiracli')

def format(arg, pretty):
    """format

    :param arg:
    :param pretty:
    """
    if pretty:
        return util.pretty(arg)
    else:
        return arg

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--debug/--no-debug', default=False)
@click.option('--pretty/--ugly', default=True)
@click.option('--host', prompt=True)
@click.option('-u', '--user', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
@click.pass_context
def cli(ctx, debug, host, user, password, pretty):
    """TODO: Docstring for jiracli."""
    logging.basicConfig(level   = logging.DEBUG if debug else logging.WARN,
                        format  = '%(asctime)s [%(name)s|%(levelname)s] %(message)s',
                        datefmt = '%H:%M:%S')

    ctx.obj['service'] = service.Service(host, user, password, 'rest/api/2')
    ctx.obj['pretty'] = pretty

@cli.command()
@click.pass_context
def myself(ctx):
    """TODO: Docstring for myself"""
    print(format(ctx.obj['service'].myself(), ctx.obj['pretty']))

@cli.command()
@click.option('--max-results', default=-1)
@click.option('--total/--no-total', default=True)
@click.option('--worklogs/--no-worklogs', default=True)
@click.option('-f', '--field', multiple=True)
@click.argument('filter', nargs=-1)
@click.pass_context
def issues(ctx, max_results, total, worklogs, field, filter):
    """TODO: Docstring for issues."""
    jira = ctx.obj['service']

    issue_gen = jira.issues(max_results, filter, worklogs)

    if not total:
        print(format(issue_gen, ctx.obj['pretty']))
    else:
        output = {'total_hours': 0, 'total_estimate': 0, 'total_velocity': 0, 'issues': []}

        for issue in issue_gen:
            output['issues'].append(issue)
            output['total_hours'] += issue.total_hours
            output['total_estimate'] += issue.estimate

        output['total_velocity'] = util.calculate_velocity(output['total_estimate'], output['total_hours'])

        print(format(output, ctx.obj['pretty']))

@cli.command()
@click.option('-u', '--user', multiple=True)
@click.argument('filter', nargs=-1)
@click.pass_context
def worklogs(ctx, user, filter):
    """TODO: Docstring for issues."""
    jira = ctx.obj['service']

    logs = {'total_hours': 0}

    issue_list = jira.issues(-1, filter, True)

    for issue in issue_list:
        logs[issue.key] = [ log for log in issue.worklog if len(user) == 0 or log.author in user ]
        if len(logs[issue.key]) > 0:
            for log in logs[issue.key]:
                logs['total_hours'] += log.total_hours
        else:
            del logs[issue.key]

    print(format(logs, ctx.obj['pretty']))

@cli.command()
@click.pass_context
def projects(ctx):
    """TODO: Docstring for issues."""
    print(format(ctx.obj['service'].projects(), ctx.obj['pretty']))

@cli.command()
@click.option('--max-results', default=-1)
@click.option('--worklogs/--no-worklogs', default=False)
@click.argument('name', nargs=-1)
@click.pass_context
def user(ctx, max_results, worklogs, name):
    """TODO: Docstring for issues."""
    for entry in name:
        print(format(ctx.obj['service'].user(max_results, entry, None), ctx.obj['pretty']))

@cli.command()
@click.option('--max-results', default=-1)
@click.option('--worklogs/--no-worklogs', default=False)
@click.argument('project')
@click.pass_context
def users(ctx, max_results, worklogs, project):
    """TODO: Docstring for issues."""
    print(format(ctx.obj['service'].users(max_results, project), ctx.obj['pretty']))

def run():
    try:
        cli(obj={})
    except service.StatuscodeException as e:
        if e.status_code == 401 and "Unauthorized" in e.message:
            # WAT
            log.error('Authorization failed!')
        else:
            raise
    except Exception as e:
        logging.exception(e)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
