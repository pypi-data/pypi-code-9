##############################################################################
#
# Copyright (c) 2011 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id:$
"""
__docformat__ = "reStructuredText"

import collections
import datetime
import threading
import pytz

import maxminddb

import zope.interface

from p01.geo import interfaces

import os.path

loaded_locator = None


def get_loaded_locator(db=None):
    """Return a GeoLocator with the DBs loaded"""
    global loaded_locator
    if loaded_locator is None:
        basepath = os.path.join(os.path.dirname(__file__), 'data')
        db = db or os.path.join(basepath, 'GeoLite2-City.mmdb')
        loaded_locator = GeoLocator(db)
    return loaded_locator


class GeoData(object):
    """GeoLocator data

    The database returns the following data for the city database.

    Note: we will use the country data which represents: A JSON object
    containing details about the country where MaxMind believes the end user
    is located.

    The registered_country describes the following: A JSON object containing
    details about the country in which the ISP has registered the IP address.


    We will get the following data for the ip address: 86.101.28.131

    {
        "country": {
            "geoname_id": 719819,
            "iso_code": "HU",
            "names": {
                "ru": "\u0412\u0435\u043d\u0433\u0440\u0438\u044f",
                "fr": "Hongrie",
                "en": "Hungary",
                "de": "Ungarn",
                "zh-CN": "\u5308\u7259\u5229",
                "pt-BR": "Hungria",
                "ja": "\u30cf\u30f3\u30ac\u30ea\u30fc\u5171\u548c\u56fd",
                "es": "Hungr\u00eda"
            }
        },
        "registered_country": {
            "geoname_id": 719819,
            "iso_code": "HU",
            "names": {
                "ru": "\u0412\u0435\u043d\u0433\u0440\u0438\u044f",
                "fr": "Hongrie",
                "en": "Hungary",
                "de": "Ungarn",
                "zh-CN": "\u5308\u7259\u5229",
                "pt-BR": "Hungria",
                "ja": "\u30cf\u30f3\u30ac\u30ea\u30fc\u5171\u548c\u56fd",
                "es": "Hungr\u00eda"
            }
        },
        "continent": {
            "geoname_id": 6255148,
            "code": "EU",
            "names": {
                "ru": "\u0415\u0432\u0440\u043e\u043f\u0430",
                "fr": "Europe",
                "en": "Europe",
                "de": "Europa",
                "zh-CN": "\u6b27\u6d32",
                "pt-BR": "Europa",
                "ja": "\u30e8\u30fc\u30ed\u30c3\u30d1",
                "es": "Europa"
            }
        },
        "location": {
            "latitude": 47.4925,
            "time_zone": "Europe/Budapest",
            "longitude": 19.0514
        }
    }

    or we will get a bit more data for the ip 128.101.101.101:

    {
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

    """

    __slots__ = [
        'ip',
        'continent',
        'countryCode',
        'countryName',
        'countryGeoName',
        'metroCode',
        'city',
        'cityGeoName',
        'tzName',
        'timezone',
        'longitude',
        'latitude',
        'postalCode',
    ]

    zope.interface.implements(interfaces.IGeoData)

    def getName(self, data):
        try:
            return data['names']['en'] or None
        except KeyError:
            return None

    def __init__(self, ip, data):
        self.ip = ip
        # continent
        continent = data.get('continent', {})
        self.continent = continent.get('code')
        # country
        country = data.get('country', {})
        self.countryCode = country.get('iso_code')
        self.countryName = self.getName(country)
        self.countryGeoName = country.get('geoname_id')
        # city
        city = data.get('city', {})
        self.city = self.getName(city)
        self.cityGeoName = city.get('geoname_id')
        # postal
        self.postalCode = data.get('postal', {}).get('code')
        # location
        location = data.get('location', {})
        self.metroCode = location.get('metro_code')
        self.longitude = location.get('longitude')
        self.latitude = location.get('latitude')
        # timezone
        self.tzName = location.get('time_zone')
        if self.tzName is not None:
            self.timezone = pytz.timezone(self.tzName)
        else:
            self.timezone = None

    def __repr__(self):
        return '<%s for %s>' %(self.__class__.__name__, self.ip)


class CacheExpire(object):
    """Cache with timeout (NOT thread safe)"""

    zope.interface.implements(interfaces.IGeoCache)

    TIMEOUT = datetime.timedelta(days=1)

    def __init__(self):
        self.data = {}

    def lookup(self, key):
        try:
            value, expires = self.data[key]
            if expires > datetime.datetime.now():
                return value
            else:
                self.invalidate(key)
                return None
        except KeyError:
            return None

    def put(self, key, value):
        expires = datetime.datetime.now() + self.TIMEOUT
        self.data[key] = (value, expires)

    def invalidate(self, key):
        try:
            del self.data[key]
        except:
            pass

    def clear(self):
        self.data.clear()


class CacheForever(object):
    """Simple cache forever (NOT thread safe)"""

    zope.interface.implements(interfaces.IGeoCache)

    def __init__(self):
        self.data = {}

    def lookup(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None

    def put(self, key, value):
        self.data[key] = value

    def invalidate(self, key):
        try:
            del self.data[key]
        except:
            pass

    def clear(self):
        self.data.clear()


class MaxItemCache(object):
    """Cache with max items invalidating latest items (thread safe)"""

    zope.interface.implements(interfaces.IGeoCache)

    def __init__(self, maxitems=100000):
        self.data = collections.OrderedDict()
        self.lock = threading.RLock()
        self.maxitems = maxitems

    def __len__(self):
        with self.lock:
            return len(self.data)

    def lookup(self, key):
        with self.lock:
            try:
                return self.data[key]
            except KeyError:
                return None

    def put(self, key, value):
        with self.lock:
            if 0 < self.maxitems == len(self.data):
                self.data.popitem(last=False)
            self.data[key] = value

    def invalidate(self, key):
        with self.lock:
            try:
                del self.data[key]
            except:
                pass

    def clear(self):
        with self.lock:
            self.data.clear()


class GeoLocator(object):
    """GeoLocator instance

    {
        "country": {
            "geoname_id": 719819,
            "iso_code": "HU",
            "names": {
                "ru": "\u0412\u0435\u043d\u0433\u0440\u0438\u044f",
                "fr": "Hongrie",
                "en": "Hungary",
                "de": "Ungarn",
                "zh-CN": "\u5308\u7259\u5229",
                "pt-BR": "Hungria",
                "ja": "\u30cf\u30f3\u30ac\u30ea\u30fc\u5171\u548c\u56fd",
                "es": "Hungr\u00eda"
            }
        },
        "registered_country": {
            "geoname_id": 719819,
            "iso_code": "HU",
            "names": {
                "ru": "\u0412\u0435\u043d\u0433\u0440\u0438\u044f",
                "fr": "Hongrie",
                "en": "Hungary",
                "de": "Ungarn",
                "zh-CN": "\u5308\u7259\u5229",
                "pt-BR": "Hungria",
                "ja": "\u30cf\u30f3\u30ac\u30ea\u30fc\u5171\u548c\u56fd",
                "es": "Hungr\u00eda"
            }
        },
        "continent": {
            "geoname_id": 6255148,
            "code": "EU",
            "names": {
                "ru": "\u0415\u0432\u0440\u043e\u043f\u0430",
                "fr": "Europe",
                "en": "Europe",
                "de": "Europa",
                "zh-CN": "\u6b27\u6d32",
                "pt-BR": "Europa",
                "ja": "\u30e8\u30fc\u30ed\u30c3\u30d1",
                "es": "Europa"
            }
        },
        "location": {
            "latitude": 47.4925,
            "time_zone": "Europe/Budapest",
            "longitude": 19.0514
        }
    }


    """

    zope.interface.implements(interfaces.IGeoLocator)

    def __init__(self, DBpath, mode=maxminddb.MODE_AUTO, cache=None):
        # load geo locator data
        self.reader = maxminddb.open_database(DBpath, mode)
        if cache is None:
            cache = CacheForever()
        self.cache = cache

    def getData(self, ip):
        """Return an instance of IGeoData based on IP address"""
        obj = self.cache.lookup(ip)
        if obj is None:
            try:
                data = self.reader.get(ip)
                obj = GeoData(ip, data)
            except (AttributeError, TypeError, ValueError):
                obj = None
            self.cache.put(ip, obj)
        return obj

    def getTimeZone(self, ip):
        """Return a pytz timezone based on IP address"""
        try:
            return self.cache.lookup(ip).timezone
        except AttributeError:
            return None
