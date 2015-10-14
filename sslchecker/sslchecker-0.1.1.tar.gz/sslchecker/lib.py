# -*- coding: utf-8 -*-
from __future__ import (unicode_literals)
from .sslcert import SSLCert
import OpenSSL
import socket
import ssl
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def get_sslcert(domain):
    if ('http' in domain) or ('/' in domain):
        parse_object = urlparse(domain)
        domain = parse_object.netloc

    try:
        cert = ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    except socket.gaierror as err:
        raise err
    except socket.error as err:
        raise err
    else:
        return SSLCert(x509)
