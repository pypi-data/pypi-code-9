import re

from jinja2 import escape


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


def nl2br(value):
    value = value.replace(' ', '\u00A0')
    return u'\n\n'.join(
        p.replace('\n', '<br>\n')
        for p in _paragraph_re.split(escape(value))
    )


def status_code_class(status_code):
    if 200 <= status_code < 300:
        return 'success'
    elif 300 <= status_code < 400:
        return 'info'
    elif 400 <= status_code < 500:
        return 'warning'
    return 'danger'
