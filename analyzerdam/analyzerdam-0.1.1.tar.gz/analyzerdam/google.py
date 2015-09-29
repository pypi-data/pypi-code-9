'''
Created on Nov 9, 2011

@author: ppa
'''
from analyzer.dam.baseDAM import BaseDAM
from analyzerdam.google_finance import GoogleFinance

import logging
LOG = logging.getLogger()


class GoogleDAM(BaseDAM):
    ''' Google DAO '''

    def __init__(self):
        super(GoogleDAM, self).__init__()
        self.google_finance = GoogleFinance()

    def read_quotes(self, start, end):
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return []

        return self.google_finance.quotes(self.symbol, start, end)

    def read_ticks(self, start, end):
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return []

        return self.google_finance.ticks(self.symbol, start, end)

    def read_fundamental(self):
        if self.symbol is None:
            LOG.debug('Symbol is None')
            return {}

        return self.google_finance.financials(self.symbol)
