# -*- coding: utf-8 -*-
#
# Copyright (c) nexiles GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'


import unittest

# http://readthedocs.org/docs/nose/en/latest/testing_tools.html
from nose import tools as nt

from nexiles.tools.api.tree import Tree


class TestTree(unittest.TestCase):

    def test_tree(self):
        tree = Tree()
        tree["root"]["child1"] = 1
        tree["root"]["child2"] = 1
        self.assertTrue("root" in tree)
        self.assertTrue("child1" in tree["root"])
        self.assertTrue("child2" in tree["root"])
        self.assertEquals(sorted(tree.root.keys()), ['child1', 'child2'])

        tree.child1.value = 17
        self.assertEquals(tree.child1, {'value': 17})

    @nt.raises(AttributeError)
    def test_valid_keys_1(self):
        tree = Tree()
        tree._invalid

    @nt.raises(AttributeError)
    def test_valid_keys_2(self):
        tree = Tree()
        tree.foo._bar

    def test_tree_from_dict(self):
        tree = Tree({
            "item": {
                "name": "fred"
                }
        })

        self.assertEquals(tree.item.name, "fred")

    def test_tree_from_dict_2(self):
        d = {u'cadname': u'0000000182.drw', u'name': u'0000000182.drw', u'url': u'http://windchill91.nexiles.com/Windchill/servlet/nexiles/tools/api/1.0/epmdocuments/OR:wt.epm.EPMDocument:100472', u'oid': u'OR:wt.epm.EPMDocument:100472', u'modified': u'2012-05-09T17:38:01', u'number': u'0000000182.DRW', u'item': {u'isExtentsValid': False, u'cadname': u'0000000182.drw', u'isHasPendingChange': None, u'isTopGeneric': False, u'number': u'0000000182.DRW', u'doctype': u'CADDRAWING', u'isLatestIteration': True, u'isMissingDependents': False, u'isTemplated': False, u'isLifeCycleAtGate': False, u'creator': {u'url': u'http://windchill91.nexiles.com/Windchill/servlet/nexiles/tools/api/1.0/users/OR:wt.org.WTUser:10', u'oid': u'OR:wt.org.WTUser:10', u'details': u'http://windchill91.nexiles.com/Windchill/servlet/TypeBasedIncludeServlet?oid=OR:wt.org.WTUser:10&u8=1', u'name': u'Administrator'}, u'state': u'RELEASED', u'isGeneric': False, u'isLocked': False, u'version': u'A.13', u'location': u'/Default', u'isDerived': False, u'modifier': {u'url': u'http://windchill91.nexiles.com/Windchill/servlet/nexiles/tools/api/1.0/users/OR:wt.org.WTUser:10', u'oid': u'OR:wt.org.WTUser:10', u'details': u'http://windchill91.nexiles.com/Windchill/servlet/TypeBasedIncludeServlet?oid=OR:wt.org.WTUser:10&u8=1', u'name': u'Administrator'}, u'thumbnail': '', u'isVerified': True, u'oid': u'OR:wt.epm.EPMDocument:100472', u'isCheckedOut': False, u'isLifeCycleBasic': True, u'path': u'/Default/0000000182.drw', u'isHasVariance': None, u'isPlaceHolder': False, u'isHasContents': False, u'name': u'0000000182.drw', u'created': u'2012-04-19T10:44:55', u'modified': u'2012-05-09T17:38:01', u'locker': None, u'isInheritedDomain': True, u'attributes': [], u'isHasHangingChange': None, u'isInstance': False}, u'version': u'A.13', u'details': u'http://windchill91.nexiles.com/Windchill/servlet/TypeBasedIncludeServlet?oid=OR:wt.epm.EPMDocument:100472&u8=1', u'_runtime': 0.1400001049041748, u'path': u'/Default/0000000182.drw'}
        tree = Tree(d)
        self.assertEquals(tree.cadname, u'0000000182.drw')
        self.assertEquals(tree.item.name, u'0000000182.drw')
        self.assertEquals(tree.item.isLatestIteration, True)

# vim: set ft=python ts=4 sw=4 expandtab :
