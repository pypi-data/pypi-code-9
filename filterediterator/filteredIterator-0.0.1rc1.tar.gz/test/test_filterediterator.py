#!/usr/bin/env python
"""
# filteredIterator : Test Suite for FilteredIterator

Summary : 
    <summary of module/class being tested>
Use Case : 
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I <Boolean statement>
    ....
"""

import unittest
import filterediterator

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '21 Oct 2015'


class Constructors(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_00_000_constructionFromIterator(self):
        """Simple construction test from Iterator"""
        iter_exp = (x for x in xrange(0, 11))
        fg = filterediterator.FilteredIterator(xrange(0, 11))
        self.assertEqual([x for x in iter_exp], [x for x in fg])

    def test_00_001_constructionFromList(self):
        """Construction of Iterator from List"""
        lst = [x for x in xrange(0, 11)]
        fg = filterediterator.FilteredIterator(lst)
        self.assertEqual(lst, [x for x in fg])

    def test_00_002_constructionFromSequence(self):
        """Construction of Iterator from Sequence"""
        seq = "01234567890"
        fg = filterediterator.FilteredIterator(seq)
        self.assertEqual([c for c in list(seq)], [x for x in fg])


class ListOfNumbers(unittest.TestCase):
    def setUp(self):
        self.lst = range(0, 11)
        self.fi = filterediterator.FilteredIterator(self.lst)

    def tearDown(self):
        pass


class Filters(ListOfNumbers):
    def test_01_000_SingleEmptyFilter(self):
        """Single Empty filter"""
        self.assertEqual([n for n in self.fi.filter()], filter(lambda x: x, self.lst))

    def test_01_001_SingleFilter(self):
        """Single unchained filter"""
        self.assertEqual([n for n in self.fi.filter(lambda x: (x % 2))], filter(lambda x: x % 2, self.lst))

    def test_01_002_SillyFilter(self):
        """Single Silly Filter - a filter which can never be true"""
        self.assertEqual([n for n in self.fi.filter(lambda x: x > 20)],
                         filter(lambda x: x > 20, self.lst))


class TakeWhile(ListOfNumbers):
    def test_02_000_TakewhileSubList(self):
        """Takewhile with subsection of list"""
        self.assertEqual([n for n in self.fi.takewhile(lambda x: x < 5)], [0, 1, 2, 3, 4])

    def test_02_001_TakewhileWholeList(self):
        """Takewhile with the whole list"""
        self.assertEqual([n for n in self.fi.takewhile(lambda x: x >= 0)], self.lst)

    def test_02_002_TakewhileEmptyList(self):
        """Takewhile returns Empty list"""
        self.assertEqual([n for n in self.fi.takewhile(lambda x: x < 0)], [])

    def test_02_010_TakeWhileRepeatList(self):
        """Takewhile stops even though List repeats - i.e. not just a filter"""
        lst = self.lst + self.lst
        fi = filterediterator.FilteredIterator(lst)
        self.assertEqual([n for n in fi.takewhile(lambda x: x < 5)], [0, 1, 2, 3, 4])
        # For completeness - prove this is not just a filter
        fi = filterediterator.FilteredIterator(lst)
        self.assertNotEqual([n for n in fi.filter(lambda x: x < 5)], [0, 1, 2, 3, 4])


class DropWhile(ListOfNumbers):
    def test_03_000_DropWhileDropSubList(self):
        """DropWhile with subsection of list"""
        self.assertEqual([n for n in self.fi.dropwhile(lambda x: x < 5)], [5, 6, 7, 8, 9, 10])

    def test_03_001_DropWhileDropWholeList(self):
        """DropWhile with subsection of list"""
        self.assertEqual([n for n in self.fi.dropwhile(lambda x: x < 20)], [])

    def test_03_002_DropWhileDropNothing(self):
        """DropWhile with subsection of list"""
        self.assertEqual([n for n in self.fi.dropwhile(lambda x: x > 20)], self.lst)

    def test_03_003_DropWhileDropStartRepeatList(self):
        """DropWhile with repeating section of list - items dropped only at the start"""
        lst = self.lst + self.lst
        fi = filterediterator.FilteredIterator(lst)
        self.assertEqual([n for n in fi.dropwhile(lambda x: x < 5)],
                         [5, 6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


class LongListOfNumbers(unittest.TestCase):
    def setUp(self):
        self.lst = [0] * 3 + [1] * 3 + [2] * 3 + [4] * 3 + [5] * 3
        self.fi = filterediterator.FilteredIterator(self.lst)

    def tearDown(self):
        pass


class Combination(LongListOfNumbers):
    def test_04_000_ChainedFilter(self):
        """Chained filter"""
        self.assertEqual([n for n in self.fi.filter(lambda x: (x % 2)).filter(lambda x: x > 5)],
                         filter(lambda x: x % 2 and x > 5, self.lst))

    def test_04_001_Filter_and_Take(self):
        """Filter out values and then take while - both chains should result the same"""
        self.assertEqual([n for n in self.fi.filter(lambda x: 0 <= x <= 2).takewhile(lambda x: (x % 2))], [])
        self.assertEqual([n for n in self.fi.takewhile(lambda x: (x % 2)).filter(lambda x: 0 <= x <= 2)], [])


# noinspection PyUnusedLocal,PyUnusedLocal
def load_tests(loader, tests=None, pattern=None):
    classes = [Constructors,
               Filters,
               TakeWhile,
               DropWhile,
               Combination
               ]
    suite = unittest.TestSuite()
    for test_class in classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    ldr = unittest.TestLoader()

    test_suite = load_tests(ldr)

    unittest.TextTestRunner(verbosity=2).run(test_suite)
