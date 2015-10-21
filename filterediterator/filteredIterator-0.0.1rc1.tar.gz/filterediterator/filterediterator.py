#!/usr/bin/env python
"""
# FilteredIterator : Implementation of FilteredIterator.py

Summary : 
    Build a Iterator class which can be post filtered - similarly to Django
Use Case : 
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I <Boolean statement>
    ....
"""
import collections

__version__ = "0.0.1rc1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '21 Oct 2015'


class FilteredIterator(object):
    """Filtered Generator"""

    def __init__(self, source):
        self._iterator_expr = None
        self._filters = []

        if not isinstance(source, (collections.Iterator, collections.Iterable)):
            raise TypeError("Source must be an Iterable or Iterator")

        self._iterator_expr = source if isinstance(source, collections.Iterator) else iter(source)
        self._debug = False

    def __iter__(self):
        return self

    def next(self):
        accept = [False]

        while not all(accept):
            val = self._iterator_expr.next()
            accept = [True]  # Ensure that if there are no filters this will pass
            fi = 0
            while fi < len(self._filters):
                ftype, pred = self._filters[fi]

                # Only accept the value if the predicate is true
                if ftype == "filter":
                    accept.append(pred(val))
                    fi += 1
                    continue

                # Only accept the value if the predicate is true - and stop if not
                if ftype == "takewhile":
                    if pred(val):
                        accept.append(True)
                    else:
                        raise StopIteration

                    fi += 1
                    continue

                # Reject values until the pred is true, and then accept rest (even if the pred becomes false again).
                if ftype == "dropwhile":
                    if pred(val):
                        accept.append(False)
                        fi += 1
                    else:
                        accept.append(True)
                        del self._filters[fi]  # Drop pred to ensure that the pred isn't applied again.
                    continue

        return val

    def __addfilter(self, ftype, pred):
        if not isinstance(pred, collections.Callable):
            raise TypeError("predicate argument must be callable")

        self._filters.append((ftype, pred))
        return self

    def filter(self, pred=lambda x: x):
        """Includes items where the predicate callable returns true.
            :param pred : A boolean predicate for the data item in question (a callable to which the item key is passed)
        """
        return self.__addfilter("filter", pred)

    def takewhile(self, pred=lambda x: x):
        """Make an iterator that returns elements from the iterable as long as the predicate is false - and then stop"""
        return self.__addfilter("takewhile", pred)

    def dropwhile(self, pred=lambda x: x):
        """Make an iterator that ignores elements from the iterable as long as the predicate is false - and then stop"""
        return self.__addfilter("dropwhile", pred)
