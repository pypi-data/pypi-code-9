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

    row = next(reader)
    eq_(row.values(), ["value11", "value12", 13])

    row = next(reader)
    eq_(row.values(), ["value21", "value22", 23])

    row = next(reader)
    eq_(row.values(), ["value31", "value32", 33])

    row = next(reader)
    eq_(row.values(), ["value41", None, 43])


def test_none_string():
    f = io.StringIO(
        "header1\theader2\theader3\n" +
        "value41\t\\N\t43\n"
    )

    reader = Reader(f, types=[str, str, int], none_string="\\N")
    eq_(reader.headers, ["header1", "header2", "header3"])

    row = next(reader)
    eq_(row.values(), ["value41", None, 43])


def test_no_headers():
    f = io.StringIO(
        "value11\tvalue12\t13\n" +
        "value21\tvalue22\t23\n"
    )

    reader = Reader(f, types=[str, str, int], headers=False)
    eq_(reader.headers, None)

    row = next(reader)
    eq_(row[0], "value11")
    eq_(row[1], "value12")
    eq_(row[2], 13)

    row = next(reader)
    eq_(row[0], "value21")
    eq_(row[1], "value22")
    eq_(row[2], 23)


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
