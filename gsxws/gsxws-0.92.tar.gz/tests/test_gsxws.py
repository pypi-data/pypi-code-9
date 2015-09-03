# -*- coding: utf-8 -*-

import logging
from os import environ as env
from datetime import date, datetime

from unittest import main, skip, TestCase

from gsxws.objectify import parse, gsx_diags_timestamp
from gsxws.products import Product
from gsxws import (repairs, escalations, lookups, returns,
                   GsxError, ServicePart, diagnostics, comptia,)


def empty(a):
    return a in [None, '', ' ']


class RemoteTestCase(TestCase):
    def setUp(self):
        from gsxws.core import connect
        connect(env['GSX_USER'], env['GSX_SOLDTO'], env['GSX_ENV'])
        self.sn = env['GSX_SN']
        device = Product(sn=self.sn)

        # pick the first part with a component code
        self.first_part = [x for x in device.parts() if not empty(x.componentCode)][0]

        self.part = repairs.RepairOrderLine()
        self.part.partNumber = self.first_part.partNumber
        self.part.comptiaCode = 'X01'
        self.part.comptiaModifier = 'A'

    def assertUnicodeOrInt(self, val):
        try:
            self.assertIsInstance(val, unicode)
        except AssertionError:
            self.assertIsInstance(val, int)


class ComptiaTestCase(RemoteTestCase):
    def test_fetch_comptia(self):
        data = comptia.fetch()
        self.assertIsInstance(data['E'], dict)


class DiagnosticsTestCase(RemoteTestCase):
    def setUp(self):
        super(DiagnosticsTestCase, self).setUp()
        self.diag = diagnostics.Diagnostics(serialNumber=self.sn)
        self.diag.shipTo = env['GSX_SHIPTO']

    def test_fetch(self):
        self.diag = diagnostics.Diagnostics(alternateDeviceId=self.sn)
        res = self.diag.fetch()

        for r in res.diagnosticTestData.testResult.result:
            self.assertIsInstance(r.name, unicode)
            self.assertUnicodeOrInt(r.value)

        for r in res.diagnosticProfileData.profile.unit.key:
            self.assertIsInstance(r.name, unicode)
            self.assertUnicodeOrInt(r.value)

        for r in res.diagnosticProfileData.report.reportData.key:
            self.assertUnicodeOrInt(r.value)

    def test_initiate_email(self):
        self.diag.emailAddress = env['GSX_EMAIL']
        res = self.diag.initiate()
        self.assertRegexpMatches(str(res), r'\d+')

    def test_initiate_phone(self):
        self.diag.phoneNumber = env['GSX_PHONE']
        with self.assertRaisesRegexp(GsxError, 'SMS sending is not supported'):
            self.diag.initiate()


class RepairTestCase(RemoteTestCase):
    def setUp(self):
        from datetime import datetime, timedelta
        super(RepairTestCase, self).setUp()
        customer = repairs.Customer(emailAddress='test@example.com')
        customer.firstName = 'First Name'
        customer.lastName = 'Last Name'
        customer.addressLine1 = 'Address Line 1'
        customer.primaryPhone = '0123456789'
        customer.city = 'Helsinki'
        customer.zipCode = '12345'
        customer.state = 'ZZ'
        customer.country = 'FI'
        self.customer = customer

        d = datetime.now() - timedelta(days=7)
        self.date = d.strftime('%m/%d/%y')
        self.time = d.strftime('%I:%M AM')

        cdata = comptia.fetch()
        gcode = str(self.first_part.componentCode)

        _comptia = repairs.CompTiaCode(comptiaGroup=gcode)
        _comptia.comptiaModifier = comptia.MODIFIERS[0][0]
        ccode, cdesc = cdata[gcode].popitem()
        _comptia.comptiaCode = ccode
        self.comptia = _comptia

        self._symptoms = repairs.SymptomIssue(serialNumber=self.sn).fetch()
        self.symptom = self._symptoms[0][0]
        self._issues = repairs.SymptomIssue(reportedSymptomCode=self.symptom).fetch()
        self.issue = self._issues[0][0]


class TestCoreFunctions(TestCase):
    def test_dump(self):
        rep = repairs.Repair(blaa=u'ääöö')
        part = repairs.RepairOrderLine()
        part.partNumber = '661-5571'
        rep.orderLines = [part]
        self.assertRegexpMatches(rep.dumps(), '<GsxObject><blaa>ääöö</blaa><orderLines>')


