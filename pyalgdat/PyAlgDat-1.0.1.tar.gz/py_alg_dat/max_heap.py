#!/usr/bin/env python

# The MIT Licese (MIT)
#
# Copyright (C) 2015 by Brian Horn, trycatchhorn@gmail.com.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Provides a general data structure used to model a maximum heap.
"""

__author__ = "Brian Horn"
__copyright__ = "Copyright (c) 2015 Brian Horn"
__credits__ = "Brian Horn"
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Brian Horn"
__email__ = "trycatchhorn@gmail.com"
__status__ = "Prototype"

from py_alg_dat.binary_heap import BinaryHeap

class MaxHeap(BinaryHeap):

    """
    Implements a max-heap with the property that the data item stored
    in each node is greater than or equal to the data items stored
    in its children.
    """

    def __init__(self, start=None):
        """
        Constructs a max-heap from the specified array or
        creates an empty max-heap.
        """
        super(MaxHeap, self).__init__(start)
        if start == None:
            start = []
        self.build_max_heap(self.array)

    def __repr__(self):
        """
        Returns the canonical representation of this max-heap.

        @return: The canonical string representation of the max-heap.
        @rtype: C{string}
        """
        return '%s' % self.array

    def __str__(self):
        """
        Returns a string representation of this max-heap.

        @return: The string representation of the max-heap.
        @rtype: C{string}
        """
        start = 0
        length = 1
        str_rep = ""
        while start < len(self.array):
            str_rep += "\n"
            str_rep += str(self.array[start:start + length])
            start += length
            length *= 2
        return str_rep

    def __eq__(self, other):
        """
        Compares two max-heaps for equality. The comparison
        is done by comparing the list field of the two max-heaps.

        @param other: The other max-heap.
        @type other: C{MaxHeap}
        @return: True if the max-heaps are equal, false otherwise.
        @rtype: C{bool}
        """
        return self.array == other.array

    def __ne__(self, other):
        """
        Compares two max-heaps for inequality. The comparison
        is done by comparing the list field of the two max-heaps.

        @param other: The other max-heap.
        @type other: C{MaxHeap}
        @return: True if the max-heaps are not equal, false otherwise.
        @rtype: C{bool}
        """
        return not self == other

    def is_max_heap(self):
        """
        Determines if this heap is a max-heap.

        @return: True if this heap is a max-heap, false otherwise.
        @rtype: C{bool}
        """
        number_of_elements = len(self.array)
        for i in xrange(number_of_elements):
            left_index = self.left_child(i)
            right_index = self.right_child(i)
            if left_index < number_of_elements and self.array[left_index] > self.array[i]:
                return False
            if right_index < number_of_elements and self.array[right_index] > self.array[i]:
                return False
        return True

    def insert(self, key):
        """
        Inserts an element into the max-heap.

        Time complexity: O(log(n)).

        NOTE: When building a max-heap by starting with and empty max-heap
        and continuosly inserting keys into the heap, the order of insertions
        affects the result of the final max-heap. This means that building
        a heap this way, will not necessarily generate the same result as
        building a max-heap by initially passing in an array to the max-heap
        constructor. However, it is guaranteed that the max-heap generated by
        continuosly inserting keys will generated a max-heap that maintains
        the max-heap property.

        Examples:
        ------------------
        Staring with an empty max-heap h1 and insert keys into h1 as
        follows:

        h1 = MaxHeap()
        h1.insert( 4 )
        h1.insert( 1 )
        h1.insert( 3 )
        h1.insert( 2 )
        h1.insert( 16 )
        h1.insert( 9 )
        h1.insert( 10 )
        h1.insert( 14 )
        h1.insert( 8 )
        h1.insert( 7 )

        Will generate a max-heap with an array of keys in the order:
        h1.array = [16, 14, 10, 8, 7, 3, 9, 1, 4, 2].

        Creating a max-heap by passing in an array of keys to the
        constructor, where the order of the keys matches the order
        when continuosly inserting keys as above, is shown below:

        h2 = MaxHeap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7])

        This will generate a max-heap with an array of keys in the order:
        h2.array = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1].

        It is clear that h1.array != h2.array. To understand why the
        two approaches might create different results, depending on
        the order in which the keys are inserted, we look at the
        number of possible permutations of the inserted keys.

        In general, the number of permutations of the elements in
        a list is given by:

        number_of_permutations = n! = n * (n - 1 ) * (n - 2) ... 1,
        where n is the number of elements in the list. With a list
        of 10 elements, as above, this results in the following
        number of permutaions:

        number_of_permutaions = 10! = 3628800.

        Of these permutations only a small number result in combinations
        which match the array h2.array. More precisely the number of
        matching permutations is given by:

        number_of_permutations_matching = 784.

        Some of matching permutaions are shown below:

        (4, 16, 9, 2, 1, 10, 3, 14, 8, 7)
        (4, 16, 9, 2, 1, 10, 3, 8, 14, 7)
        (4, 16, 9, 14, 1, 10, 3, 2, 8, 7)
        (4, 16, 9, 14, 7, 10, 3, 2, 8, 1)
        (4, 16, 9, 8, 1, 10, 3, 2, 14, 7)
        .
        ..
        ...

        Naturally, this results in a number of combinations not
        matching the array h2.array. More precisely the number of
        permutations not matching is given by:

        number_of_permutaitions_not_matching = 3628016.

        Some of the permutations not matching are shown below:

        (4, 1, 3, 2, 16, 9, 10, 14, 8, 7)
        (4, 1, 3, 2, 16, 9, 10, 14, 7, 8)
        (4, 1, 3, 2, 16, 9, 10, 8, 14, 7)
        (4, 1, 3, 2, 16, 9, 10, 8, 7, 14)
        (4, 1, 3, 2, 16, 9, 10, 7, 14, 8)
        .
        ..
        ...
        However, it is important to state that the permutations
        not matching the array h2.array all result in max-heaps
        which satisfies the max-heap property.
        ------------------

        Time complexity: O(log(n)).

        @param key: The key of the node to be inserted into the max-heap.
        @type: C{int}
        """
        self.array.append(key)
        self.propagate_up(len(self.array) - 1)

    def remove(self, i):
        """
        Removes the element at the specified position from the
        max-heap.

        Time complexity: O(log(n)).

        @param i: The index of the node to be removed from the heap.
        @type: C{int}
        """
        if i < 0 or i > len(self.array) - 1:
            return None
        if i == len(self.array) - 1:
            pass
        else:
            self.swap(i, len(self.array) - 1)
            while i > 0 and self.array[self.parent(i)] < self.array[i]:
                self.swap(i, self.parent(i))
                i = self.parent(i)
            if len(self.array) != 0:
                self.propagate_down(i)
        self.array.pop()

    def propagate_up(self, i):
        """
        Compares node at index i with parent node and swaps it with
        the parent node if the node is larger that the parent node.

        Time complexity: O(log(n)).

        @param i: The index of the node from which propergation starts.
        @type: C{int}
        """
        if i <= 0 and i > len(self.array) - 1:
            return
        while i != 0 and self.array[i] > self.array[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def propagate_down(self, i):
        """
        Compares node at index i with the left node and moves the node
        at index i down the heap by successively exchanging the node
        with the smaller of its two children. The operation continues
        until the node reaches a position where it is less than both
        its children, or, failing that, until it reaches a leaf.

        Time complexity: O(log(n)).

        @param i: The index of the node from which propergation starts.
        @type: C{int}
        """
        if i <= 0 and i > len(self.array) - 1:
            return
        while not self.is_leaf(i):
            left_index = self.left_child(i)
            if left_index < len(self.array) - 1:
                if self.array[left_index + 1] > self.array[left_index]:
                    left_index += 1
            if self.array[left_index] <= self.array[i]:
                return
            self.swap(i, left_index)
            i = left_index

    def max_heapify_recursive(self, holder, i):
        """
        Responsible for maintaining the max-heap property of the max-heap.
        This function assumes that the subtree located at the left
        and right child satisfies the max-heap property. But the
        tree at index (current node) does not. Note: this function
        uses recursion, which for large inputs could cause a
        decrease in runtime performance compared to its iterative
        counterpart.

        Time complexity: O(log(n)).

        @param holder: The array backing the max-heap.
        @type: C{list}
        @param i: The index of the node from which the max-heap property should be maintained.
        @type: C{int}
        """
        left_index = self.left_child(i)
        right_index = self.right_child(i)
        largest = i
        if left_index < len(holder) and holder[left_index] > holder[i]:
            largest = left_index
        if right_index < len(holder) and holder[right_index] > holder[largest]:
            largest = right_index
        if largest != i:
            holder[i], holder[largest] = holder[largest], holder[i]
            self.max_heapify_recursive(holder, largest)

    def max_heapify_iterative(self, holder, i):
        """
        Responsible for maintaining the heap property of the heap.
        This function assumes that the subtree located at the left
        and right child satisfies the max-heap property. But the
        tree at index (current node) does not. Note: this function
        uses iteration, which for large inputs could give an increase
        in runtime performance compared to its recursive counterpart.

        Time complexity: O(log(n)).

        @param holder: The array backing the max-heap.
        @type: C{list}
        @param i: The index of the node from which the heap property should be maintained.
        @type: C{int}
        """
        left_index = self.left_child(i)
        while left_index < len(holder):
            right_index = left_index + 1
            if right_index == len(holder):
                if holder[left_index] > holder[i]:
                    holder[left_index], holder[i] = holder[i], holder[left_index]
                return
            choice = right_index
            if holder[left_index] > holder[right_index]:
                choice = left_index
            if holder[choice] < holder[i]:
                return
            holder[i], holder[choice] = holder[choice], holder[i]
            i = choice
            left_index = 2 * i + 1

    def build_max_heap(self, holder, recursive=True):
        """
        Responsible for building the heap bottom up. It starts with the lowest
        non-leaf nodes and calls heapify on them. This function is useful for
        initialising a heap with an unordered array.

        Time complexity: O(n).

        @param holder: The array backing the max-heap.
        @type: C{list}
        @param recursive: If True, the max-heap is build using recursion otherwise iteration.
        @type: C{int}
        """
        for i in xrange(len(holder) / 2, -1, -1):
            if recursive:
                self.max_heapify_recursive(holder, i)
            else:
                self.max_heapify_iterative(holder, i)

    def heap_sort(self):
        """
        The heap-sort algorithm.

        Time complexity: O(n*log(n)).
        """
        self.build_max_heap(self.array)
        output = []
        for i in xrange(len(self.array) -1, 0, -1):
            self.array[0], self.array[i] = self.array[i], self.array[0]
            output.append(self.array.pop())
            self.max_heapify_recursive(self.array, 0)
        output.append(self.array.pop())
        self.array = output

    def heap_extract_max(self):
        """
        Part of the Priority Queue, extracts the element on the top of
        the heap and then re-heapifies. Note: this function removes -and
        returns the element on top of the heap.

        Time complexity: O(log(n)).

        @return: The max element of this heap.
        @rtype: C{int}
        """
        max_value = self.array[0]
        data = self.array.pop()
        if len(self.array) > 0:
            self.array[0] = data
            self.max_heapify_recursive(self.array, 0)
        return max_value

    def heap_increase_key(self, i, key):
        """
        Implements the increase key operation.

        Time complexity: O(log(n)).

        @param i: The index of the node whose key is to increased.
        @type: C{int}
        @param key: The new key of the node to be increase in the heap.
        @type: C{int}
        """
        if key < self.array[i]:
            print "New key is smaller than current key!"
            return
        self.array[i] = key
        while i > 0 and self.array[self.parent(i)] < self.array[i]:
            self.array[i], self.array[self.parent(i)] = self.array[self.parent(i)], self.array[i]
            i = self.parent(i)

    def increment(self, key, value):
        """
        Increments key by the input value.

        Time complexity: O(n).

        @param key: The key which should be increased.
        @type: C{int}
        @param value: The value by which the key should be increased.
        @type: C{int}
        """
        for i in xrange(len(self.array)):
            if self.array[i] == key:
                self.array[i] += value
                self.propagate_up(i)
                break

    def heap_merge(self, heap):
        """
        Implements the merge heap operation.

        Time complexity: O(n).

        @param i: The heap which should be merged with this heap.
        @type: L{heap}
        @return: A heap which is the result of a merge between this heap and h.
        @type: L{heap}
        """
        nodes = self.array + heap.array
        result = MaxHeap(nodes)
        return result


