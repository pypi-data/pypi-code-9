# copyright 2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement
from cubicweb.utils import UStringIO
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.web.component import EmptyComponent


class ConfRegistrationComponentTC(CubicWebTC):
    regid = 'confregistrationbox'

    def create_conf(self, cnx, reg_open=True):
        pa = cnx.create_entity('PostalAddress',
                               street=u"ma rue",
                               postalcode=u"42",
                               city=u'ma ville')
        conf = cnx.create_entity('Conference', title=u"my conf",
                                 reg_open=reg_open, take_place_at=pa)
        cnx.commit()
        return conf

    def setUp(self):
        super(ConfRegistrationComponentTC, self).setUp()

    def test_boolean_field(self):
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(len(cnx.execute('Any C WHERE C is Conference')), 0)
            pa = cnx.create_entity('PostalAddress',
                                   street=u"ma rue",
                                   postalcode=u"42",
                                   city=u'ma ville')
            conf = cnx.create_entity('Conference', title=u"my conf",
                                     reg_open=True, take_place_at=pa)
            cnx.commit()
            self.assertEqual(len(cnx.execute('Any C WHERE C is Conference, C reg_open True')), 1)

    def test_create_conf(self):
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(len(cnx.execute('Any C WHERE C is Conference')), 0)
            conf = self.create_conf(cnx)
            self.assertTrue(conf.reg_open)
            self.assertEqual(len(cnx.execute('Any C WHERE C is Conference, C reg_open True')), 1)
            self.assertEqual(conf.take_place_at[0].street, u"ma rue")
            conf = self.create_conf(cnx, reg_open=False)
            self.assertEqual(len(cnx.execute('Any C WHERE C is Conference, C reg_open False')), 1)
            self.assertFalse(conf.reg_open)
            self.assertEqual(len(cnx.execute('Any C WHERE C is Conference')), 2)

    def test_no_open_registration(self):
        with self.admin_access.web_request() as req:
            component = self.vreg['ctxcomponents'].select(self.regid, req)
            self.assertEqual(component.context, "left")
            self.assertRaises(EmptyComponent, component.init_rendering)
            self.create_conf(req.cnx, reg_open=False)
            self.assertRaises(EmptyComponent, component.init_rendering)

    def test_anonymous_session(self):
        with self.admin_access.repo_cnx() as cnx:
            self.create_conf(cnx)

        with self.new_access('anon').web_request() as req:
            self.assertTrue(req.session.anonymous_session)
            component = self.vreg['ctxcomponents'].select(self.regid, req)
            component.init_rendering()
            label = component.render_body(UStringIO)
        self.assertEqual(label, _('Register now for the conference !'))

    def test_items_not_found(self):
        with self.admin_access.repo_cnx() as cnx:
            self.create_conf(cnx)

        with self.admin_access.web_request() as req:
            component = self.vreg['ctxcomponents'].select(self.regid, req)
            component.init_rendering()
            label = component.render_body(UStringIO)
        self.assertEqual(label, _('Register now for the conference !'))

    def test_items_found_and_cart_is_checked_out(self):
        with self.admin_access.repo_cnx() as cnx:
            self.create_conf(cnx)

        you_are_registered = _('You are registered for the conference')
        self.skipTest(you_are_registered)

    def test_items_found_and_cart_not_checked_out(self):
        with self.admin_access.repo_cnx() as cnx:
            self.create_conf(cnx)

        pay_to_confirm = _('Pay now to confirm your registration !')
        self.skipTest(pay_to_confirm)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
