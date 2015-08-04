import json
import re

from docutils.core import publish_parts

from okapi.core.exceptions import InvalidHeaderException
from okapi.rst.writers.html import HTMLWriter


RE_HEADER = re.compile(
    r'^(?P<key>[^:]+): *(?P<value>.+)'
)
"""
Parses HTML headers in format ``key: value``.
"""


def publish(text, path=None):
    """
    Render RST string.

    :param text: RST text
    :type text: str

    :return: Rendered RST.
    """
    return publish_parts(text, writer=HTMLWriter(), source_path=path)


def parse_headers(lines):
    """
    Parses HTML headers in format ``key: value``.

    :param lines: List with headers strings.
    :type lines: list[str]

    :return: Dictionary with parsed (key, value).
    :rtype: dict[str, str]
    """
    headers = {}
    errors = []

    for l in lines:
        try:
            matched = RE_HEADER.match(l)
            headers[matched.group('key')] = matched.group('value')
        except AttributeError:
            errors.append('Cannot parse headers line `{}`'.format(l))

    if errors:
        raise InvalidHeaderException('\n'.join(errors))

    return headers


def format_json(o):
    """
    Converts object to JSON readable format.

    :param o: Object convertible to JSON
    :type o: dict | tuple | str

    :return: Formatted string
    :rtype: str
    """
    if not o:
        return
    return json.dumps(o, sort_keys=True, indent=2, separators=(',', ': '))
