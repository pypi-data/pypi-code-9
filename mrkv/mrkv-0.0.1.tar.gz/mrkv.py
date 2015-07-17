
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
  zip, round, input, int, pow, object)

from collections import defaultdict, Counter
import random

class MarkovError(Exception):
  pass

class Markov(object):
  def __init__(self, order=1): 
    self._order = order
    self._rules = defaultdict(Counter)
    self.default = None

  def addTransition(self, pred, succ):
    '''Add/update a transition by passing a predecessor and a successor.'''
    if len(pred) != self._order:
      raise MarkovError('Predecessor is not of correct order.')
    self._rules[pred].update([succ])

  def generate(self, pred):
    '''Generate a single state given a predecessor.'''
    choice = self.default

    elts = self._rules[pred].most_common()
    totalSum = 0
    for _, count in elts:
      totalSum += count

    rnd = random.random()
    currentSum = 0
    for elt, count in elts:
      if rnd >= currentSum / totalSum \
          and rnd <= (currentSum + count) / totalSum:
        choice = elt
      currentSum += count
        
    return choice

  def addTransitions(self, states):
    '''Add a set of transitions given a sequence of states.''' 
    limit = len(states) - self._order
    if limit < 0:
      raise MarkovError('State list is too short.')

    for i in range(limit):
      pred = []
      for j in range(self._order):
        pred.append(states[i+j])
      succ = states[i + self._order]
      self.addTransition(tuple(pred), succ)
    
  def generateSequence(self, pred, length):
    '''Generate a sequence of desired length given a predecessor.'''
    seq = list(pred)
    for i in range(length):
      succ = self.generate(tuple(seq[i:i+self._order]))
      seq.append(succ)
    return seq[self._order:]

