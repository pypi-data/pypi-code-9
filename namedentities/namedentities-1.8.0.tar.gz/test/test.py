
import six
from namedentities import *
from namedentities.core import (named_entities_codec, hex_entities_codec,
                                numeric_entities_codec,
                                numeric_entities_builtin)
import sys
import pytest


def _print(*args, **kwargs):
    """
    Python 2 and 3 compatible print function, similar to Python 3 arg handling.
    """
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    f   = kwargs.get('file', sys.stdout)
    parts.append(end)
    f.write(sep.join(parts))


def test_unicode():
    u = six.u('both em\u2014and')
    assert named_entities(u) == six.u("both em&mdash;and")


def test_numeric_entity():
    u = six.u('and&#x2013;dashes')
    assert named_entities(u) == six.u("and&ndash;dashes")
    assert hex_entities(u) == entities(u, 'hex')


def test_broken_entity():
    # if the entity is broken, it doesn't encode anything properly
    # so do-not-translate is the right approach
    u = six.u('and&#broke;it')
    assert named_entities(u) == u
    assert hex_entities(u) == u
    assert numeric_entities(u) == u
    assert unicode_entities(u) == u

    # similarly, if there really is no named entity, leave it be

    u = 'also &broken; too'
    assert hex_entities(u) == u
    

def test_broken_codecs():
    # ensure some trivial exception paths as not legitimate issues
    with pytest.raises(TypeError):
        numeric_entities_codec(4)
    with pytest.raises(TypeError):
        hex_entities_codec(4)
    with pytest.raises(TypeError):
        named_entities_codec(4)


def test_hex():

    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert hex_entities(u) == six.u("both em&#x2014;and&#x2013;dashes&#x2026;")


def test_entities():
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert hex_entities(u) == entities(u, 'hex')
    assert named_entities(u) == entities(u, 'named')
    assert numeric_entities(u) == entities(u, 'numeric')
    assert unicode_entities(u) == entities(u, 'unicode')
    assert u == entities(u, 'none')
    with pytest.raises(UnknownEntities):
        entities(u, 'bozo')


def test_unicode_and_numeric():
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert named_entities(u) == six.u("both em&mdash;and&ndash;dashes&hellip;")


def test_numeric_entities_builtin():
    # not exported, but let's test it anyway
    assert numeric_entities_builtin('this &mdash;') == 'this &#8212;'


def test_missing_named_entities():
    """
    Some great Unicode symbols don't have HTML entity names. What
    happens when they're encountered?
    """
    sm = six.u("\u2120")
    assert numeric_entities(sm) == '&#8480;'
    assert named_entities(sm) == '&#8480;'  # can't name-encode


def test_six_print_example(capsys):
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    six.print_(named_entities(u))
    out, err = capsys.readouterr()
    assert out.startswith("both em&mdash;and&ndash;dashes&hellip;")


def test_docs_example():
    u = six.u('both em\u2014and&#x2013;dashes&hellip;')
    assert named_entities(u)   == 'both em&mdash;and&ndash;dashes&hellip;'
    assert numeric_entities(u) == 'both em&#8212;and&#8211;dashes&#8230;'
    assert unescape(u)   == six.u('both em\u2014and\u2013dashes\u2026')


def test_encode_ampersands():
    assert encode_ampersands("this & that") == "this &amp; that"

    assert encode_ampersands("this &amp; that") == "this &amp; that"
    # ha! not fooled!
