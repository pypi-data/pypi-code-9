# -*- encoding:UTF-8
import os
import datetime
import unittest

from pyf.splitter import (
    tokenize, get_splitter, chain_splitters,
    get_input_item_flow, get_input_item_str_flow,
    EndOfFileError, InputSplitterError,
    input_item_separator,
)

from pyjon.utils import get_secure_filename
from nose.tools import raises


class TestItem(object):
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __repr__(self):
        return "<TestItem(field1='%s', field2='%s')>" % (
            self.field1, self.field2
        )

    def __eq__(self, other):
        if isinstance(other, TestItem):
            return (self.field1 == other.field1) and (
                self.field2 == other.field2
            )

        else:
            return False


def input_datafile(input_bytes):
    """A helper to write data in a file and use it as input.

    :param input_bytes: a bytes stream to serialize to the file
    :type input_bytes: in python 2.x use string in python 3.x use bytes
    """
    filename = get_secure_filename()

    f = open(filename, 'w+b')
    f.write(input_bytes)
    f.flush()
    f.seek(0)

    return f

class TestTokenize(unittest.TestCase):

    def test_tokenize(self):
        """Test the tokenize function in some edge cases."""
        result = tokenize(b'', separator=input_item_separator)
        assert result == ([], b''), (
            "Tokenize returned (%s, '%s') "
            "instead of ([], b'')" % (result[0], result[1])
        )

        result = tokenize(input_item_separator, separator=input_item_separator)
        assert result == ([b''], b''), (
            "Tokenize returned (%s, '%s') "
            "instead of ([b''], b'')" % (result[0], result[1])
        )

        result = tokenize(
            b's' + input_item_separator, separator=input_item_separator
        )
        assert result == ([b's'], b''), (
            "Tokenize returned (%s, '%s') "
            "instead of ([b's'], b'')" % (result[0], result[1])
        )

        result = tokenize(b's', separator=input_item_separator)
        assert result == ([], b's'), (
            "Tokenize returned (%s, '%s') "
            "instead of ([], b's')" % (result[0], result[1])
        )

        result = tokenize(
            input_item_separator + b's', separator=input_item_separator
        )
        assert result == ([b''], b's'), (
            "Tokenize returned (%s, '%s') "
            "instead of ([b''], b's')" % (result[0], result[1])
        )


def test_read_file_success():
    """Test the get_input_item_str_flow function with various inputs."""
    # only one element
    sep = input_item_separator
    data = b'aaaaaaaaaa' + sep
    f = input_datafile(data)
    count = 0
    for _ in get_input_item_str_flow(f, chunk_size=1):
        count += 1
    f.close()

    assert count == 1, "The parser yielded %s elements instead of 1" % count

    # various elements with "weird chars"
    data = [b's', b'', b'\aava', b'\x11\x12\x12ava', b'agfdaaaaaaa']
    f = input_datafile(sep.join(data) + sep)
    count = 0
    for element in get_input_item_str_flow(f, chunk_size=1):
        assert element == data[count], (
            "The parser yielded %s instead of %s" % (element, data[count])
        )
        count += 1
    f.close()

    assert count == 5, "The parser yielded %s elements instead of 5" % count

    # various elements with "weird chars" starting by a separator
    data = [b'', b's', b'', b'\aava', b'\x11\x12\x12ava', b'agfdaaaaaaa']
    f = input_datafile(sep.join(data) + sep)
    count = 0
    for element in get_input_item_str_flow(f, chunk_size=1):
        assert element == data[count], (
            "The parser yielded %s instead of %s" % (element, data[count])
        )
        count += 1
    f.close()

    assert count == 6, "The parser yielded %s elements instead of 6" % count


@raises(EndOfFileError)
def test_read_file_failed():
    """Test the get_input_item_str_flow function with an input leading
    to an error.
    """
    sep = input_item_separator
    # various elements with "weird chars" and no separator at the end
    data = [b's', b'', b'\aava', b'\x11\x12\x12ava', b'agfdaaaaaaa']
    f = input_datafile(sep.join(data))
    for count, element in enumerate(get_input_item_str_flow(f, chunk_size=1)):
        assert element == data[count], (
            "The parser yielded %s instead of %s" % (element, data[count])
        )


