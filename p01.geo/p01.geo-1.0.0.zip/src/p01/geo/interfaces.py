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

import zope.interface
import zope.schema


class IGeoData(zope.interface.Interface):
    """GeoLocator"""

    ip = zope.schema.TextLine(title=u"IP address")
    # continent
    continent = zope.schema.TextLine(title=u"Continent")
    # country
    countryCode = zope.schema.TextLine(title=u"Country code")
    countryName = zope.schema.TextLine(title=u"Country name")
    countryGeoName = zope.schema.TextLine(title=u"Country geo name")
    # postal
    postalCode = zope.schema.TextLine(title=u"Postal code")
    # city
    city = zope.schema.TextLine(title=u"City")
    cityGeoName = zope.schema.TextLine(title=u"City geo name")
    # location
    metroCode = zope.schema.TextLine(title=u"Metro code")
    longitude = zope.schema.Float(title=u"Longitude")
    latitude = zope.schema.Float(title=u"Latitude")
    # timezone
    tzName = zope.interface.Attribute("Timezone name")
    timezone = zope.interface.Attribute("pytz timezone")


class IGeoCache(zope.interface.Interface):
    """GeoData cache API"""

    def lookup(key):
        """Lookup GeoData by ip address as key"""

    def put(key, value):
        """Add GeoData by ip address as key"""

    def invalidate(key):
        """Invalidate GeoData by ip address as key"""

    def clear():
        """Remove all GeoData items from cache"""


class IGeoLocator(zope.interface.Interface):
    """GeoLocator, all lookup values are cached"""

    def getTimeZone(ip):
        """Return a pytz timezone based on IP address"""

    def getData(ip):
        """Return an instance of IGeoData based on IP address"""