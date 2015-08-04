"""
A set of utility functions.
"""

import bisect
import operator
import random  # TODO Use cryptographic-friendly randomization
import re

__all__ = ["accumulate", "natural", "nonzero_natural",
           "random_weighted_choice", "extract_words", "GenerationError"]


def accumulate(iterable, func=operator.add):
    """
    Return a generator of accumulated values of iterable.

    :param iterable: the iterable of values;
    :param func:  a function taking an accumulated value and a value of
    iterable and returning the new accumulated value.
    :return: a generator of accumulated values of iterable with func.

    Copied from
    https://docs.python.org/3/library/itertools.html#itertools.accumulate
    """
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        total = func(total, element)
        yield total


def natural(value):
    """
    Return value as a positive integer.
    
    :param value: the value to cast;
    :return: value as a positive integer.
    :raises ValueError: if value does not represent a positive integer.
    """
    integer = int(value)
    if integer < 0:
        raise ValueError("'%s' is not a positive integer" % value)
    return integer


def nonzero_natural(value):
    """
    Return value as a strict positive integer.
    
    :param value: the value to cast;
    :return: value as a strict positive integer.
    :raises ValueError: if value does not represent a strict positive integer.
    """
    integer = int(value)
    if integer <= 0:
        raise ValueError("'%s' is not a strict positive integer" % value)
    return integer


def random_weighted_choice(choices):
    """
    Return a random key of choices, weighted by their value.

    :param choices: a dictionary of keys and positive integer pairs;
    :return: a random key of choices.
    """
    choices, weights = zip(*choices.items())
    cumdist = list(accumulate(weights))
    x = random.random() * cumdist[-1]
    element = bisect.bisect(cumdist, x)
    return choices[element]


def extract_words(lines):
    """
    Extract from the given iterable of lines the list of words.

    :param lines: an iterable of lines;
    :return: a generator of words of lines.
    """
    for line in lines:
        for word in re.findall(r"\w+", line):
            yield word


class GenerationError(Exception):
    """
    A problem occurred during random word generation.
    """
    pass