class TestSimplerSplitter(unittest.TestCase):
    def tearDown(self):
        # cleanup the mess
        for filename in self.splitter.bucket_filenames:
            os.unlink(filename)

    def test_simple_splitter_push(self):
        """Test the simple splitter by pushing items manually."""
        splitter = get_splitter(max_items=2)
        self.splitter = splitter
        for i in range(0, 10):
            o = TestItem('ref1', 'value%s' % i)
            _ = splitter.push(o)

        result = splitter.finalize()
        assert len(result) == 5


    def test_simple_splitter_empty_max(self):
        """Test the simple splitter in various scenarios."""
        # empty input with no max_items
        input_items = list()
        self.splitter =  get_splitter(input_items, 0)
        result = self.splitter.split()
        assert len(result) == 0, (
            "The splitter returned %s files instead of none" % len(result)
        )

    def test_simple_splitter_emtpy_max(self):
        input_items = list()

        # empty input with max_items
        self.splitter = get_splitter(input_items, 1)
        result = self.splitter.split()
        assert len(result) == 0, (
            "The splitter returned %s files instead of none" % len(result)
        )

    def test_simple_splitter_one_nomax(self):
        input_items = list()

        # only one item with no max_items
        o = TestItem('ref0', 'value0')
        input_items.append(o)

        self.splitter = get_splitter(input_items, 0)
        result = self.splitter.split()
        assert len(result) == 1, (
            "The splitter returned %s files instead of 1" % len(result)
        )

        count = 0
        f = open(result[0], 'rb')
        for item in get_input_item_flow(f):
            assert item == input_items[count], (
                "[File %s][Item %s] Got %s, %s instead of %s, %s" % (
                    f.name, count,
                    item, type(item),
                    input_items[count], type(input_items[count]),
                )
            )
        f.close()

    def test_simple_splitter_one_max1(self):
        input_items = list()
        o = TestItem('ref0', 'value0')
        input_items.append(o)

        # only one item with max_items = 1
        self.splitter = get_splitter(input_items, 1)
        result = self.splitter.split()
        assert len(result) == 1, (
            "The splitter returned %s files instead of 1" % len(result)
        )

        count = 0
        f = open(result[0], 'rb')
        for item in get_input_item_flow(f):
            assert item == input_items[count], (
                "[File %s][Item %s] Got %s instead of %s" % (
                    f.name, count, item, input_items[count]
                )
            )
        f.close()

    def test_simple_splitter_one_maxmore(self):
        # only one item with max_items > 1
        input_items = list()
        o = TestItem('ref0', 'value0')
        input_items.append(o)

        self.splitter = get_splitter(input_items, 10)
        result = self.splitter.split()
        assert len(result) == 1, (
            "The splitter returned %s files instead of 1" % len(result)
        )

        count = 0
        f = open(result[0], 'rb')
        for item in get_input_item_flow(f):
            assert item == input_items[count], (
                "[File %s][Item %s] Got %s instead of %s" % (
                    f.name, count, item, input_items[count]
                )
            )
        f.close()

    def test_simple_splitter_eleven_maxmore(self):
        # only one item with max_items > 1
        input_items = list()
        o = TestItem('ref0', 'value0')
        input_items.append(o)
        # list of items with no max_items
        input_items.extend(
            [TestItem('ref1', 'value%s' % i) for i in range(1, 10)]
        )

        self.splitter = get_splitter(input_items, 0)
        result = self.splitter.split()
        assert len(result) == 1, (
            "The splitter returned %s files instead of 1" % len(result)
        )

        count = 0
        for filename in result:
            f = open(filename, 'rb')
            for item in get_input_item_flow(f):
                assert item == input_items[count], (
                    "[File %s][Item %s] Got %s instead of %s" % (
                        f.name, count, item, input_items[count]
                    )
                )
                count += 1
            f.close()
        assert count == len(input_items), (
            "We got %s items after splitting, instead of the %s we had before" % (
                count, len(input_items)
            )
        )

    def test_simple_splitter_eleven_max3(self):
        # only one item with max_items > 1
        input_items = list()
        o = TestItem('ref0', 'value0')
        input_items.append(o)
        input_items.extend(
            [TestItem('ref1', 'value%s' % i) for i in range(1, 10)]
        )

        # list of items with max_items < nb items
        self.splitter = get_splitter(input_items, 3)
        result = self.splitter.split()
        assert len(result) == 4, (
            "The splitter returned %s files instead of 4" % len(result)
        )

        count = 0
        for filename in result:
            f = open(filename, 'rb')
            for item in get_input_item_flow(f):
                assert item == input_items[count], (
                    "[File %s][Item %s] Got %s instead of %s" % (
                        f.name, count, item, input_items[count])
                )
                count += 1
            f.close()
        assert count == len(input_items), (
            "We got %s items after splitting, instead of the %s we had before" % (
                count, len(input_items))
        )

    def test_simple_splitter_ten_max10(self):
        input_items = list()
        input_items.extend(
            [TestItem('ref1', 'value%s' % i) for i in range(0, 10)]
        )
        # list of items with max_items = nb items
        self.splitter = get_splitter(input_items, 10)
        result = self.splitter.split()
        assert len(result) == 1, (
            "The splitter returned %s files instead of 1" % len(result)
        )

        count = 0
        for filename in result:
            f = open(filename, 'rb')
            for item in get_input_item_flow(f):
                assert item == input_items[count], (
                    "[File %s][Item %s] Got %s instead of %s" % (
                        f.name, count, item, input_items[count])
                )
                count += 1
            f.close()
        assert count == len(input_items), (
            "We got %s items after splitting, instead of the %s we had before" % (
                count, len(input_items)
            )
        )

    def test_simple_splitter_eleven_max100(self):
        input_items = list()
        o = TestItem('ref0', 'value0')
        input_items.append(o)
        input_items.extend(
            [TestItem('ref1', 'value%s' % i) for i in range(1, 10)]
        )
        # list of items with max_items > nb items
        self.splitter = get_splitter(input_items, 100)
        result = self.splitter.split()
        assert len(result) == 1, (
            "The splitter returned %s files instead of 1" % len(result)
        )

        count = 0
        for filename in result:
            f = open(filename, 'rb')
            for item in get_input_item_flow(f):
                assert item == input_items[count], (
                    "[File %s][Item %s] Got %s instead of %s" % (
                        f.name, count, item, input_items[count]
                    )
                )
                count += 1
            f.close()
        assert count == len(input_items), (
            "We got %s items after splitting, instead of the %s we had before" % (
                count, len(input_items)
            )
        )


