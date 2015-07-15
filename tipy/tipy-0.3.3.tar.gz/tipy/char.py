#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Some variables and functions to help handling characters categories."""


from unicodedata import category


blankspaces = ' \f\n\c\r\t\v'
"""@var: A string containing every blankspaces characters."""

separators = '`~!@#$%^&*()_-+=\\|]}[{\";:/?.>,<†„“।॥ו–´’‘‚י0123456789ः'
"""@var: A string containing every separators characters."""


def first_word_char(string):
    """Return the index of the first word character in a string.

    @return:
        The index of the first word character in the string 'string' or -1 if
        the string contains no word character.
    @rtype: int
    """
    for i, ch in enumerate(string):
        if is_word_char(ch):
            return i
    return -1


def last_word_char(string):
    """Return the index of the last word character in a string.

    @return:
        The index of the last word character in the string 'string' or -1 if
        the string contains no word character.
    @rtype: int
    """
    result = first_word_char(string[::-1])
    if result == -1:
        return -1
    return len(string) - result - 1


def is_word_char(char):
    """Check if a character is a word character.

    @return:
        True or False weither the character 'char' is a word character, i.e. a
        printable non-ponctuation character.
    @rtype: bool
    """
    if category(char)[0] == "L":
        return True
    return False
