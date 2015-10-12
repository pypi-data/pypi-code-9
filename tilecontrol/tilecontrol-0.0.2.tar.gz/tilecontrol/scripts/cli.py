# Skeleton of a CLI

import click

import tilecontrol


@click.command('tilecontrol')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(tilecontrol.has_legs)