def test_splitter_attr():
    """Test splitting by attribute in various scenarios."""
    split_attribute = 'field1'

    # empty input with no max_items
    input_items = list()
    result = get_splitter(input_items, 0, split_attribute).split()
    assert len(result) == 0, (
        "The splitter returned %s files instead of none" % len(result)
    )

    # empty input with max_items
    result = get_splitter(input_items, 1, split_attribute).split()
    assert len(result) == 0, (
        "The splitter returned %s files instead of none" % len(result)
    )

    # only one item with no max_items
    input_items.append(TestItem('ref0', 'value0'))

    result = get_splitter(input_items, 0, split_attribute).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item == input_items[count], (
            "Got %s instead of %s" % (
                input_items[count], item
            )
        )
        count += 1
    f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # only one item with max_items = 1
    result = get_splitter(input_items, 1, split_attribute).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item == input_items[count], (
            "Got %s instead of %s" % (input_items[count], item)
        )
        count += 1
    f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # only one item with max_items > 1
    result = get_splitter(input_items, 10, split_attribute).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item == input_items[count], (
            "Got %s instead of %s" % (input_items[count], item)
        )
        count += 1
    f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with no max_items
    input_items.append(TestItem('ref0', 'value1'))
    input_items.extend([TestItem('ref1', 'value%s' % i) for i in range(3)])

    result = get_splitter(input_items, 0, split_attribute).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    already_seen = list()
    for filename in result:
        ref_values = set()
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            ref_value = getattr(item, split_attribute)
            ref_values.add(ref_value)
            assert ref_value not in already_seen, (
                "The value %s should have been in a previous file" % (
                    ref_value
                )
            )
            count += 1
        f.close()
        already_seen.extend(ref_values)
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with max_items < nb items
    result = get_splitter(input_items, 3, split_attribute).split()
    assert len(result) == 2, (
        "The splitter returned %s files instead of 2" % len(result)
    )

    count = 0
    already_seen = list()
    for filename in result:
        ref_values = set()
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            ref_value = getattr(item, split_attribute)
            ref_values.add(ref_value)
            assert ref_value not in already_seen, (
                "The value %s should have been in a previous file" % (
                    ref_value
                )
            )
            count += 1
        f.close()
        already_seen.extend(ref_values)
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with max_items = nb items
    result = get_splitter(input_items, 5, split_attribute).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    already_seen = list()
    for filename in result:
        ref_values = set()
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            ref_value = getattr(item, split_attribute)
            ref_values.add(ref_value)
            assert ref_value not in already_seen, (
                "The value %s should have been in a previous file" % (
                    ref_value
                )
            )
            count += 1
        f.close()
        already_seen.extend(ref_values)
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with max_items > nb items
    result = get_splitter(input_items, 10, split_attribute).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    already_seen = list()
    for filename in result:
        ref_values = set()
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            ref_value = getattr(item, split_attribute)
            ref_values.add(ref_value)
            assert ref_value not in already_seen, (
                "The value %s should have been in a previous file" % (
                    ref_value
                )
            )
            count += 1
        f.close()
        already_seen.extend(ref_values)
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )


