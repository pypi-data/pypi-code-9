'''
General utility functions used within the library.

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

from .defaults import FILTER_NAME_TO_UUID

def toutf8(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    elif isinstance(s, str):
        return s.decode('utf-8').encode('utf-8')
    else:
        raise TypeError("Object is neither 'str' nor 'unicode': {}".format(repr(s)))

def dict_of_lists_to_tuples(dict_of_lists):
    for key, value_list in dict_of_lists.iteritems():
        for value in value_list:
            yield key, value

def list_filters():
    '''Return a list of available filters' names.'''
    return FILTER_NAME_TO_UUID.keys()

def generate_poll_times(start, end, steps):
    '''
    Generate poll times from between start and end bounds.

    First yield 'steps' number of times evenly distributed between the bounds,
    afterwards yield end continuously.
    '''
    if start < 0 or end < 0:
        raise ValueError('start and end should be non-negative')
    start = float(start)
    end = float(end)
    if steps > 1:
        incr = (end - start) / (steps - 1)
        time = start
        for step in xrange(steps-1):
            yield time
            time += incr
    while True:
        yield end
