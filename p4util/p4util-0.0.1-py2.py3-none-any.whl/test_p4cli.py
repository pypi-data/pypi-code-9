'''Test cases for p4cli.py

$Id: //guest/lester_cheung/p4util/p4util/test_p4cli.py#1 $
$DateTime: 2014/04/01 19:11:15 $
$Author: lester_cheung $
'''

import unittest
import logging as log
DEBUGLVL = log.DEBUG
log.basicConfig(
    level=DEBUGLVL,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M',
)
from pprint import pprint, pformat


class NoEnoughTestExtendMe(unittest.TestCase):

    def setUp(self):
        from p4cli import P4
        p4 = P4()
        p4.user = 'someuser'
        p4.port = '1666'
        p4.client = 'noclient'
        p4.connect()
        self.p4 = p4

    def test_changes_m1(self):
        self.p4.run_changes('-m1')




if __name__ == '__main__':
    unittest.main()
