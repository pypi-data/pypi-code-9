"""handy math and statistics routines"""

# std py3k stanza
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import Counter


class MathError(ValueError):
    '''general math error'''
    pass


def fequal(num1, num2, tolerance=0.000001):
    """compare float equality to a given tolerance"""
    return abs(num1 - num2) < tolerance


def is_even(num):
    '''return True if num(int) is even'''
    return num % 2 == 0


def is_odd(num):
    '''return True if num(int) is odd'''
    return num & 1


def mean(lst):
    """return the arithmetic mean of the list (lst) of numbers"""
    try:
        return sum(lst) / len(lst)
    except ZeroDivisionError:
        raise MathError('mean of an empty list is undefined')


def gmean(lst):
    '''return the geometric mean of the list of numbers'''
    size = len(lst)
    if size == 0:
        raise MathError('gmean of an empty list is undefined')
    accum = lst[0]
    for num in lst[1:]:
        accum *= num
    return accum**(1/size)


def hmean(lst):
    '''given a list of numbers, return the harmonic mean'''
    size = len(lst)
    if size == 0:
        raise MathError('hmean of an empty list is undefined')
    try:
        return size / sum([1/x for x in lst])
    except ZeroDivisionError:
        raise MathError('ZeroDivisionError')


def median(lst):
    '''return the median value from the list'''
    slst = sorted(lst)
    size = len(slst)
    if size == 0:
        raise MathError('median of an empty list is undefined')
    mid = size // 2
    if is_even(size):
        return mean(slst[mid-1:mid+1])
    else:
        return slst[mid]


def pvariance(lst):
    '''return the population variance for the list of numbers'''
    mu = mean([x for x in lst])
    return sum([(x-mu)**2 for x in lst])/len(lst)


def svariance(lst):
    '''return the sample population variance for the list of numbers'''
    xbar = mean([float(x) for x in lst])
    return sum([(x-xbar)**2 for x in lst])/(len(lst) - 1)


def pstddev(lst):
    """return the population standard deviation of the elements in the list"""
    return pvariance(lst)**.5


def sstddev(lst):
    """return the sample standard deviation of the elements in the list"""
    return svariance(lst)**.5


def mode(lst):
    '''return the mode (most common element value) from the list'''
    if not lst:
        raise MathError('mode of an empty list is undefined.')
    cntr = Counter(lst)
    # test for multi-modal
    cnts = cntr.most_common(2)
    if cnts[0][1] == cnts[1][1]:
        raise MathError('Mutiple Modes found')
    return cnts[0][0]


def ttest_independent(lst1, lst2):
    '''calc the ttest for two independent samples'''
    cnt1 = len(lst1)
    cnt2 = len(lst2)
    term1 = (((cnt1-1) * sstddev(lst1)**2) + ((cnt2-1) * sstddev(lst2)**2))
    term1 /= (cnt1+cnt2-2)
    term2 = (cnt1 + cnt2)/(cnt1*cnt2)
    return (mean(lst1) - mean(lst2))/(term1 * term2)**.5


def ttest_dependent(lst, lst_prime):
    '''calculate the ttest for two dependent samples. i.e. pre/post'''
    pass
