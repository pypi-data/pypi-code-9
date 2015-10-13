# -*- coding: utf-8 -*-
# Copyright (c) 2015, RedJack, LLC.
# All rights reserved.
#
# Please see the COPYING file in this distribution for license details.
from contextlib import closing
import ipaddress
import itertools
import socket
import struct
import sys

from . import exceptions
from . import status


__version__ = '0.3.0'

__all__ = ['EdgeScape', 'status', 'exceptions', 'EDGESCAPE_VERSION']


BUFFER_SIZE = 1024
EDGESCAPE_VERSION = 3
DEFAULT_RESPONSE_DATA = {'default_answer': True, 'default_source': 'client'}

INTEGER_FIELDS = ('dma', 'msa', 'pmsa', 'areacode', 'asnum', 'bw')
FLOAT_FIELDS = ('lat', 'long')
MULTIVALUE_FIELDS = ('areacode', 'county', 'fips', 'zip', 'asnum')
BOOLEAN_FIELDS = ('default_answer',)


PY2 = sys.version_info[0] == 2


if PY2:
    string_types = basestring,
else:
    string_types = str,


class EdgeScape(object):
    """
    Akamai EdgeScape client.
    """

    def __init__(self, host='127.0.0.1', port=2001):
        self.host = host
        self.port = port

    def __repr__(self):
        return '<%s(host=%s, port=%s)>' % (self.__class__.__name__,
                                           self.host, self.port)

    def ip_lookup(self, ip, timeout=1):
        """
        Return a `dict` with all of the Akamai-provided data about an IP
        address.

        Note that this does not return the Akamai data exactly as provided by
        Akamai. Rather, integers will be converted to integers, floats to
        floats, and multivalue or range fields to lists.

        Note that 'zip' and 'fips' codes will be returned as lists of strings
        in order to preserve any leading zeroes. However, any zip code ranges
        provided by Akamai will be fully expanded, so that downstream
        applications can query by zip code. For example, if Akamai returns
        '00901-00911', this will return
        `['00901', '00902', ..., '00910', '00911']` so that
        `'00910' in result['zip'] == True`.

        - Raises `ValueError` if the IP address is invalid.
        - Raises `socket.timeout` if there is no response within `timeout`
          seconds.
        - Raises `akadata.exceptions.EdgeScapeException` or a subclass if the
          Akamai response is invalid.
        """
        if PY2 and isinstance(ip, str):  # pragma: no cover
            ip = ip.decode('utf-8')
        # Raise a ValueError if `ip` is not a valid IPv4 or IPv6 address.
        ipaddress.ip_address(ip)

        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.settimeout(timeout)
            sock.sendto(_pack_ip(ip), (self.host, self.port))

            resp = sock.recv(BUFFER_SIZE)

        result_str, status_code = _validate_result(resp, ip)

        if status_code == status.AKAMAI_DEFAULT:
            result_dict = DEFAULT_RESPONSE_DATA.copy()
        else:
            result_dict = _edgescape_result_to_dict(result_str)

        # EdgeScape does not include the IP address in its result
        result_dict['ip'] = ip

        return result_dict


def _pack_ip(ip):
    """Pack an IPv4/IPv6 address into the EdgeScape query format."""
    # Akamai's Perl client sets the query number to the current timestamp, the
    # C and Java clients use random numbers, and the PHP client is always 0.
    # We'll follow the behavior of the PHP client to simplify testing.
    query_no = 0

    # All of the Akamai clients set flags=0 in the query and only the Java
    # client even gives it a name.
    flags = 0

    # IP addresses will always be ASCII strings. Invalid user input will have
    # already raised an error in the public `ip_lookup` method.
    ip = ip.encode('ascii')

    # In Perl: CCnnCCa*
    return struct.pack('!BBHHBB{}s'.format(len(ip)),
                       EDGESCAPE_VERSION, flags, query_no, BUFFER_SIZE, 0, 0, ip)