@raises(InputSplitterError)
def test_splitter_attr_fail_max():
    """Try splitting by attribute with max_items too low."""
    split_attribute = 'field1'

    input_items = list()
    input_items.extend([TestItem('ref0', 'value%s' % i) for i in range(10)])
    input_items.extend([TestItem('ref1', 'value%s' % i) for i in range(5)])

    _ = get_splitter(input_items, 5, split_attribute).split()


@raises(InputSplitterError)
def test_splitter_attr_fail_attr():
    """Try splitting by attribute with unexisting split_attribute."""
    split_attribute = 'foobar'

    input_items = list()
    input_items.extend([TestItem('ref0', 'value%s' % i) for i in range(10)])
    input_items.extend([TestItem('ref1', 'value%s' % i) for i in range(5)])

    _ = get_splitter(input_items, 0, split_attribute).split()


def test_splitter_force_attr():
    """Test splitting by attribute (forcing split) in various scenarios."""
    split_attribute = 'field1'

    # empty input with no max_items
    input_items = list()
    result = get_splitter(
        input_items, 0, split_attribute, force_split=True
    ).split()
    assert len(result) == 0, (
        "The splitter returned %s files instead of none" % len(result)
    )

    # empty input with max_items
    result = get_splitter(
        input_items, 1, split_attribute, force_split=True
    ).split()
    assert len(result) == 0, (
        "The splitter returned %s files instead of none" % len(result)
    )

    # only one item with no max_items
    input_items.append(TestItem('ref0', 'value0'))

    result = get_splitter(
        input_items, 0, split_attribute, force_split=True
    ).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item == input_items[count], (
            "Got %s instead of %s" % (
                input_items[count], item
            )
        )
        count += 1
    f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # only one item with max_items = 1
    result = get_splitter(
        input_items, 1, split_attribute, force_split=True
    ).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item == input_items[count], (
            "Got %s instead of %s" % (
                input_items[count], item
            )
        )
        count += 1
    f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # only one item with max_items > 1
    result = get_splitter(
        input_items, 10, split_attribute, force_split=True
    ).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item == input_items[count], (
            "Got %s instead of %s" % (
                item, input_items[count]
            )
        )
        count += 1
    f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with no max_items
    input_items.append(TestItem('ref0', 'value1'))
    input_items.extend([TestItem('ref1', 'value%s' % i) for i in range(3)])

    result = get_splitter(
        input_items, 0, split_attribute, force_split=True
    ).split()
    assert len(result) == 2, (
        "The splitter returned %s files instead of 2" % len(result)
    )

    count = 0
    for filename in result:
        bucket_value = None
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute "
                "in a file of items with %s" % (
                    value, bucket_value
                )
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with max_items < nb items
    result = get_splitter(
        input_items, 3, split_attribute, force_split=True
    ).split()
    assert len(result) == 2, (
        "The splitter returned %s files instead of 2" % len(result)
    )

    count = 0
    for filename in result:
        bucket_value = None
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute "
                "in a file of items with %s" % (value, bucket_value)
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with max_items = nb items
    result = get_splitter(
        input_items, 5, split_attribute, force_split=True
    ).split()
    assert len(result) == 2, (
        "The splitter returned %s files instead of 2" % len(result)
    )

    count = 0
    for filename in result:
        bucket_value = None
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute "
                "in a file of items with %s" % (value, bucket_value)
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the %s we had before" % (
            count, len(input_items)
        )
    )

    # list of items with max_items > nb items
    result = get_splitter(
        input_items, 10, split_attribute, force_split=True
    ).split()
    assert len(result) == 2, (
        "The splitter returned %s files instead of 2" % len(result)
    )

    count = 0
    for filename in result:
        bucket_value = None
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute "
                "in a file of items with %s" % (value, bucket_value)
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )


