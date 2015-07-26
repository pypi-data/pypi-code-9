import re
from datetime import datetime
import pytz
import strict_rfc3339
from contoml import tokens
from contoml.tokens import TYPE_BOOLEAN, TYPE_INTEGER, TYPE_FLOAT, TYPE_DATE, \
    TYPE_MULTILINE_STRING, TYPE_BARE_STRING, TYPE_MULTILINE_LITERAL_STRING, TYPE_LITERAL_STRING, \
    TYPE_STRING
import codecs
import six


def deserialize(token):
    """
    Deserializes the value of a single tokens.Token instance based on its type.
    """
    
    if token.type == TYPE_BOOLEAN:
        return _to_boolean(token)
    elif token.type == TYPE_INTEGER:
        return _to_int(token)
    elif token.type == TYPE_FLOAT:
        return _to_float(token)
    elif token.type == TYPE_DATE:
        return _to_date(token)
    elif token.type in (TYPE_STRING, TYPE_MULTILINE_STRING, TYPE_BARE_STRING,
                        TYPE_LITERAL_STRING, TYPE_MULTILINE_LITERAL_STRING):
        return _to_string(token)
    else:
        raise Exception('This should never happen!')


def _unescape_str(unescaped):
    if six.PY2:
        return unescaped.decode('string-escape').decode('unicode-escape')
    else:
        return codecs.decode(unescaped, 'unicode-escape')


def _to_string(token):
    if token.type == tokens.TYPE_BARE_STRING:
        return token.source_substring

    elif token.type == tokens.TYPE_STRING:
        escaped = token.source_substring[1:-1]
        return _unescape_str(escaped)

    elif token.type == tokens.TYPE_MULTILINE_STRING:
        escaped = token.source_substring[3:-3]
        if escaped[0] == '\n':
            escaped = escaped[1:]

        # Remove all occurrences of a slash-newline-one-or-more-whitespace patterns
        escaped = re.sub('\\\\\n\\s*', repl='', string=escaped, flags=re.DOTALL)
        return _unescape_str(escaped)

    elif token.type == tokens.TYPE_LITERAL_STRING:
        return token.source_substring[1:-1]

    elif token.type == tokens.TYPE_MULTILINE_LITERAL_STRING:
        text = token.source_substring[3:-3]
        if text[0] == '\n':
            text = text[1:]
        return text

    raise RuntimeError('Control should never reach here.')


def _to_int(token):
    return int(token.source_substring.replace('_', ''))

def _to_float(token):
    assert token.type == tokens.TYPE_FLOAT
    string = token.source_substring.replace('_', '')
    return float(string)

def _to_boolean(token):
    return token.source_substring == 'true'

def _to_date(token):
    return datetime.fromtimestamp(strict_rfc3339.rfc3339_to_timestamp(token.source_substring), tz=pytz.utc)
