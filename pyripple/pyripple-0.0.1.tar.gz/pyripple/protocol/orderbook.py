# PyRipple
#
# Copyright 2015 Gilles Pirio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gilles Pirio <gilles.xrp@gmail.com>
"""

import numpy as np
import pandas as pd
import mpmath as mp
from mpmath import mpf
import matplotlib
import matplotlib.pyplot as plt
import json


def _weigtedAverage(book, target):
  rs = 0
  ws = 0
  t = target
  for order in book:
    if t <= order['limit']:
      rs += t
      ws += t*order['rate']
      return ws / rs
    else:
      rs += order['limit']
      ws += order['limit']*order['rate']
      t -= order['limit']

def _currencyStr((c, i)):
  return 'XRP' if c=='XRP' else '%s@%s' % (c, i)

def _foldBook(accumulator, orderbook):
  if accumulator is None:
    accumulator = { 'bids': { }, 'asks': { }, 'ledgers': [ ] }
  ldg= orderbook.ledger.index
  accumulator['ledgers'].append(ldg)
  for offer in orderbook.offersA:
    uid = (offer['account'], offer['sequence'])
    if uid in accumulator['asks']:
      accumulator['asks'][uid]['end'] = ldg
    else:
      accumulator['asks'][uid] = { 'start': ldg, 'end': ldg, 'offer': offer }
  for offer in orderbook.offersB:
    uid = (offer['account'], offer['sequence'])
    if uid in accumulator['bids']:
      accumulator['bids'][uid]['end'] = ldg
    else:
      accumulator['bids'][uid] = { 'start': ldg, 'end': ldg, 'offer': offer }
  return accumulator

def _foldBooks(orderbooks):
  acc = None
  for orderbook in orderbooks:
    acc = _foldBook(acc, orderbook)
  return acc

class Orderbook:
  def __init__(self, (c0, i0), (c1, i1), ldgA, offersA, ldbB, offersB, through=[]):
    self.c0= c0
    self.i0= i0
    self.c1= c1
    self.i1= i1
    self.offersA= offersA
    self.offersB= offersB
    self.spread= offersA[0]['rate']-offersB[0]['rate']
    self.spread_pct= self.spread*100 /  offersA[0]['rate']
    self.ledger= ldgA
    self.through= through
  def weigtedAverageA(self, v): 
    return _weigtedAverage(self.offersA, v)
  def weigtedAverageB(self, v): 
    return _weigtedAverage(self.offersB, v)
  def info(self):
    return {
      'currency': _currencyStr((self.c0, self.i0)),
      'counter_currency': _currencyStr((self.c1, self.i1)),
      'spread': self.spread,
      'spread': self.spread_pct,
      'best_ask': self.offersA[0]['rate'],
      'n_asks': len(self.offersA),
      'n_bids': len(self.offersB),
      'best_bid': self.offersB[0]['rate'],
      'through': self.through
    }

  def showInfo(self):
    print ('Orderbook %s%s in ledger %i' % (self.c0, self.c1, self.ledger.index))
    print ('  Close date: %s' % self.ledger.date_human)
    print ('  Currency: XRP' if self.c0=='XRP' else '  Currency: %s@%s' % (self.c0, self.i0))
    print ('  Counter currency: XRP' if self.c1=='XRP' else '  Counter currency: %s@%s' % (self.c1, self.i1))
    print ('  Spread: %f (%f %%)' % (self.spread, self.spread_pct))
    print ('  Best ask/bid: %f / %f' % (self.offersA[0]['rate'], self.offersB[0]['rate']))
    print '  Through: ', self.through
  
  def __mul__(self, other):
    assert self.c1 == other.c0 and self.i1 == other.i0, "Invalide trade"
    # Let's compute the new orderbook!
    def prudctOffers(o0, o1):
      offers = []
      i0= 0
      i1= 0
      xlim= 0
      o0limit= 0
      o1limit= 0
      while i1 < len(o1) and i0 < len(o0):
        if o0limit==0:
          o0rate= o0[i0]['rate']
          o0limit= o0[i0]['limit']
          i0+= 1
        if o1limit==0:
          o1rate= o1[i1]['rate']
          o1limit= o1[i1]['limit']
          i1+= 1
        delta = o0limit*o0rate-o1limit        
        if delta<0:
          amt= o0limit*o1rate
          o0limit= 0
          o1limit-= amt
          xlim+= amt
          offers.append({ 'rate': o0rate*o1rate, 'limit': amt, 'xlimit': xlim })
        elif delta>0:
          amt= o1limit
          o1limit= 0
          o0limit-= amt
          xlim+= amt
          offers.append({ 'rate': o0rate*o1rate, 'limit': amt, 'xlimit': xlim })
        else:
          o0limit= 0
          o1limit= 0
          xlim+= o1limit
          offers.append({ 'rate': o0rate*o1rate, 'limit': o1limit, 'xlimit': xlim })
      return offers
    through = list(self.through)
    through.append((self.c1, self.i1))
    return Orderbook((self.c0, self.i0), 
                     (other.c1, other.i1), 
                     self.ledger, prudctOffers(self.offersA, other.offersA), other.ledger, prudctOffers(self.offersB, other.offersB), through)

  def plot(self, *args, **kwargs):
    fA = pd.DataFrame(self.offersA)
    fB = pd.DataFrame(self.offersB)
    newfig= kwargs.get('newfig', True)
    if newfig:
      plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k'); 
      axes = plt.gca(); 
      plt.title('Order book for %s / %s at ledger %i' % (_currencyStr((self.c0, self.i0)), _currencyStr((self.c1, self.i1)), self.ledger.index)); 
      plt.xlabel(_currencyStr((self.c1, self.i1)))
      plt.ylabel('%s%s' % (self.c0, self.c1)) 
      plt.gca().xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    if kwargs.get('orders', True):
      plt.hlines(fA['rate'], 0, fA['limit'], color='b', label= 'Asks')
      plt.plot(fA['limit'], fA['rate'], 'b^')
      plt.hlines(fB['rate'], 0, fB['limit'], color='r', label= 'Bids')
      plt.plot(fB['limit'], fB['rate'], 'r^')
    def supplyDemand(xlimits):
      x= []
      y= []
      limit= 0
      for (r, l) in xlimits:
        x.append(r)
        x.append(r)
        y.append(limit)
        limit= l
        y.append(limit)
      return (x,y)
    if kwargs.get('supplydemand', True):
      (x, y)= supplyDemand(zip(fA['rate'], fA['xlimit']))
      plt.plot(y, x, 'b--', label= 'Supply')
      (x, y)= supplyDemand(zip(fB['rate'], fB['xlimit']))
      plt.plot(y, x, 'r--', label= 'Demand')
    if newfig:
      plt.legend()
  
  def plotWeighted(self, limit, *args, **kwargs):
    newfig= kwargs.get('newfig', True)
    if newfig:
      plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k'); 
      plt.xlabel('%s@%s' % (self.c1, self.i1))
      plt.title('Rate (weigthed average) for %s / %s ledger %i' % (_currencyStr((self.c0, self.i0)), _currencyStr((self.c1, self.i1)), self.ledger.index))
      plt.gca().xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    x = np.arange(1, limit, limit / 1000 if limit > 1000 else 1)
    cask = kwargs.get('styleask', 'b')
    cbid = kwargs.get('stylebid', 'r')
    label = kwargs.get('label', 'Weighted avg')
    plt.plot(x, map(self.weigtedAverageA, x), cask, label= label + ' (ask)')
    plt.plot(x, map(self.weigtedAverageB, x), cbid, label= label + ' (bid)')
    if newfig:
      plt.legend()  

  @staticmethod
  def plotTimeResolvedBook(orderbooks):
    ob0 = orderbooks[0]
    fold = _foldBooks(orderbooks)
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k'); 
    plt.hlines(map(lambda x: x['offer']['rate'], fold['asks'].values()), 
               map(lambda x: x['start'], fold['asks'].values()), 
               map(lambda x: x['end'], fold['asks'].values()), color ='b', label= 'asks' )
    plt.hlines(map(lambda x: x['offer']['rate'], fold['bids'].values()), 
               map(lambda x: x['start'], fold['bids'].values()), 
               map(lambda x: x['end'], fold['bids'].values()), color ='r', label= 'bids' )
    x = map(lambda ob: ob.ledger.index, orderbooks)
    plt.plot(x, map(lambda x: x.offersA[0]['rate'], orderbooks), 'b--')
    plt.plot(x, map(lambda x: x.offersB[0]['rate'], orderbooks), 'r--')
    axes = plt.gca()
    axes.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))
    axes.set_xlabel('Ripple ledger #')
    axes.set_ylabel('%s%s' % (ob0.c0, ob0.c1)) 
    plt.title('Order books for %s / %s' % (_currencyStr((ob0.c0, ob0.i0)), _currencyStr((ob0.c1, ob0.i1))));
    plt.legend()

