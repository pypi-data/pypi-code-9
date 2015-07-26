

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
