##############################################################################
#
# Copyright (c) 2011 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
$Id:$
"""

import os.path
import doctest
import unittest

from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass

import p01.geo.locator
import p01.geo.testing
from p01.geo import interfaces

###############################################################################
#
# TestCase
#
###############################################################################
marker_pos = object()
marker_kws = object()


class SimpleTestCase(unittest.TestCase):

    iface = None
    klass = None
    pos = marker_pos
    kws = marker_kws

    def getTestInterface(self):
        if self.iface is not None:
            return self.iface

        msg = 'Subclasses has to implement getTestInterface()'
        raise NotImplementedError(msg)

    def getTestClass(self):
        if self.klass is not None:
            return self.klass

        raise NotImplementedError('Subclasses has to implement getTestClass()')

    def getTestPos(self):
        return self.pos

    def getTestKws(self):
        return self.kws

    def makeTestObject(self, object=None, *pos, **kws):
        # provide default positional or keyword arguments
        ourpos = self.getTestPos()
        if ourpos is not marker_pos and not pos:
            pos = ourpos

        ourkws = self.getTestKws()
        if ourkws is not marker_kws and not kws:
            kws = ourkws

        testclass = self.getTestClass()

        if object is None:
            # a class instance itself is the object to be tested.
            return testclass(*pos, **kws)
        else:
            # an adapted instance is the object to be tested.
            return testclass(object, *pos, **kws)

    def test_verifyClass(self):
        # class test
        self.assert_(verifyClass(self.getTestInterface(), self.getTestClass()))

    def test_verifyObject(self):
        # object test
        self.assert_(verifyObject(self.getTestInterface(),
            self.makeTestObject()))


GEO_DATA =     {
        "city": {
            "geoname_id": 5037649,
            "names": {
                "ru": "\u041c\u0438\u043d\u043d\u0435\u0430\u043f\u043e\u043b\u0438\u0441",
                "fr": "Minneapolis",
                "en": "Minneapolis",
                "de": "Minneapolis",
                "zh-CN": "\u660e\u5c3c\u963f\u6ce2\u5229\u65af",
                "pt-BR": "Minneapolis",
                "ja": "\u30df\u30cd\u30a2\u30dd\u30ea\u30b9",
                "es": "Mine\u00e1polis"
            }
        },
        "country": {
            "geoname_id": 6252001,
            "iso_code": "US",
            "names": {
                "ru": "\u0421\u0448\u0430",
                "fr": "\u00c9tats-Unis",
                "en": "United States",
                "de": "USA",
                "zh-CN": "\u7f8e\u56fd",
                "pt-BR": "Estados Unidos",
                "ja": "\u30a2\u30e1\u30ea\u30ab\u5408\u8846\u56fd",
                "es": "Estados Unidos"
            }
        },
        "registered_country": {
            "geoname_id": 6252001,
            "iso_code": "US",
            "names": {
                "ru": "\u0421\u0448\u0430",
                "fr": "\u00c9tats-Unis",
                "en": "United States",
                "de": "USA",
                "zh-CN": "\u7f8e\u56fd",
                "pt-BR": "Estados Unidos",
                "ja": "\u30a2\u30e1\u30ea\u30ab\u5408\u8846\u56fd",
                "es": "Estados Unidos"
            }
        },
        "subdivisions": [
            {
                "geoname_id": 5037779,
                "iso_code": "MN",
                "names": {
                    "ru": "\u041c\u0438\u043d\u043d\u0435\u0441\u043e\u0442\u0430",
                    "en": "Minnesota",
                    "ja": "\u30df\u30cd\u30bd\u30bf\u5dde",
                    "es": "Minnesota"
                }
            }
        ],
        "location": {
            "latitude": 44.9759,
            "time_zone": "America/Chicago",
            "longitude": -93.2166,
            "metro_code": 613
        },
        "postal": {
            "code": "55414"
        },
        "continent": {
            "geoname_id": 6255149,
            "code": "NA",
            "names": {
                "ru": "\u0421\u0435\u0432\u0435\u0440\u043d\u0430\u044f \u0410\u043c\u0435\u0440\u0438\u043a\u0430",
                "fr": "Am\u00e9rique du Nord",
                "en": "North America",
                "de": "Nordamerika",
                "zh-CN": "\u5317\u7f8e\u6d32",
                "pt-BR": "Am\u00e9rica do Norte",
                "ja": "\u5317\u30a2\u30e1\u30ea\u30ab",
                "es": "Norteam\u00e9rica"
            }
        }
    }


class GeoDataTest(SimpleTestCase):

    def getTestInterface(self):
        return interfaces.IGeoData

    def getTestClass(self):
        return p01.geo.locator.GeoData

    def getTestKws(self):
        return {'ip': '128.101.101.101', 'data': GEO_DATA}



class CacheExpireTest(SimpleTestCase):

    def getTestInterface(self):
        return interfaces.IGeoCache

    def getTestClass(self):
        return p01.geo.locator.CacheExpire


class CacheForeverTest(SimpleTestCase):

    def getTestInterface(self):
        return interfaces.IGeoCache

    def getTestClass(self):
        return p01.geo.locator.CacheForever


class MaxItemCacheTest(SimpleTestCase):

    def getTestInterface(self):
        return interfaces.IGeoCache

    def getTestClass(self):
        return p01.geo.locator.MaxItemCache

    def getTestKws(self):
        return {'maxitems': 10}

    def test_maxitems(self):
        obj = self.makeTestObject()
        self.assert_(obj.maxitems, 10)


class GeoLocatorTest(SimpleTestCase):

    def getTestInterface(self):
        return interfaces.IGeoLocator

    def getTestClass(self):
        return p01.geo.locator.GeoLocator

    def getTestPos(self):
        path = os.path.join(os.path.dirname(p01.geo.__file__), 'data',
            'GeoLite2-City.mmdb')
        return (path,)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(GeoDataTest),
        unittest.makeSuite(CacheExpireTest),
        unittest.makeSuite(CacheForeverTest),
        unittest.makeSuite(MaxItemCacheTest),
        unittest.makeSuite(GeoLocatorTest),
        doctest.DocFileSuite(
            'README.txt',
            setUp=p01.geo.testing.setUp, tearDown=p01.geo.testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        doctest.DocFileSuite(
            'performance.txt',
            setUp=p01.geo.testing.setUp, tearDown=p01.geo.testing.tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        ))


if __name__ == '__main__':
    unittest.main()