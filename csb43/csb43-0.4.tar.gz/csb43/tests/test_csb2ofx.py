
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import unittest
import datetime
from lxml import etree
import os.path

from .. import ofx
from .. import csb43
from ..utils import m3_bytes


class TestCsb2Ofx(unittest.TestCase):

    def setUp(self):

        f = csb43.File(strict=False)

        for n in range(2):
            ac = csb43.Account(strict=False)

            ac.currency = "EUR"
            ac.shortName = "John Doe"
            ac.accountNumber = "%010d" % n
            ac.bankCode = "0001"
            ac.branchCode = "0005"
            ac.infomationMode = 1
            ac.initialBalance = 10 ** n

            f.add_account(ac)

            for m in range(3):
                t = csb43.Transaction(strict=False)
                t.transactionDate = datetime.datetime(year=2012,
                                                      month=2,
                                                      day=n+1).date()
                t.valueDate = t.transactionDate
                t.documentNumber = n * 10 + m
                t.sharedItem = 12
                t.ownItem = 123
                t.reference1 = "1" * 12
                t.reference2 = "2" * 16
                t.amount = 53.2

                #it = csb43.Item(strict=False)
                #it.item1 = n
                #it.item2 = m
                #t.add_item(it)

                f.add_transaction(t)

            ac.initialDate = ac.transactions[0].transactionDate
            ac.finalDate = ac.transactions[-1].transactionDate

            f.close_account()

        f.close_file()

        self.n_fitid = len(f.accounts) * len(ac.transactions)
        self.csb = f
        self.ofx = ofx.convertFromCsb(self.csb)

    def test_unique_fitid(self):
        """
        fitid field has a unique constraint
        """

        xml = etree.fromstring(str(self.ofx).encode("UTF-8"))

        fitid = [node.text for node in xml.xpath("//STMTTRN/FITID")]

        self.assertEqual(len(fitid), len(set(fitid)),
                         "all FITID content must be unique within an OFX file")

    def test_v211_xsd_validation(self):
        """
        XSD
        """

        xsd_path = os.path.join(os.path.dirname(__file__),
                                "schemas",
                                "ofx2.1.1",
                                "OFX2_Protocol.xsd")

        if not os.path.exists(xsd_path):
            raise unittest.SkipTest("OFX 2.1.1 Schema not found")


        xsd = etree.XMLSchema(file=xsd_path)

        document = str(self.ofx)

        document = (document
                    .replace("<OFX>", '<ofx:OFX xmlns:ofx="http://ofx.net/types/2003/04">')
                    .replace("</OFX>", "</ofx:OFX>"))

        root = etree.fromstring(document.encode("UTF-8"))

        xsd.assertValid(root)



