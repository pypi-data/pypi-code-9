from nanomsg import *
from config import *
import pymerlion
import multiprocessing
from websocket import create_connection
import time, os
from ticktype import *
from decimal import Decimal
import signal
import numbers

def run_daemon():
    ib = pymerlion.tradingsystem()
    print 'Mode:', yml_sentosa['global']['mode']
    ib.run()

class Merlion(object):
  def __init__(self, account=None):
    self.s1 = None
    self.account = yml_sentosa['global']['account']
    self.symbols = SYMBOLS
    self.trade_num = {}
    [self.trade_num.setdefault(i, 0) for i in self.symbols]
    self.p = None
    self.interest_list=[]

  def rerun(self):
    if self.p:
      os.kill(self.p.pid, signal.SIGINT)
      time.sleep(3)
      self.run()

  def subscribe(self):
    #self.universe.append(symbols)
    self.s1 = Socket(SUB)
    url = 'tcp://127.0.0.1:{}'.format(yml_sentosa['global']['MKD_TO_ALGO_PORT'])
    self.s1.connect(url)
    #self.s1.set_int_option(SOL_SOCKET, RCVTIMEO, 100)
    #for s in self.symbols:
    #  self.s1.set_string_option(SUB, SUB_SUBSCRIBE, s)
    self.s1.set_string_option(SUB, SUB_SUBSCRIBE, '')

  def connect_oms(self):
      while 1:
          try:
              url = 'ws://{}:16180/ws'.format(LOCALIP)
              #print url
              self.ws = create_connection(url)
              return
          except:
              pass
              time.sleep(1)

  def get_mkdata(self):
    while self.s1:
      msg = self.s1.recv()
      #print msg
      if msg is not None and msg.index('|') > 0:
        v = msg.split('|')
        if len(v) == 3:
            if self.interest_list and v[0] in self.interest_list:
                print msg
            if v[1] == 'ASK_PRICE' and float(v[2]) > 0:
                return v[0], ASK_PRICE, float(v[2])
            elif v[1] == 'BID_PRICE' and float(v[2]) > 0:
                return v[0], BID_PRICE, float(v[2])

  def track_msg(self, target):
    self.interest_list.append(target)

  def get_balance(self):
    pass

  def get_uPNL(self):
    pass

  def get_aPNL(self):
    pass

  def buy(self, ticker, share):
    msg='m|{}|{}'.format(ticker,share)
    self.ws.send(msg)

  def sell(self, ticker, share):
    msg='m|{}|{}'.format(ticker,-share)
    self.ws.send(msg)

  def run(self):
    self.p = multiprocessing.Process(target=run_daemon)
    self.p.start()
    self.subscribe()
    self.connect_oms()
    return self

if __name__ == "__main__":
    m = Merlion()
    m.run()
    while True:
        symbol, ticktype, value = m.get_mkdata()
        if symbol == 'FXI':
            print symbol, ticktype, value
            if int(ticktype) == ASK_PRICE:# and Decimal(value) > 0 and  Decimal(value) < 100:
                m.buy(symbol, 100)
                #m.wait_until_filled()
                break
            elif int(ticktype) == BID_PRICE and Decimal(value) > 150:
                m.sell(symbol, 100)
                break
        time.sleep(0.1)