@raises(InputSplitterError)
def test_splitter_force_attr_fail_max():
    """Try splitting by attribute (forcing split) with max_items too low."""
    split_attribute = 'field1'

    input_items = list()
    input_items.extend([TestItem('ref0', 'value%s' % i) for i in range(10)])
    input_items.extend([TestItem('ref1', 'value%s' % i) for i in range(5)])

    _ = get_splitter(
        input_items, 5, split_attribute, force_split=True
    ).split()


@raises(InputSplitterError)
def test_splitter_force_attr_fail_attr():
    """Try splitting by attribute (forcing split)
    with unexisting split_attribute.
    """
    split_attribute = 'foobar'

    input_items = list()
    input_items.extend([TestItem('ref0', 'value%s' % i) for i in range(10)])
    input_items.extend([TestItem('ref1', 'value%s' % i) for i in range(5)])

    _ = get_splitter(input_items, 0, split_attribute).split()


def test_splitter_datetime():
    """test that structures containing datetime instances can be pushed in"""

    elements = [
        [
            '1',
            datetime.datetime(2004, 1, 22, 10, 0, 0),
            datetime.date(2010, 12, 24),
        ],
        [
            '1',
            datetime.datetime(2005, 2, 23, 11, 27, 32),
            datetime.date(2015, 12, 24),
        ],
        [
            '1',
            datetime.datetime(2014, 8, 22, 9, 54, 0),
            datetime.date(2001, 11, 6),
        ],
    ]

    fnames = get_splitter(elements, 0).split()
    for fname in fnames:
        f = open(fname, 'rb')
        flow = get_input_item_flow(f)
        for index, item in enumerate(flow):
            assert item == elements[index], (
                "Expected: '%s' got '%s'" % (item, elements[index])
            )


def test_splitter_unicode():
    """Test that unicode attributes are preserved after splitting."""
    max_items = 2
    unicode_field = u'$Â£Ã¸'
    split_attribute = 'field1'

    input_items = list()
    o = TestItem('ref1', unicode_field)
    input_items.append(o)

    # test the simple splitter
    result = get_splitter(input_items, max_items).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item.field2 == unicode_field, (
            "Simple splitter didn't preserve unicode value: "
            "got %s instead of %s" % (item.field2, unicode_field)
        )
    f.close()

    # test the splitter by attribute
    result = get_splitter(input_items, 2, split_attribute).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item.field2 == unicode_field, (
            "Splitter by attribute didn't preserve unicode value: "
            "got %s instead of %s" % (item.field2, unicode_field)
        )
    f.close()

    # test the splitter by attribute, forcing it to split
    result = get_splitter(
        input_items, 2, split_attribute, force_split=True
    ).split()
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    f = open(result[0], 'rb')
    for item in get_input_item_flow(f):
        assert item.field2 == unicode_field, (
            "Splitter by attribute (forcing to split) didn't "
            "preserve unicode value: got %s instead of %s" % (
                item.field2, unicode_field)
        )
    f.close()


