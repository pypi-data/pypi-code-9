# -*- coding: utf-8 -*-
"""Test suite for grep"""
from tempfile import NamedTemporaryFile
from functools import wraps
from StringIO import StringIO
from mock import patch
import unittest
import grep
import sys


def mock_stdin(func):
    """A decorator to mock stdin since I was having
    trouble with pytest and mock with stdin."""
    @wraps(func)
    def inner(*args, **kwargs):
        """The function returned as a substitute for the
        original."""
        _fake_in = StringIO(u"hello\nworld\nhello world")
        setattr(_fake_in, "name", "<stdin>")
        old_in = sys.stdin
        sys.stdin = _fake_in
        func(*args, **kwargs)
        sys.stdin = old_in
    return inner


def test_imports():
    """This tests that everything that should be importable is.
    `import grep` is missing as it was imported above (An error
    would have been thrown if it didn't work)."""
    from grep import parse_args
    from grep import main


class TestArgumentParser(unittest.TestCase):
    """A collection of tests for the arguments which parse_args
    should accept."""

    def test_pattern(self):
        """Test that pattern is the first positional argument."""
        sys.argv = ["", "pattern"]
        args = grep.parse_args()
        self.assertEqual(args.pattern, "pattern")

    def test_files(self):
        """Test that files can be provided or not and that
        a list is always what you get, even with the default
        to stdin"""
        # Test that parse_args throws error on non-existant files
        sys.argv = ["", "pattern", "file_1", "file_2", "file_3"]
        with self.assertRaises(SystemExit):
            args = grep.parse_args()

        # test that parse_args can use a real file
        _file = NamedTemporaryFile()
        sys.argv = ["", "pattern", _file.name]
        args = grep.parse_args()
        self.assertIn(_file.name, [x.name for x in args.files])
        self.assertEqual(len(args.files), 1)

        # test that parse_args defaults to stdin
        sys.argv = ["", "pattern"]
        args = grep.parse_args()
        self.assertIn(sys.stdin, args.files)
        self.assertEqual(len(args.files), 1)

    def test_ignore_case(self):
        """Test that -i and --ignore-case provide boolean
        arguments"""
        sys.argv = ["", "-i", "pattern"]
        args = grep.parse_args()
        self.assertTrue(args.ignore_case)

        sys.argv = ["", "--ignore-case", "pattern"]
        args = grep.parse_args()
        self.assertTrue(args.ignore_case)

        sys.argv = ["", "pattern"]
        args = grep.parse_args()
        self.assertFalse(args.ignore_case)

    def test_line_number(self):
        """Test that -n and --line-number privide boolean
        arguments"""
        sys.argv = ["", "-n", "pattern"]
        args = grep.parse_args()
        self.assertTrue(args.line_number)

        sys.argv = ["", "--line-number", "pattern"]
        args = grep.parse_args()
        self.assertTrue(args.line_number)

        sys.argv = ["", "pattern"]
        args = grep.parse_args()
        self.assertFalse(args.line_number)

    def test_with_filename(self):
        """Test that -H and --with-filename provide boolean
        arguments"""
        sys.argv = ["", "-H", "pattern"]
        args = grep.parse_args()
        self.assertTrue(args.with_filename)

        sys.argv = ["", "--with-filename", "pattern"]
        args = grep.parse_args()
        self.assertTrue(args.with_filename)

        sys.argv = ["", "pattern"]
        args = grep.parse_args()
        self.assertFalse(args.with_filename)


class TestMain(unittest.TestCase):
    """Test the main functionality of the program"""
    @mock_stdin
    def test_find_word(self):
        """Basic test that grep.main can find a word based
        on pattern"""
        sys.argv = ["", "hello"]
        args = grep.parse_args()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            grep.main(args)
            fake_out.seek(0)
            self.assertEqual("hello\nhello world\n", fake_out.read())

    @mock_stdin
    def test_ignore_case(self):
        """Test that if -i or --ignore-case are provided, then
        case is actually ignored"""
        # test -i
        sys.argv = ["", "-i", "HELLO"]
        args = grep.parse_args()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            grep.main(args)
            fake_out.seek(0)
            self.assertEqual("hello\nhello world\n", fake_out.read())

        # test --ignore-case
        sys.stdin.seek(0)
        sys.argv = ["", "--ignore-case", "HELLO"]
        args = grep.parse_args()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            grep.main(args)
            fake_out.seek(0)
            self.assertEqual("hello\nhello world\n", fake_out.read())

    @mock_stdin
    def test_line_number(self):
        """Test that if -n or --line-number are provided, then
        line-numbers are actually output"""
        # test -n
        sys.argv = ["", "-n", "hello"]
        args = grep.parse_args()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            grep.main(args)
            fake_out.seek(0)
            self.assertEqual("0:hello\n2:hello world\n", fake_out.read())

        # test --line-numbers
        sys.stdin.seek(0)
        sys.argv = ["", "--line-number", "hello"]
        args = grep.parse_args()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            grep.main(args)
            fake_out.seek(0)
            self.assertEqual("0:hello\n2:hello world\n", fake_out.read())

    @mock_stdin
    def test_with_filename(self):
        """Test that if -H or --with-filename are provided, then
        the filename is actually output"""
        # test -H
        sys.argv = ["", "-H", "hello"]
        args = grep.parse_args()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            grep.main(args)
            fake_out.seek(0)
            self.assertEqual(
                "<stdin>:hello\n<stdin>:hello world\n", fake_out.read())

        # test --with-filename
        sys.stdin.seek(0)
        sys.argv = ["", "--with-filename", "hello"]
        args = grep.parse_args()
        with patch("sys.stdout", new=StringIO()) as fake_out:
            grep.main(args)
            fake_out.seek(0)
            self.assertEqual(
                "<stdin>:hello\n<stdin>:hello world\n", fake_out.read())
