""":mod:`sslchecker.cli` --- Command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import click
import sys

from .lib import get_sslcert, render_cert


@click.command()
@click.argument('domain')
def cli(domain):
    """A simple SSL certificates validator on your command line."""
    try:
        sslcert = get_sslcert(domain)
    except:
        click.secho("#################", fg='red', bold=True)
        click.secho("# SSL unsecured #", fg='red', bold=True)
        click.secho("#################", fg='red', bold=True)
        click.echo("No SSL certificates were found on {}.".format(domain))
        sys.exit()

    render_cert(sslcert)
