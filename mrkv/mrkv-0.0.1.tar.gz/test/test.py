
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
  zip, round, input, int, pow, object)

from mrkv import Markov
import unittest
import random
from collections import Counter

class MarkovTester(unittest.TestCase):
  def test_deterministic_chain(self):
    # should generate a specific sequence 
    states = ['a', 'b', 'c', 'd', 'e']
    m = Markov(order=2)
    m.addTransitions(states)
    seq = m.generateSequence(['a','b'], 3)
    self.assertTrue(seq == ['c', 'd', 'e'])

  def test_probabilistic_generation(self):
    # should generate approximately 
    # equal numbers of 'a's and 'b's
    m = Markov(order=1)
    m.addTransition(tuple('a'), 'a')
    m.addTransition(tuple('a'), 'b')
    m.addTransition(tuple('b'), 'a')
    m.addTransition(tuple('b'), 'b')
    count = 100000
    epsilon = 1000
    seq = m.generateSequence('a', count)
    c = Counter(seq)
    self.assertTrue(c['a'] + c['b'] == count)
    self.assertTrue(abs(c['a'] - c['b']) < epsilon)

if __name__ == '__main__':
  unittest.main(verbosity=2)

