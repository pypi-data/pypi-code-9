import io

from nose.tools import eq_, raises

from ..reader import Reader, RowReadingError


def test_reader():
    f = io.StringIO(
        "header1\theader2\theader3\n" +
        "value11\tvalue12\t13\n" +
        "value21\tvalue22\t23\n" +
        "value31\tvalue32\t33\n" +
        "value41\tNULL\t43\n"
    )

    reader = Reader(f, types=[str, str, int])
    eq_(reader.headers, ["header1", "header2", "header3"])

    row = reader.next()
    eq_(row.values(), ["value11", "value12", 13])

    row = reader.next()
    eq_(row.values(), ["value21", "value22", 23])

    row = reader.next()
    eq_(row.values(), ["value31", "value32", 33])

    row = reader.next()
    eq_(row.values(), ["value41", None, 43])

@raises(RowReadingError)
def test_read_error():
    f = io.StringIO(
        "header1\theader2\theader3\n" +
        "value11\tvalue12\t13\n" +
        "value21\tvalue22\t23\n" +
        "value31\tvalue32\tnotanumber\n" + # Should error
        "value41\tNULL\t43\n"
    )

    reader = Reader(f, types=[str, str, int])

    [row for row in reader]

def test_handled_read_error():
    f = io.StringIO(
        "header1\theader2\theader3\n" +
        "value11\tvalue12\t13\n" +
        "value21\tvalue22\t23\n" +
        "notanumber\n" + # Should error
        "value41\tNULL\t43\n"
    )

    def handle_error(lineno, line, e):
        print("An error occurred while processing line {0}".format(line))
        print(repr(line))
        print(e)

    reader = Reader(f, types=[str, str, int], error_handler=handle_error)

    [row for row in reader]
