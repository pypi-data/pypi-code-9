# -*- coding: utf-8 -*-

from simplere import *
import re
import six
import pytest
import sys

_PY33ORGREATER = sys.version_info[:2] >= (3, 3)


class YesItIs(ValueError):
    pass


def test_memoization():

    assert Glob('a*') is Glob('a*')
    assert Glob("a*", "b*") is Glob("a*", "b*")


def test_Glob():
    assert "alpha" in Glob("a*")
    assert "beta" not in Glob("a*")

    assert Glob("a*").__contains__("alpha") == "a*"

    assert 'globtastic' in Glob('glob*')


def test_Glob_starargs():
    g = Glob("a*", "b*")
    assert "alpha" in g
    assert "beta" in g
    assert "gamma" not in g
    assert 4 not in g


def test_Glob_contains():
    assert Glob("a*").__contains__("alpha") == "a*"
    assert Glob("a*").contains("alpha") == "a*"

    g = Glob("a*", "b*")
    assert g.contains("andy") == "a*"
    assert g.contains("bubba") == "b*"


def test_InsensitiveGlob():
    g = InsensitiveGlob("b*")
    gg = InsensitiveGlob("B*")

    # some easy ASCII stuff
    assert "bubba" in g
    assert "bubba" in gg
    assert "Bubba" in g
    assert "Bubba" in gg
    assert "wubba" not in g
    assert "wubba" not in gg

    # now some (basic) Unicode foldign
    assert six.u("BUSSE") in g
    assert six.u("BU\u1E9EE") in g # LATIN CAPITAL LETTER SHARP S
    assert six.u("BU\u00DFE") in g # LATIN SMALL LETTER SHARP S

@pytest.mark.skipif(not _PY33ORGREATER, reason="Unicode is hard")
def test_InsensitiveGlob_harder():
    ug = InsensitiveGlob(six.u("BUSSE"))
    ugg = InsensitiveGlob(six.u("BU\u1E9EE"))  # LATIN CAPITAL LETTER SHARP S
    uggg = InsensitiveGlob(six.u("BU\u00DFE")) # LATIN SMALL LETTER SHARP S

    assert six.u("BUSSE") in ug
    assert six.u("BUSSE") in ugg
    assert six.u("BUSSE") in uggg

    assert six.u("BU\u1E9EE") in ug
    assert six.u("BU\u1E9EE") in ugg
    assert six.u("BU\u1E9EE") in uggg

    assert six.u("BU\u00DFE") in ug
    assert six.u("BU\u00DFE") in ugg
    assert six.u("BU\u00DFE") in uggg
