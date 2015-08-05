#!/usr/bin/env python

import sys
import click

import xpcs.pcs
import xpcs.resource
import xpcs.node
import xpcs.globals


@click.group()
@click.option('--quiet', '-q', is_flag=True)
@click.option('--status')
@click.pass_context
def cli(ctx, quiet=False, status=None):
    xpcs.globals.quiet = quiet
    ctx.obj = xpcs.pcs.PCS(statusfile=status)


cli.add_command(xpcs.resource.cli)
cli.add_command(xpcs.node.cli)


if __name__ == '__main__':
    cli()
