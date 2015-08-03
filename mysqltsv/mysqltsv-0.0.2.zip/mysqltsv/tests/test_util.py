from nose.tools import eq_

from ..util import decode, encode, read_row


def test_encode():

    eq_(encode("foobar"), "foobar")
    eq_(encode(5), "5")
    eq_(encode(b"foobar"), "foobar")
    eq_(encode("foo\tbar"), "foo\\tbar")

def test_decode():

    eq_(decode("foobar"), "foobar")
    eq_(decode("5"), "5")
    eq_(decode("5", int), 5)
    eq_(decode(b"foobar"), "foobar")
    eq_(decode("foo\\tbar\\n"), "foo\tbar\n")

def test_encode_decode():

    input = "\t\nfoobar\t,derp"
    expected_encoded = "\\t\\nfoobar\\t,derp"

    eq_(encode(input), expected_encoded)

    eq_(decode(encode(input)), input)

def test_read_row():

    eq_(list(read_row("foo\tbar\tNULL")), ["foo", "bar", None])

    eq_(
        list(read_row("foo\t12\tNULL", types=[str, int, str])),
        ["foo", 12, None]
    )