class TestTypes(TestCase):
    def setUp(self):
        xml = open('tests/fixtures/escalation_details_lookup.xml', 'r').read()
        self.data = parse(xml, 'lookupResponseData')

    def test_unicode(self):
        self.assertIsInstance(self.data.lastModifiedBy, unicode)

    def test_timestamp(self):
        self.assertIsInstance(self.data.createTimestamp, datetime)

    def test_ts_comp(self):
        self.assertGreater(datetime.now(), self.data.createTimestamp)

    def test_list(self):
        for x in self.data.escalationNotes.iterchildren():
            self.assertIsInstance(x.text, str)


class TestErrorFunctions(TestCase):
    def setUp(self):
        xml = open('tests/fixtures/multierror.xml', 'r').read()
        self.data = GsxError(xml=xml)

    def test_code(self):
        self.assertEqual(self.data.errors['RPR.ONS.025'],
                        'This unit is not eligible for an Onsite repair from GSX.')

    def test_message(self):
        self.assertRegexpMatches(self.data.message, 'Multiple error messages exist.')

    def test_exception(self):
        msg = 'Connection failed'
        e = GsxError(msg)
        self.assertEqual(e.message, msg)

    def test_error_ca_fmip(self):
        from gsxws.core import GsxResponse
        xml = open('tests/fixtures/error_ca_fmip.xml', 'r').read()
        with self.assertRaisesRegexp(GsxError, 'A repair cannot be created'):
            GsxResponse(xml=xml, el_method='CreateCarryInResponse', 
                        el_response='repairConfirmation')
        


class TestLookupFunctions(RemoteTestCase):
    def test_component_check(self):
        l = lookups.Lookup(serialNumber=env['GSX_SN'])
        l.repairStrategy = "CA"
        l.shipTo = env['GSX_SHIPTO']
        r = l.component_check()
        self.assertFalse(r.eligibility)

    def test_component_check_with_parts(self):
        l = lookups.Lookup(serialNumber=env['GSX_SN'])
        l.repairStrategy = "CA"
        l.shipTo = env['GSX_SHIPTO']
        r = l.component_check([self.part])
        self.assertFalse(r.eligibility)


class TestEscalationFunctions(RemoteTestCase):
    def setUp(self):
        super(TestEscalationFunctions, self).setUp()
        esc = escalations.Escalation()
        esc.shipTo = env['GSX_SHIPTO']
        esc.issueTypeCode = 'WS'
        esc.notes = 'This is a test'
        c1 = escalations.Context(1, self.sn)
        c2 = escalations.Context(12, '2404776')
        esc.escalationContext = [c1, c2]
        self.escalation = esc.create()

    def test_create_general_escalation(self):
        self.assertTrue(self.escalation.escalationId)

    def test_update_general_escalation(self):
        esc = escalations.Escalation()
        esc.escalationId = self.escalation.escalationId
        esc.status = escalations.STATUS_CLOSED
        result = esc.update()
        self.assertEqual(result.updateStatus, 'SUCCESS')

    @skip("Skip")
    def test_attach_general_escalation(self):
        esc = escalations.Escalation()
        esc.escalationId = self.escalation.escalationId
        esc.attachment = escalations.FileAttachment('/tmp/logo.png')
        result = esc.update()
        self.assertEqual(result.updateStatus, 'SUCCESS')

    def test_lookup_general_escalation(self):
        esc = escalations.Escalation()
        esc.escalationId = self.escalation.escalationId
        result = esc.lookup()
        self.assertEqual(result.escalationType, 'GSX Help')


