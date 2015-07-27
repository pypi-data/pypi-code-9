# -*- coding: utf-8 -*-
#
# copyright 2014-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of cwclientlib.
#
# cwclientlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# cwclientlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with cwclientlib. If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO
import unittest

from cwclientlib.cwproxy import CWProxy, SignedRequestAuth

try:
    from cubicweb.devtools.httptest import CubicWebServerTC
except ImportError:
    CubicWebServerTC = object  # make this module importable

__docformat__ = "restructuredtext en"


def setUpModules():
    if CubicWebServerTC is object:
        raise unittest.SkipTest('cubicweb is missing')


class CWProxyClientTC(CubicWebServerTC):
    '''Basic tests for CWProxy'''
    def setup_database(self):
        with self.admin_access.client_cnx() as cnx:
            token = cnx.create_entity('AuthToken', id=u'simulagora',
                                      enabled=True,
                                      token_for_user=cnx.user.eid)
            self.admineid = cnx.user.eid
            cnx.commit()
            auth = SignedRequestAuth(token_id=token.id,
                                     secret=token.token)
            self.client = CWProxy(base_url=cnx.base_url(),
                                  auth=auth)

    def test_rql(self):
        self.assertEqual([['admin'], ['anon']],
                         self.client.rql('Any L WHERE U login L').json())

        self.assertEqual([[self.admineid]],
                         self.client.rql('Any U WHERE U login "admin"').json())

    def test_execute(self):
        self.assertEqual([[self.admineid]],
                         self.client.execute('Any U WHERE U login %(l)s',
                                             {'l': 'admin'}))

    def test_rql_vid(self):
        admin = self.client.rql('Any U WHERE U login "admin"',
                                vid='ejsonexport').json()[0]
        self.assertIn('login', admin.keys())

    def test_rql_path(self):
        result = self.client.rql('Any U WHERE U login "admin"',
                                 path='test-controller').text
        self.assertEqual("coucou", result)

    def test_bad_rql_path(self):
        result = self.client.rql('CWGroup U WHERE U login "admin"')
        self.assertEqual(result.status_code, 500)

    def test_rqlio(self):
        queries = [('INSERT CWUser U: U login %(login)s, U upassword %(pw)s',
                    {'login': 'babar', 'pw': 'cubicweb rulez & 42'}),
                   ('INSERT CWGroup G: G name %(name)s',
                    {'name': 'pachyderms'}),
                   ('SET U in_group G WHERE G eid %(g)s, U eid %(u)s',
                    {'u': '__r0', 'g': '__r1'}),
                   ]

        results = self.client.rqlio(queries).json()
        self.assertEqual(3, len(results))
        babar = results[0][0][0]
        pach = results[1][0][0]

        with self.admin_access.client_cnx() as cnx:
            users = cnx.find('CWUser', eid=babar)
            self.assertEqual(1, len(users))
            self.assertEqual('babar', users.one().login)

            groups = cnx.find('CWGroup', eid=pach)
            self.assertEqual(1, len(groups))
            self.assertEqual('pachyderms', groups.one().name)

        self.assertEqual([babar, pach], results[2][0])

    def test_rqlio_no_kwargs(self):
        queries = [('INSERT CWUser U: U login "babar", '
                    'U upassword "cubicweb rulez & 42", '
                    'U in_group G WHERE G name "users"', None),
                   ]
        results = self.client.rqlio(queries).json()
        self.assertEqual(1, len(results))
        babar = results[0][0][0]
        with self.admin_access.client_cnx() as cnx:
            users = cnx.find('CWUser', eid=babar)
            self.assertEqual(1, len(users))
            self.assertEqual('babar', users.one().login)

    def test_rqlio_file(self):
        queries = [('INSERT File F: F data %(content)s, F data_name %(fname)s',
                    {'content': BytesIO('some binary data'),
                     'fname': 'toto.bin'}),
                   ]

        eid = self.client.rqlio(queries).json()[0][0][0]
        with self.admin_access.client_cnx() as cnx:
            file = cnx.entity_from_eid(eid)
            self.assertEqual('toto.bin', file.data_name)
            content = file.data.getvalue()
            self.assertEqual('some binary data', content)


class UtilsTests(unittest.TestCase):

    def test_base_url_slash_normalization(self):
        """test '/' can't appear twice in base_url

        e.g. we don't want ``http://www.logilab.org//``
        nor ``http://www.logilab.org//basepath``
        """
        proxy = CWProxy(base_url='http://www.logilab.org')
        self.assertEqual(proxy.base_url, ('http', 'www.logilab.org'))
        proxy = CWProxy(base_url='http://www.logilab.org/')
        self.assertEqual(proxy.base_url, ('http', 'www.logilab.org'))
        proxy = CWProxy(base_url='http://www.logilab.org/basepath')
        self.assertEqual(proxy.base_url, ('http', 'www.logilab.org/basepath'))
        proxy = CWProxy(base_url='http://www.logilab.org/basepath/')
        self.assertEqual(proxy.base_url, ('http', 'www.logilab.org/basepath'))

    def test_base_url_absolute_url(self):
        """test CWProxy.build_url parsing of absolute URLs
        """
        proxy = CWProxy(base_url='http://www.logilab.org')
        for url in ('http://www.logilab.org',
                    'http://www.logilab.org/path/to',
                    'http://www.logilab.org/path/to/',):
            self.assertEqual(url, proxy.build_url(url))

        proxy = CWProxy(base_url='http://www.logilab.org/with/path/')
        for url in ('http://www.logilab.org/with/path',
                    'http://www.logilab.org/with/path/to/something',
                    'http://www.logilab.org/with/path/to/something/',):
            self.assertEqual(url, proxy.build_url(url))


if __name__ == '__main__':
    from unittest import main
    main()
