""":mod:`sslchecker.cli` --- Command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import click
import datetime
import pycountry
import sys

from .lib import get_sslcert


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

    expire_in = _expire_in(sslcert)
    secured = _secured(sslcert)
    warning = _warning(sslcert)

    secure_text = '# SSL secured #'
    append_secure_text = '###############'

    if secured and not warning:
        color = 'green'
    elif secured and warning:
        color = 'yellow'
    else:
        color = 'red'
        secure_text = '# SSL unsecured #'
        append_secure_text = '#################'

    click.secho("{}".format(append_secure_text), fg=color, bold=True)
    click.secho("{}".format(secure_text), fg=color, bold=True)
    click.secho("{}\n".format(append_secure_text), fg=color, bold=True)

    click.echo("Common name: {0.cn}".format(sslcert))
    click.echo("Valid from: {0.notbefore}".format(sslcert))

    if secured:
        click.echo("Expiration date: {0.notafter}".format(sslcert))
        click.echo("\tExpire in {0} days.\n".format(expire_in))
    else:
        click.secho("Expiration date: {0.notafter}".format(sslcert), fg='red')

    click.echo("Signature Algorithm: {0.keyinfo[0]}".format(sslcert))
    click.echo("Key length: {0.keyinfo[1]}".format(sslcert))
    click.echo("Issued by:".format(sslcert))
    for issuer in sslcert.issuer:
        cat_name = issuer[0]
        cat_value = issuer[1]
        cat = ''
        if cat_name == 'O':
            cat = 'Organization'
        elif cat_name == 'C':
            cat = 'Country'
            cat_value = pycountry.countries.get(alpha2=cat_value).name
        elif cat_name == 'OU':
            cat = 'Organization unit'
        elif cat_name == 'CN':
            cat = 'Common name'
        elif cat_name == 'ST':
            cat = 'State'
        elif cat_name == 'L':
            cat = 'Locality'

        click.echo("\t{0}: {1}".format(cat, cat_value))

    return None


def _warning(sslcert):
    return (0 < _expire_in(sslcert)) and (_expire_in(sslcert) < 30)


def _secured(sslcert):
    return not sslcert.has_expired


def _expire_in(sslcert):
    d = sslcert.notafter - datetime.datetime.now()
    return d.days
