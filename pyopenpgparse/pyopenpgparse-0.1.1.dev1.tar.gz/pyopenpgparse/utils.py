#!/usr/boin/env python
"""
This module includes utility functions, used anywhere in the library.
"""
def get_int2(data, start):
    '''Pull two bytes from data at start and return as an integer.'''
    return (data[start] << 8) + data[start + 1]

def get_int4(data, start):
    '''Pull four bytes from data at start and return as an integer.'''
    return ((data[start] << 24) + (data[start + 1] << 16) +
                    (data[start + 2] << 8) + data[start + 3])

def get_int8(data, start):
    '''Pull eight bytes from data at start and return as an integer.'''
    return (get_int4(data, start) << 32) + get_int4(data, start + 4)
