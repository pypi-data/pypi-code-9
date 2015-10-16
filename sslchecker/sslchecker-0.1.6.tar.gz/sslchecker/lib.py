# -*- coding: utf-8 -*-
from __future__ import (unicode_literals)
from .sslcert import SSLCert
from socket import setdefaulttimeout
from ssl import SSLError
import click
import datetime
import OpenSSL
import os
import pycountry
import socket
import ssl
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


FILE_PATH = os.path.dirname(__file__)
setdefaulttimeout(3)


def get_sslcert(domain):
    if ('http' in domain) or ('/' in domain):
        parse_object = urlparse(domain)
        domain = parse_object.netloc

    try:
        cert = ssl.get_server_certificate((domain, 443), ca_certs=os.path.join(FILE_PATH, 'data/cacert.pem'))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    except SSLError as err:
        raise err
    except socket.gaierror as err:
        raise err
    except socket.error as err:
        raise err
    else:
        return SSLCert(x509)


def render_cert(sslcert):
    expire_in = _expire_in(sslcert)
    secured = _secured(sslcert)
    warning = _warning(sslcert)

    secure_text = '# SSL unsecured #'
    append_secure_text = '#################'

    if secured and not warning:
        color = 'green'
        secure_text = '# SSL secured #'
        append_secure_text = '###############'
    elif secured and warning:
        color = 'yellow'
    else:
        color = 'red'

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
