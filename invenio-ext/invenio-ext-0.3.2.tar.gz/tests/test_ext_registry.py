# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Test unit for the miscutil/mailutils module.
"""

from __future__ import absolute_import

from flask_registry import ImportPathRegistry, RegistryError

from invenio_ext.registry import DictModuleAutoDiscoverySubRegistry
from invenio_testing import InvenioTestCase


class TestDictModuleAutoDiscoverySubRegistry(InvenioTestCase):
    def test_registration(self):
        r = self.app.extensions['registry']

        r['testpkgs'] = ImportPathRegistry(
            initial=['apps']
        )
        assert len(r['testpkgs']) == 1

        r['myns'] = \
            DictModuleAutoDiscoverySubRegistry(
                'last',
                keygetter=lambda k, v, new_v: k if k else v.__name__,
                app=self.app,
                registry_namespace='testpkgs'
            )
        assert len(r['myns']) == 1

        from apps.last import views
        assert r['myns']['apps.last.views'] == \
            views

        self.assertRaises(
            RegistryError,
            DictModuleAutoDiscoverySubRegistry,
            'last',
            app=self.app,
            registry_namespace='testpkgs'
        )

        # Register simple object
        class TestObject(object):
            pass

        r['myns'].register(TestObject)

        # Identical keys raises RegistryError
        self.assertRaises(
            RegistryError,
            r['myns'].register,
            TestObject
        )

        r['myns'].unregister('TestObject')
        assert 'TestObject' not in r['myns']

        r['myns']['mykey'] = TestObject
        assert TestObject == r['myns']['mykey']

        assert len(r['myns'].items()) == 2
