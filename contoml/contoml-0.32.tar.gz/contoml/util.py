import math


def is_sequence_like(x):
    """
    Returns True if x exposes a sequence-like interface.
    """
    required_attrs = (
        '__len__',
        '__getitem__'
    )
    return all(hasattr(x, attr) for attr in required_attrs)


def is_dict_like(x):
    """
    Returns True if x exposes a dict-like interface.
    """
    required_attrs = (
        '__len__',
        '__getitem__',
        'keys',
        'values',
    )
    return all(hasattr(x, attr) for attr in required_attrs)


def join_with(iterable, separator):
    """
    Joins elements from iterable with separator and returns the produced sequence as a list.

    separator must be addable to a list.
    """
    inputs = list(iterable)
    b = []
    for i, element in enumerate(inputs):
        if isinstance(element, (list, tuple, set)):
            b += tuple(element)
        else:
            b += [element]
        if i < len(inputs)-1:
            b += separator
    return b


def chunkate_string(text, length):
    """
    Iterates over the given seq in chunks of at maximally the given length. Will never break a whole word.
    """
    iterator_index = 0

    def next_newline():
        try:
            return next(i for (i, c) in enumerate(text) if i > iterator_index and c == '\n')
        except StopIteration:
            return len(text)

    def next_breaker():
        try:
            return next(i for (i, c) in reversed(tuple(enumerate(text)))
                        if i >= iterator_index and
                        (i < iterator_index+length) and
                        c in (' ', '\t'))
        except StopIteration:
            return len(text)

    while iterator_index < len(text):
        next_chunk = text[iterator_index:min(next_newline(), next_breaker()+1)]
        iterator_index += len(next_chunk)
        yield next_chunk