def test_chaining_splitters_single():
    """Make sure that chaining only one splitter doesn't
    change the behavior.
    """
    split_attribute = 'field1'

    input_items = list()
    for i in range(1, 11):
        input_items.append(TestItem('ref%s' % (i % 5), 'value%s' % (i % 3)))

    # simple splitter without max_items
    params_splitters = [{}]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 1, (
        "The splitter returned "
        "%s files instead of 1" % len(result)
    )

    count = 0
    for filename in result:
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            assert item == input_items[count], (
                "[File %s][Item %s] Got %s instead of %s" % (
                    f.name, count, item, input_items[count]
                )
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )

    # simple splitter with max_items < nb items
    params_splitters = [{'max_items': 4}]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 3, (
        "The splitter returned %s files instead of 3" % len(result)
    )

    count = 0
    for filename in result:
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            assert item == input_items[count], (
                "[File %s][Item %s] Got %s instead of %s" % (
                    f.name, count, item, input_items[count]
                )
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )

    # split by attribute without max_items
    params_splitters = [{'split_attribute': split_attribute}]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 1, (
        "The splitter returned %s files instead of 1" % len(result)
    )

    count = 0
    already_seen = list()
    for filename in result:
        ref_values = set()
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            ref_value = getattr(item, split_attribute)
            ref_values.add(ref_value)
            assert ref_value not in already_seen, (
                "The value %s should have been in "
                "a previous file" % ref_value
            )
            count += 1
        f.close()
        already_seen.extend(ref_values)
    assert count == len(input_items), (
        "We got %s items after splitting, "
        "instead of the %s we had before" % (count, len(input_items))
    )

    # split by attribute with max_items < nb items
    params_splitters = [{'max_items': 8, 'split_attribute': split_attribute}]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 2, (
        "The splitter returned %s files instead of 2" % len(result)
    )

    count = 0
    already_seen = list()
    for filename in result:
        ref_values = set()
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            ref_value = getattr(item, split_attribute)
            ref_values.add(ref_value)
            assert ref_value not in already_seen, (
                "The value %s should have been "
                "in a previous file" % ref_value
            )
            count += 1
        f.close()
        already_seen.extend(ref_values)
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )

    # split by attribute forcing split without max_items
    params_splitters = [
        {'split_attribute': split_attribute, 'force_split': True}
    ]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 5, (
        "The splitter returned %s files instead of 5" % len(result)
    )

    count = 0
    for filename in result:
        bucket_value = None
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute "
                "in a file of items with %s" % (value, bucket_value)
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )

    # split by attribute forcing split with max_items < nb items
    params_splitters = [
        {
            'max_items': 6,
            'split_attribute': split_attribute,
            'force_split': True
        }
    ]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 5, (
        "The splitter returned %s files instead of 5" % len(result)
    )

    count = 0
    for filename in result:
        bucket_value = None
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute "
                "in a file of items with %s" % (value, bucket_value)
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )


def test_chaining_splitters():
    """Test chaining different splitters."""
    first_split_attribute = 'field1'
    second_split_attribute = 'field2'

    input_items = list()
    for i in range(1, 21):
        input_items.append(
            TestItem('ref%s' % (i % 5), 'value%s' % (i % 3))
        )

    # chain two splitters without max_items
    # the first one won't do anything, so this is strictly
    # equivalent to having only the second one
    params_splitters = [
        {'split_attribute': first_split_attribute},
        {'split_attribute': second_split_attribute, 'force_split': True},
    ]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 3, (
        "The splitter returned %s files instead of 3" % len(result)
    )

    count = 0
    for filename in result:
        bucket_value = None
        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, second_split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute "
                "in a file of items with %s" % (value, bucket_value)
            )
            count += 1
        f.close()
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )

    # chain two splitters with first max_items < nb items
    params_splitters = [
        {'max_items': 8, 'split_attribute': first_split_attribute},
        {'split_attribute': second_split_attribute, 'force_split': True}
    ]
    result = chain_splitters(input_items, params_splitters)
    assert len(result) == 9, (
        "The splitter returned %s files instead of 9" % len(result)
    )

    count = 0
    already_seen = list()
    for filename in result:
        bucket_value = None
        ref_values = set()

        f = open(filename, 'rb')
        for item in get_input_item_flow(f):
            value = getattr(item, second_split_attribute)
            if not bucket_value:
                bucket_value = value
            assert value == bucket_value, (
                "We got an item with %s for its split_attribute in a "
                "file of items with %s" % (value, bucket_value)
            )

            ref_value = (getattr(item, first_split_attribute), value)
            ref_values.add(ref_value)
            assert ref_value not in already_seen, (
                "The value %s should have been in a previous file" % (
                    ref_value,
                )
            )

            count += 1
        f.close()
        already_seen.extend(ref_values)
    assert count == len(input_items), (
        "We got %s items after splitting, instead of the "
        "%s we had before" % (count, len(input_items))
    )
