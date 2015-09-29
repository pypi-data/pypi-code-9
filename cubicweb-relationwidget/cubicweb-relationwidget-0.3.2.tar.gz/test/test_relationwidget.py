# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-relationwidget automatic tests


uncomment code below if you want to activate automatic test for your cube:

.. sourcecode:: python

    from cubicweb.devtools.testlib import AutomaticWebTest

    class AutomaticWebTest(AutomaticWebTest):
        '''provides `to_test_etypes` and/or `list_startup_views` implementation
        to limit test scope
        '''

        def to_test_etypes(self):
            '''only test views for entities of the returned types'''
            return set(('My', 'Cube', 'Entity', 'Types'))

        def list_startup_views(self):
            '''only test startup views of the returned identifiers'''
            return ('some', 'startup', 'views')
"""

from cubicweb.devtools import testlib
from cubes.relationwidget.views import rset_main_type

class RelationWidgetTC(testlib.CubicWebTC):
    def test_rset_main_type(self):
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute('Any X,N LIMIT 1 WHERE X name N')
            self.assertEqual(rset_main_type(rset), None)
            rset = cnx.execute('Any X,N LIMIT 1 WHERE X name N, X is State')
            self.assertEqual(rset_main_type(rset), 'State')
            rset = cnx.execute('Any LOWER(N),X LIMIT 1 WHERE X name N, X is State')
            self.assertEqual(rset_main_type(rset), None)

    def test_related_entities_table_empty_rset(self):
        with self.admin_access.web_request() as req:
            rset = req.empty_rset()
            self.vreg['views'].select('select_related_entities_table', req, rset=rset)

if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
