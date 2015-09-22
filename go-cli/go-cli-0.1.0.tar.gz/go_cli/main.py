""" Command line interface to Vumi Go HTTP APIs. """

import click

import go_cli.send


class GoCliContext(object):
    def __init__(self):
        self.account_key = None


@click.group(name="go-cli")
@click.version_option()
@click.option('--account', '-a', help='Vumi Go account key')
@click.pass_context
def cli(ctx, account):
    """ Vumi Go command line utility. """
    ctx.auto_envvar_prefix = 'GO_CLI'
    ctx.obj = GoCliContext()
    ctx.obj.account_key = account


cli.command('send')(go_cli.send.send)
