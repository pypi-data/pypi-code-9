import io

from nose.tools import eq_, raises

from ..writer import Writer


def test_writer():

    rows = [
        ["Foo", 5, None],
        ["Bar", 10, "waffles"]
    ]
    expected = "Thing\tAmount\tNotes\n" + \
               "Foo\t5\tNULL\n" + \
               "Bar\t10\twaffles\n"

    f = io.StringIO()

    writer = Writer(f, headers=["Thing", "Amount", "Notes"])

    for row in rows:
        writer.write(row)

    eq_(f.getvalue(), expected)


def test_none_string():
    rows = [
        ["Foo", 5, None],
        ["Bar", 10, "waffles"]
    ]
    expected = "Thing\tAmount\tNotes\n" + \
               "Foo\t5\t\\N\n" + \
               "Bar\t10\twaffles\n"

    f = io.StringIO()

    writer = Writer(f, headers=["Thing", "Amount", "Notes"], none_string="\\N")

    for row in rows:
        writer.write(row)

    eq_(f.getvalue(), expected)
