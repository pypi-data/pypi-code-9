# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""cubicweb-skos unit tests for hooks"""

from cubicweb.devtools.testlib import CubicWebTC


class HooksTC(CubicWebTC):

    def test_externaluri_to_concept(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'preexisting')
            concept = scheme.add_concept(u'something', cwuri=u'http://data.bnf.fr/ark:/12148/cb11934798x')
            exturi = cnx.create_entity('ExternalUri', cwuri=u'http://someuri/someobject',
                                       uri=u'http://someuri/someobject',
                                       exact_match=concept)
            cnx.commit()
            # now insert a concept with the external uri as cwuri
            scheme = cnx.create_entity('ConceptScheme')
            new_concept = scheme.add_concept(u'some object', cwuri=u'http://someuri/someobject')
            cnx.commit()
            # ensure the external uri has been replaced by the concept and deleted
            concept.cw_clear_all_caches()
            self.assertEqual(concept.exact_match[0].eid, new_concept.eid)
            self.failIf(cnx.execute('Any X WHERE X eid %(x)s', {'x': exturi.eid}))

    def test_skos_source(self):
        with self.admin_access.repo_cnx() as cnx:
            skos = cnx.create_entity('SKOSSource', name=u'a source', url=u'http://skos.org\nhttp://skos.net')
            cnx.commit()
            source = cnx.find('CWSource', name=u'a source').one()
            self.assertEqual(source.url, u'http://skos.org\nhttp://skos.net')
            skos.cw_set(name=u'new name', url=u'http://skos.com')
            self.assertEqual(source.name, u'new name')
            self.assertEqual(source.url, u'http://skos.com')
