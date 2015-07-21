# Standard library imports.
import unittest

# Local imports.
from traits.api import HasTraits, Int
from pyface.tasks.topological_sort import before_after_sort, \
    topological_sort


class TestItem(HasTraits):

    id = Int
    before = Int
    after = Int

    def __init__(self, id, **traits):
        super(TestItem, self).__init__(id=id, **traits)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return repr(self.id)


class TopologicalSortTestCase(unittest.TestCase):

    def test_before_after_sort_1(self):
        """ Does the before-after sort work?
        """
        items = [ TestItem(1), TestItem(2), TestItem(3, before=2),
                  TestItem(4, after=1), TestItem(5) ]
        actual = before_after_sort(items)
        desired = [ TestItem(1), TestItem(3), TestItem(4),
                    TestItem(2), TestItem(5) ]
        self.assertEquals(actual, desired)

    def test_before_after_sort_2(self):
        """ Does the before-after sort work when both 'before' and 'after'
            are set?
        """
        items = [ TestItem(1), TestItem(2), TestItem(3),
                  TestItem(4, after=2, before=3) ]
        actual = before_after_sort(items)
        desired = [ TestItem(1), TestItem(2), TestItem(4), TestItem(3) ]
        self.assertEquals(actual, desired)

    def test_before_after_sort_3(self):
        """ Does the degenerate case for the before-after sort work?
        """
        actual = before_after_sort([ TestItem(1) ])
        desired = [ TestItem(1) ]
        self.assertEquals(actual, desired)

    def test_topological_sort_1(self):
        """ Does a basic topological sort work?
        """
        pairs = [ (1,2), (3,5), (4,6), (1,3), (1,4), (1,6), (2,4) ]
        result, has_cycles = topological_sort(pairs)
        self.assert_(not has_cycles)
        self.assertEquals(result, [1, 2, 3, 4, 5, 6])

    def test_topological_sort_2(self):
        """ Does another basic topological sort work?
        """
        pairs = [ (1,2), (1,3), (2,4), (3,4), (5,6), (4,5) ]
        result, has_cycles = topological_sort(pairs)
        self.assert_(not has_cycles)
        self.assertEquals(result, [1, 2, 3, 4, 5, 6])

    def test_topological_sort_3(self):
        """ Does cycle detection work?
        """
        pairs = [ (1,2), (2,3), (3,1) ]
        result, has_cycles = topological_sort(pairs)
        self.assert_(has_cycles)


if __name__ == '__main__':
    unittest.main()