class TestRepairFunctions(RepairTestCase):
    def test_symptom_code(self):
        self.assertEqual(self._symptoms[0][0], 'PD17A')

    def test_issue_code(self):
        self.assertEqual(self._issues[0][0], 'PD17-01')
    
    def test_create_carryin(self):
        rep = repairs.CarryInRepair()
        rep.serialNumber = self.sn
        rep.unitReceivedDate = self.date
        rep.unitReceivedTime = self.time
        rep.orderLines = [self.part]
        rep.shipTo = env['GSX_SHIPTO']
        rep.poNumber = '123456'
        rep.symptom = 'This is a test symptom'
        rep.diagnosis = 'This is a test diagnosis'
        rep.customerAddress = self.customer
        rep.reportedSymptomCode = self.symptom
        rep.reportedIssueCode = self.issue
        rep.create()

    def test_repair_or_replace(self):
        rep = repairs.RepairOrReplace()
        rep.serialNumber = env['GSX_SN']
        rep.unitReceivedDate = self.date
        rep.unitReceivedTime = self.time
        rep.shipTo = env['GSX_SHIPTO']
        rep.purchaseOrderNumber = '123456'
        rep.coverageOptions = 'A1'
        rep.symptom = 'This is a test symptom'
        rep.diagnosis = 'This is a test diagnosis'
        rep.shipper = 'XUPSN'
        rep.trackingNumber = '123456'
        rep.customerAddress = self.customer
        rep.orderLines = [self.part]

        rep.reportedSymptomCode = self.symptom
        rep.reportedIssueCode = self.issue

        rep.reportedSymptomCode = ''
        rep.reportedIssueCode = ''

        rep.create()

    def test_mail_in(self):
        rep = repairs.MailInRepair()
        rep.serialNumber = self.sn
        rep.unitReceivedDate = self.date
        rep.unitReceivedTime = self.time
        rep.orderLines = [self.part]
        rep.shipTo = env['GSX_SHIPTO']
        rep.diagnosedByTechId = env['GSX_TECHID']
        rep.symptom = 'This is a test symptom'
        rep.diagnosis = 'This is a test diagnosis'
        rep.customerAddress = self.customer
        rep.reportedSymptomCode = self.symptom
        rep.reportedIssueCode = self.issue
        rep.addressCosmeticDamage = False
        rep.purchaseOrderNumber = '123456'
        rep.soldToContact = 'Firstname Lastname'
        rep.soldToContactPhone = '123456'
        rep.comptia = [self.comptia]
        rep.shipper = returns.CARRIERS[25][0]
        rep.trackingNumber = '12345678'
        rep.create()

    def test_whole_unit_exchange(self):
        rep = repairs.WholeUnitExchange()
        rep.serialNumber = ''
        rep.unitReceivedDate = self.date
        rep.unitReceivedTime = self.time
        rep.shipTo = env['GSX_SHIPTO']
        rep.purchaseOrderNumber = '123456'
        rep.symptom = 'This is a test symptom'
        rep.diagnosis = 'This is a test diagnosis'
        rep.customerAddress = self.customer
        rep.orderLines = [self.part]
        rep.create()


class TestPartFunction(RemoteTestCase):
    def test_product_parts(self):
        parts = Product(env['GSX_SN']).parts()
        self.assertIsInstance(parts[0].partNumber, basestring)


class TestRemoteWarrantyFunctions(TestCase):
    @classmethod
    def setUpClass(cls):
        from gsxws.core import connect
        connect(env['GSX_USER'], env['GSX_SOLDTO'], env['GSX_ENV'])

    def setUp(self):
        super(TestRemoteWarrantyFunctions, self).setUp()
        self.sn = env['GSX_SN']
        device = Product(sn=self.sn)
        self.product = Product(env['GSX_SN'])
        self.wty = self.product.warranty(ship_to=env['GSX_SHIPTO'])

    def test_warranty_lookup(self):
        self.assertEqual(self.wty.warrantyStatus, 'Out Of Warranty (No Coverage)')

    def test_warranty_lookup_imei(self):
        wty = Product(env['GSX_IMEI']).warranty()
        self.assertEqual(wty.warrantyStatus, 'Out Of Warranty (No Coverage)')

    def test_fmip_status(self):
        self.assertIn('Find My iPhone is active', self.product.fmip_status)

    def test_fmip_active(self):
        self.assertTrue(self.product.fmip_is_active)


class TestLocalWarrantyFunctions(TestCase):
    def setUp(self):
        self.data = parse('tests/fixtures/warranty_status.xml',
                          'warrantyDetailInfo')

    def test_product_type(self):
        product = Product('DGKFL06JDHJP')
        product.description='MacBook Pro (17-inch, Mid 2009)'
        self.assertTrue(product.is_mac)
        product.description='iMac (27-inch, Late 2013)'
        self.assertTrue(product.is_mac)
        product.description='iPhone 5'
        self.assertTrue(product.is_iphone)
        product.description = 'iPad 2 3G'
        self.assertTrue(product.is_ipad)
        self.assertTrue(product.is_ios)

    def test_purchase_date(self):
        self.assertIsInstance(self.data.estimatedPurchaseDate, date)

    def test_config_description(self):
        self.assertEqual(self.data.configDescription, 'IPHONE 4,16GB BLACK')

    def test_limited_warranty(self):
        self.assertTrue(self.data.limitedWarranty)

    def test_parts_covered(self):
        self.assertIsInstance(self.data.partCovered, bool)
        self.assertTrue(self.data.partCovered)


class TestRepairDiagnostics(RemoteTestCase):
    def setUp(self):
        super(TestRepairDiagnostics, self).setUp()
        self.results = diagnostics.Diagnostics(serialNumber=env['GSX_SN']).fetch()

    def test_diag_result(self):
        self.assertEqual(self.results.eventHeader.serialNumber, env['GSX_SN'])

    def test_result_timestamp(self):
        ts = gsx_diags_timestamp(self.results.eventHeader.startTimeStamp)
        self.assertIsInstance(ts, datetime)


