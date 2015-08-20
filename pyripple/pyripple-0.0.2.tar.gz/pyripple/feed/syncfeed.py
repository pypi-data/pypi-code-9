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

from pyripple.protocol import orderbook, ledger

from websocket import create_connection
from mpmath import mpf
import json

class SyncFeed:
  def __init__(self, ws= "wss://s-west.ripple.com:443"):
    self.ws= ws

  def getOrderbook(self, (c0, i0), (c1, i1), *args, **kwargs):

    def getAmount(a):
      if isinstance(a, basestring):
        return mpf(a) / mpf(1e6)
      else:
        return mpf(a['value'])
    
    def rate(x ,y):
      return mpf(x) / mpf(y)
    
    def process(offer, xlimit0, ask):
      x = mpf(getAmount(offer['TakerGets']))
      y = mpf(getAmount(offer['TakerPays']))
      if ask:
        x, y = y, x
      xlimit = xlimit0 + x
      return (xlimit, { 'rate': rate(x,y), 'limit': x, 'xlimit': xlimit, 'account': offer['Account'], 'sequence': offer['Sequence'] })

    ws = create_connection(self.ws)
    cc0 = {'currency': 'XRP'} if c0=='XRP' else {'currency': c0, 'issuer': i0}
    cc1 = {'currency': 'XRP'} if c1=='XRP' else {'currency': c1, 'issuer': i1}
    cmdA = {'command': 'book_offers', 'id': 1, 'limit': 1000, 'taker_gets': cc0, 'taker_pays': cc1}
    cmdB = {'command': 'book_offers', 'id': 1, 'limit': 1000, 'taker_gets': cc1, 'taker_pays': cc0}
    if kwargs.get('ledger') is not None:
      cmdA['ledger_index'] = kwargs.get('ledger')
      cmdB['ledger_index'] = kwargs.get('ledger')
    ws.send(json.dumps(cmdA))
    resultA = {}
    resultB = {}
    if kwargs.get('ledger') is None:
      resultA = json.loads(ws.recv())['result']
      cmdB['ledger_index'] = resultA['ledger_current_index']
      indexA = resultA['ledger_current_index']
      ws.send(json.dumps(cmdB))
    else:
      ws.send(json.dumps(cmdB))
      try:
        m = ws.recv()
        resultA = json.loads(m)['result']
      except KeyError:
        print 'Could find ledger #%i' % ledger
        return None
      indexA = resultA['ledger_index']
    try:
      m = ws.recv()
      resultB = json.loads(m)['result']
    except KeyError:
      print 'Could find ledger #%i' % ledger
      return None
    indexB = resultB['ledger_current_index'] if 'ledger_current_index' in resultB else resultB['ledger_index']
    assert(indexA==indexB)
    offersA = []
    xlimit= 0
    for x in resultA['offers']:
      (xlimit, r) = process(x, xlimit, True)
      offersA.append(r)
    offersB = []  
    xlimit= 0
    for x in resultB['offers']:
      (xlimit, r) = process(x, xlimit, False)
      offersB.append(r) 
    ws.close()
    return orderbook.Orderbook((c0, i0), (c1, i1), ledger.Ledger(indexA), offersA, ledger.Ledger(indexB), offersB)

