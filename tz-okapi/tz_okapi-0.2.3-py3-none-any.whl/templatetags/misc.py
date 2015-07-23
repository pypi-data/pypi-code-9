import re

from jinja2 import escape


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


def nl2br(value):
    value = value.replace(' ', '\u00A0')
    return u'\n\n'.join(
        p.replace('\n', '<br>\n')
        for p in _paragraph_re.split(escape(value))
    )
