from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

"""
Get package download statistics from PyPI
"""

# Based on https://github.com/collective/Products.PloneSoftwareCenter\
# /commit/601558870175e35cfa4d05fb309859e580271a1f

# For sorting XML-RPC results

from collections import deque

# HTTPS connection for normalize function

try:
    from http.client import HTTPSConnection
except ImportError:
    from httplib import HTTPSConnection

import json
import time

# PyPI's XML-RPC methods
# https://wiki.python.org/moin/PyPIXmlRpc

try:
    import xmlrpc.client as xmlrpc
except ImportError:  # Python 2
    import xmlrpclib as xmlrpc

PYPI_HOST = 'pypi.python.org'
PYPI_URL = 'https://%s/pypi' % PYPI_HOST
PYPI_JSON = '/'.join([PYPI_URL, '%s/json'])
PYPI_XML = xmlrpc.ServerProxy(PYPI_URL)

# PyPI JSON
# http://stackoverflow.com/a/28786650

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def by_two(source):
    """
    """
    out = []
    for x in source:
        out.append(x)
        if len(out) == 2:
            yield out
            out = []


def count_downloads(package, version=None, json=False):
    """
    """
    count = 0
    items = []
    for urls, data in get_release_info([package], json=json):
        for url in urls:
            filename = url['filename']
            downloads = url['downloads']
            if not json:
                upload_time = url['upload_time'].timetuple()
                upload_time = time.strftime('%Y-%m-%d', upload_time)
            else:
                # Convert 2011-04-14T02:16:55 to 2011-04-14
                upload_time = url['upload_time'].split('T')[0]
            if version == data['version'] or not version:
                items.append(
                    {
                        'upload_time': upload_time,
                        'filename': filename,
                        'downloads': downloads,
                    }
                )
                count += url['downloads']
    return count, items


# http://stackoverflow.com/a/28786650
def get_jsonparsed_data(url):
    """Receive the content of ``url``, parse it as JSON and return the
       object.
    """
    response = urlopen(url)
    data = str(response.read())
    return json.loads(data)


def normalize(name):
    """
    """
    http = HTTPSConnection(PYPI_HOST)
    http.request('HEAD', '/pypi/%s/' % name)
    r = http.getresponse()
    if r.status not in (200, 301):
        raise ValueError(r.reason)
    return r.getheader('location', name).split('/')[-1]


def get_releases(packages):
    """
    """
    mcall = xmlrpc.MultiCall(PYPI_XML)
    called_packages = deque()
    for package in packages:
        mcall.package_releases(package, True)
        called_packages.append(package)
        if len(called_packages) == 100:
            result = mcall()
            mcall = xmlrpc.MultiCall(PYPI_XML)
            for releases in result:
                yield called_packages.popleft(), releases
    result = mcall()
    for releases in result:
        yield called_packages.popleft(), releases


def get_release_info(packages, json=False):
    """
    """
    if json:
        for package in packages:
            data = get_jsonparsed_data(PYPI_JSON % package)
            for release in data['releases']:
                urls = data['releases'][release]
                yield urls, data['info']
        return

    mcall = xmlrpc.MultiCall(PYPI_XML)

    i = 0
    for package, releases in get_releases(packages):
        for version in releases:
            mcall.release_urls(package, version)
            mcall.release_data(package, version)
            i += 1
            if i % 50 == 49:
                result = mcall()
                mcall = xmlrpc.MultiCall(PYPI_XML)
                for urls, data in by_two(result):
                    yield urls, data

    result = mcall()
    for urls, data in by_two(result):
        yield urls, data


def get_stats(package):

    grand_total = 0

    if '==' in package:
        package, version = package.split('==')
    try:
        package = normalize(package)
        version = None
    except ValueError:
        raise RuntimeError('No such module or package %r' % package)

    # Count downloads
    total, releases = count_downloads(
        package,
        json=True,
        version=version,
    )

    result = {
        'version': version,
        'downloads': total or 0,
        'releases': releases,
    }

    grand_total += total

    return result, grand_total, version
