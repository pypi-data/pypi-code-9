
import collections

from . import _compat

__all__ = ['chunked',
           'overlapped',
           'grouped',
           'pluralized']

def chunked(iterable, size, rounded=True):
    return _windowed(iterable, size=size, step=size, rounded=rounded)

def overlapped(iterable):
    return _windowed(iterable, size=2, step=1)

def grouped(iterable):
    groups = collections.defaultdict(list)

    for groupkey, groupvalue in iterable:
        groups[groupkey].append(groupvalue)

    for groupkey, groupvalue in _compat.iteritems(groups):
        yield (groupkey, groupvalue)

def pluralized(obj):
    for item in obj if isinstance(obj, list) else [obj]:
        yield item

def _windowed(iterable, size, step=1, rounded=True):
    size = 0 if size is None else size
    step = 0 if step is None else step

    if step < 1 or size < 1:
        pass # Quickly yields nothing for this special case.

    elif size == 1 and step == 1:
        # A more efficient implementation for this particular special case.

        for item in iterable:
            yield (item,)
    else:
        # The general case.

        window = ()
        overshoot = 0
        for item in iterable:

            if overshoot < 0:
                overshoot += 1
            else:
                window += (item,)

            if len(window) == size:
                yield window

                # This prevents appending to the window when there are supposed to be gaps between the windows.
                overshoot = size - step
                if overshoot > 0:
                    overshoot = 0

                window = window[step:]

        if not rounded:
            while len(window):
                yield window
                window = window[step:]