class TestIosDiagnostics(TestCase):
    def setUp(self):
        self.data = parse('tests/fixtures/ios_diagnostics.xml',
                          'lookupResponseData')

    def test_sn(self):
        self.assertEqual(self.data.diagnosticTestData.testContext.serialNumber,
                         "XXXXXXXXXXXX")

    def test_result(self):
        data = self.data.diagnosticTestData.testResult
        for i in data.result:
            logging.debug("%s: %s" % (i.name, i.value))

        self.assertEqual(data.result[1].name, "FULLY_CHARGED")

    def test_profile(self):
        data = self.data.diagnosticProfileData.profile
        for i in data.unit.key:
            logging.debug("%s: %s" % (i.name, i.value))

        self.assertEqual(data.unit.key[1].value, "fliPhone")

    def test_report(self):
        data = self.data.diagnosticProfileData.report
        for i in data.reportData.key:
            logging.debug("%s: %s" % (i.name, i.value))

        self.assertEqual(data.reportData.key[0].name, "LAST_USAGE_LENGTH")


class TestOnsiteCoverage(RemoteTestCase):
    def setUp(self):
        super(TestOnsiteCoverage, self).setUp()
        self.product = Product(env['GSX_SN'])
        self.product.warranty()

    def test_has_onsite(self):
        self.assertTrue(self.product.has_onsite)

    def test_coverage(self):
        self.assertTrue(self.product.parts_and_labor_covered)

    def test_is_vintage(self):
        self.assertFalse(self.product.is_vintage)


class TestActivation(TestCase):
    def setUp(self):
        self.data = parse('tests/fixtures/ios_activation.xml',
                          'activationDetailsInfo')

    def test_unlock_date(self):
        self.assertIsInstance(self.data.unlockDate, date)

    def test_unlocked(self):
        self.assertIs(type(self.data.unlocked), bool)
        self.assertTrue(self.data.unlocked)

        p = Product(env['GSX_SN'])
        self.assertTrue(p.is_unlocked(self.data))

    def test_imei(self):
        self.assertEqual(self.data.imeiNumber, '010648001526755')


class TestPartsLookup(TestCase):
    def setUp(self):
        self.data = parse('tests/fixtures/parts_lookup.xml',
                          'PartsLookupResponse')
        self.part = self.data.parts[0]

    def test_parts(self):
        self.assertEqual(len(self.data.parts), 3)

    def test_exchange_price(self):
        self.assertEqual(self.part.exchangePrice, 14.4)

    def test_stock_price(self):
        self.assertEqual(self.part.stockPrice, 17.1)

    def test_serialized(self):
        self.assertIsInstance(self.part.isSerialized, bool)
        self.assertTrue(self.part.isSerialized)

    def test_description(self):
        self.assertEqual(self.part.partDescription, 'SVC,REMOTE')


class TestOnsiteDispatchDetail(TestCase):
    def setUp(self):
        self.data = parse('tests/fixtures/onsite_dispatch_detail.xml',
                          'onsiteDispatchDetails')

    def test_details(self):
        self.assertEqual(self.data.dispatchId, 'G101260028')

    def test_address(self):
        self.assertEqual(self.data.primaryAddress.zipCode, 85024)
        self.assertEqual(self.data.primaryAddress.firstName, 'Christopher')

    def test_orderlines(self):
        self.assertIsInstance(self.data.dispatchOrderLines.isSerialized, bool)


class TestRepairUpdate(RemoteTestCase):
    def setUp(self):
        super(TestRepairUpdate, self).setUp()
        self.dispatchId = 'G135934345'
        self.repair = repairs.CarryInRepair(self.dispatchId)

    def test_set_repair_status(self):
        result = self.repair.set_status('BEGR')
        self.assertEqual(result.confirmationNumber, self.dispatchId)

    def test_set_repair_techid(self):
        result = self.repair.set_techid('XXXXX')
        self.assertEqual(result.confirmationNumber, self.dispatchId)


class TestCarryinRepairDetail(TestCase):
    def setUp(self):
        self.data = parse('tests/fixtures/repair_details_ca.xml',
                          'lookupResponseData')

    def test_details(self):
        self.assertEqual(self.data.dispatchId, 'G2093174681')

    def test_unicode_name(self):
        self.assertEqual(self.data.primaryAddress.firstName, u'Ääkköset')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