def _validate_result(data, ip):
    """
    Parse and validate the response from EdgeScape Facilitator.

    If the response is invalid or contains an error, raises
    `akadata.exceptions.EdgeScapeException` or one of its subclasses.

    If the response is valid, returns a tuple of the unpacked result (as a
    string) and the status code.
    """
    # In Perl: CCnnSa*
    unpacked = struct.unpack('!BBHHBB{}s'.format(len(data) - 8), data)
    version, flags, _, size, status_code, _, result = unpacked

    if version != EDGESCAPE_VERSION:
        raise exceptions.InvalidVersion(status_code=status_code,
                                        query_version=EDGESCAPE_VERSION,
                                        result_version=version)
    elif flags != 0 or size != len(data):
        raise exceptions.EdgeScapeException(status_code=status_code)
    elif status_code not in (status.AKAMAI_OK, status.AKAMAI_DEFAULT):
        raise exceptions.EdgeScapeException(status_code=status_code)

    result_address, result = result[:len(ip)], result[len(ip):]
    result_address = result_address.decode('ascii')
    result = result.decode('utf-8')

    if result_address != ip:
        raise exceptions.InvalidAddress(status_code=status_code,
                                        query_address=ip,
                                        result_address=result_address)
    return result, status_code


def _edgescape_result_to_dict(data):
    """
    Convert the EdgeScape result (a string of null-byte delimited key=val
    pairs) to a `dict`, converting data types as appropriate.

    When possible, converts integers to `int`s and floats to `float`s. If a
    value cannot be converted (e.g. a private IP address with an asnum of
    'reserved', the original string will be retained.  Multivalue and range
    (encoded by Akamai with '+' and '-') fields will *always* be converted to
    `list`s, even if there is only one element.
    """
    data = dict(
        field.split('=', 1)
        for field in data.split('\0') if field.strip()
    )

    # Always include a 'default_answer' key so consumers can quickly tell if
    # a response came from Akamai or not.
    data.setdefault('default_answer', False)

    for field in MULTIVALUE_FIELDS:
        orig_value = data.get(field)

        if orig_value is None:
            continue

        data[field] = orig_value.split('+')

    # Akamai returns US/PR zip codes as numeric ranges, e.g. 20901-20910.
    # We want to enumerate these ranges so that clients can test whether an
    # IP is in a given zip code, e.g. `'20910' in result['zip']`. To enable
    # this, we convert US/PR zip codes to integers and expand the range and
    # then convert back to five-character zero-padded strings for the final
    # result.
    numeric_zip_codes = data.get('country_code') in {'US', 'PR'}

    integer_like_fields = INTEGER_FIELDS
    if numeric_zip_codes is True:
        integer_like_fields = INTEGER_FIELDS + ('zip',)

    for field in integer_like_fields:
        orig_value = data.get(field)

        if orig_value is None:
            continue

        if isinstance(orig_value, list):
            value = []

            for el in orig_value:
                # Some multiple value fields, such as 'zip', can contain
                # ranges, e.g.: 10001-10003.
                # Because a list with one or two items will always have a
                # 0th and -1th element, we can treat all values as ranges.
                el = el.split('-', 1)
                try:
                    start = int(el[0], 10)
                    end = int(el[-1], 10)
                except ValueError:
                    # Private IP addresses (and other yet to be discovered edge
                    # cases) will contain strings where we expect integers.
                    value.append(el)
                else:
                    value.append(range(start, end + 1))

            data[field] = list(itertools.chain.from_iterable(value))
        else:
            try:
                data[field] = int(orig_value, 10)
            except ValueError:
                # Private IP addresses (and other yet to be discovered edge
                # cases) will contain strings where we expect integers.
                pass

    for field in FLOAT_FIELDS:
        orig_value = data.get(field)

        if orig_value is None:
            continue

        try:
            data[field] = float(orig_value)
        except ValueError:
            # Private IP addresses (and other yet to be discovered edge cases)
            # will contain strings where we expect floats.
            pass

    for field in BOOLEAN_FIELDS:
        orig_value = data.get(field)

        if orig_value is None:
            continue

        if isinstance(orig_value, string_types):
            data[field] = orig_value.lower() == 't'

    # We converted US/PR zip codes to integers in order to expand the ranges
    # and now we convert them back to five-character zero-padded strings.
    if numeric_zip_codes is True and data.get('zip'):
        data['zip'] = ['%05d' % zc for zc in data.get('zip')]

    return data
