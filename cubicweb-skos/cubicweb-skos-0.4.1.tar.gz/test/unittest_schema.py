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

"""cubicweb-skos sobjects tests"""

from yams import ValidationError

from cubicweb import Unauthorized
from cubicweb.devtools.testlib import CubicWebTC


class SKOSSchemaTC(CubicWebTC):

    def test_concept_unique_pref_label_language(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'scheme')
            concept = scheme.add_concept(u'un concept', language_code=u'fr')
            with self.assertRaises(ValidationError) as cm:
                cnx.create_entity('Label', label=u'le concept', language_code=u'fr',
                                  pref_label_of=concept)
        self.assertEqual(cm.exception.errors,
                         {'': u'a preferred label in "%(lang)s" language already exists',
                          'language_code': u'please use another language code'})

    def test_concept_label_unique(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'scheme')
            concept = scheme.add_concept(u'a concept', language_code=u'en')
            concept.pref_label[0].cw_set(alt_label_of=concept)
            with self.assertRaises(ValidationError) as cm:
                cnx.commit()
        self.assertEqual(cm.exception.errors,
                         {'pref_label_of-subject': "can't apply twice a label on a concept"})

    def test_concept_label_no_language(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'scheme')
            concept = scheme.add_concept(u'a concept', language_code=None)
            cnx.commit()
            concept.cw_clear_all_caches()
            self.assertEqual(concept.labels, {None: 'a concept'})
            self.assertEqual(concept.label(), 'a concept')

    def test_scheme_no_title(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme')
            cnx.commit()
            # title default to cwuri
            self.assertEqual(scheme.dc_title(), 'http://testing.fr/cubicweb/%s' % scheme.eid)

    def test_concept_multiple_schemes(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme1 = cnx.create_entity('ConceptScheme', title=u'some scheme')
            concept = scheme1.add_concept(u'a concept', language_code=u'en')
            scheme2 = cnx.create_entity('ConceptScheme', title=u'some other scheme')
            concept.cw_set(in_scheme=scheme2)
            cnx.commit()
            self.assertEqual(set(x.eid for x in concept.in_scheme),
                             set([scheme1.eid, scheme2.eid]))
            # "scheme" property picks a scheme randomly, as we don't want to clutter the code for
            # this peculiarity (do we?)
            self.assertIn(concept.scheme.eid, [scheme1.eid, scheme2.eid])

    def test_concept_multiple_parents(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'some scheme')
            concept1 = scheme.add_concept(u'a concept', language_code=u'en')
            concept2 = scheme.add_concept(u'another concept', language_code=u'en')
            subconcept = concept1.add_concept(u'a sub-concept', language_code=u'en')
            subconcept.cw_set(broader_concept=concept2)
            cnx.commit()
            self.assertEqual(set(x.eid for x in subconcept.broader_concept),
                             set([concept1.eid, concept2.eid]))
            # "parent_concept" property picks a scheme randomly, as we don't want to clutter the
            # code for this peculiarity (do we?)
            self.assertIn(subconcept.parent_concept.eid, [concept1.eid, concept2.eid])

    def test_in_scheme_permissions(self):
        with self.admin_access.repo_cnx() as cnx:
            url = u'file://%s' % self.datapath('siaf_matieres_shortened.xml')
            cnx.create_entity('CWSource', name=u'mythesaurus',
                              type=u'datafeed', parser=u'rdf.skos', url=url)
            cnx.commit()
            dfsource = self.repo.sources_by_uri[u'mythesaurus']
            with self.repo.internal_cnx() as icnx:
                stats = dfsource.pull_data(icnx, force=True, raise_on_error=False)
            assert stats['created']
            scheme = cnx.find('ConceptScheme').one()
            with self.assertRaises(Unauthorized) as cm:
                cnx.execute('DELETE X in_scheme S WHERE X is Concept, '
                            'S cw_source SO, SO name "mythesaurus"')
                cnx.commit()
            cnx.rollback()
            self.assertEqual(cm.exception.args,
                             ('delete', 'relation Concept in_scheme ConceptScheme'))
            with self.assertRaises(Unauthorized) as cm:
                cnx.create_entity('Concept', in_scheme=scheme)
                cnx.commit()
            cnx.rollback()
            self.assertEqual(cm.exception.args,
                             ('add', 'relation Concept in_scheme ConceptScheme'))


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
