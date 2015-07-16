# coding: utf-8
#
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

from itertools import count

from logilab.common.testlib import TestCase, require_module, unittest_main

from cubicweb import devtools # XXX ensure python path is ok
from cubes.skos import ExtEntity
from cubes.skos.rdfio import (RDFRegistryError, RDFRegistry, RDFLibRDFGraph,
                              LibRDFRDFGraph, rdf_graph_to_entities, unicode_with_language as ul)

class UnicodeWithLanguageTC(TestCase):

    def test_comparison_ul_ul(self):
        a = ul('toto', 'fr')
        b = ul('toto', 'fr')
        self.assertEqual(a, b)

        b = ul('toto', 'en')
        self.assertNotEqual(a, b)

        b = ul('titi', 'fr')
        self.assertNotEqual(a, b)

    def test_comparison_ul_and_other(self):
        a = ul('toto', 'fr')
        b = u'toto'
        self.assertNotEqual(a, b)

class RDFRegistryTC(TestCase):
    def setUp(self):
        self.xy = RDFRegistry()
        self.xy.register_prefix('dc', 'http://purl.org/dc/elements/1.1/')
        self.xy.register_prefix('foaf', 'http://xmlns.com/foaf/0.1/')
        self.xy.register_prefix('skos', 'http://www.w3.org/2004/02/skos/core#')

    def test_register_prefix(self):
        xy = self.xy
        self.assertEqual(xy.prefixes['dc'], 'http://purl.org/dc/elements/1.1/')
        # re-registering the same prefix is fine
        xy.register_prefix('dc', 'http://purl.org/dc/elements/1.1/')
        # though re-registering an existing prefix to a different url isn't
        self.assertRaises(RDFRegistryError,
                          xy.register_prefix, 'dc', 'http://purl.org/dc/elements/1.2/')
        # unless we explicitly tell it's ok
        xy.register_prefix('dc', 'http://purl.org/dc/elements/1.2/', overwrite=True)
        self.assertEqual(xy.prefixes['dc'], 'http://purl.org/dc/elements/1.2/')

    def test_register_etype_equivalence(self):
        xy = self.xy
        xy.register_etype_equivalence('CWUser', 'foaf:Person')
        self.assertEqual(xy.etype2rdf['CWUser'], 'http://xmlns.com/foaf/0.1/Person')
        # re-registering the same equivalence is fine
        xy.register_etype_equivalence('CWUser', 'foaf:Person')
        # though re-registering a different isn't
        self.assertRaises(RDFRegistryError,
                          xy.register_etype_equivalence, 'CWUser', 'foaf:Personne')
        # unless we explicitly tell it's ok
        xy.register_etype_equivalence('CWUser', 'foaf:Personne', overwrite=True)
        self.assertEqual(xy.etype2rdf['CWUser'], 'http://xmlns.com/foaf/0.1/Personne')
        xy.register_etype_equivalence('User', 'foaf:Person', overwrite=True)

    def test_register_attribute_equivalence(self):
        xy = self.xy
        xy.register_etype_equivalence('CWUser', 'foaf:Person')
        xy.register_attribute_equivalence('CWUser', 'login', 'dc:title')
        self.assertEqual(xy.attr2rdf[('CWUser', 'login')], 'http://purl.org/dc/elements/1.1/title')
        # re-registering the same equivalence is fine
        xy.register_attribute_equivalence('CWUser', 'login', 'dc:title')
        # though re-registering a different isn't
        self.assertRaises(RDFRegistryError,
                          xy.register_attribute_equivalence, 'CWUser', 'login', 'dc:description')
        # unless we explicitly tell it's ok
        xy.register_attribute_equivalence('CWUser', 'login', 'dc:description', overwrite=True)
        self.assertEqual(xy.attr2rdf[('CWUser', 'login')], 'http://purl.org/dc/elements/1.1/description')

    def test_register_relation_equivalence(self):
        xy = self.xy
        xy.register_etype_equivalence('ConceptScheme', 'skos:ConceptScheme')
        xy.register_etype_equivalence('Concept', 'skos:Concept')
        xy.register_relation_equivalence('Concept', 'in_scheme', 'ConceptScheme', 'skos:inScheme')
        xy.register_relation_equivalence('Concept', 'broader_concept', 'Concept', 'skos:broader')
        self.assertEqual(xy.rel2rdf[('Concept', 'in_scheme', 'ConceptScheme')],
                         set([('http://www.w3.org/2004/02/skos/core#inScheme', False)]))
        xy.register_relation_equivalence('Concept', 'in_scheme', 'ConceptScheme', 'skos:inScheme')
        xy.register_relation_equivalence('Concept', 'in_scheme', 'ConceptScheme', 'skos:inSchema')
        self.assertEqual(xy.rel2rdf[('Concept', 'in_scheme', 'ConceptScheme')],
                        set([('http://www.w3.org/2004/02/skos/core#inScheme', False),
                             ('http://www.w3.org/2004/02/skos/core#inSchema', False)]))
        xy.register_relation_equivalence('Concept', 'broader_concept', 'Concept', 'skos:broader')
        xy.register_relation_equivalence('Concept', 'broader_concept', 'Concept', 'skos:narrower',
                                         reverse=True)
        self.assertEqual(xy.rel2rdf[('Concept', 'broader_concept', 'Concept')],
                         set([('http://www.w3.org/2004/02/skos/core#broader', False),
                              ('http://www.w3.org/2004/02/skos/core#narrower', True)]))

    def test_predicates_for_subject_etype(self):
        xy = self.xy
        xy.register_etype_equivalence('ConceptScheme', 'skos:ConceptScheme')
        xy.register_etype_equivalence('Concept', 'skos:Concept')
        xy.register_attribute_equivalence('ConceptScheme', 'title', 'dc:title')
        xy.register_relation_equivalence('Concept', 'in_scheme', 'ConceptScheme', 'skos:inScheme')
        xy.register_relation_equivalence('Concept', 'broader_concept', 'Concept', 'skos:narrower',
                                         reverse=True)
        self.assertEqual(sorted(xy.predicates_for_subject_etype('ConceptScheme')),
                         [('title', 'http://purl.org/dc/elements/1.1/title', False)])
        self.assertEqual(sorted(xy.predicates_for_subject_etype('Concept')),
                         [('broader_concept', 'http://www.w3.org/2004/02/skos/core#narrower', True),
                          ('in_scheme', 'http://www.w3.org/2004/02/skos/core#inScheme', False)])


def dcf(string):
    return 'http://data.culture.fr/thesaurus/resource/ark:/67717/' + string


def ext_entities_to_dict(ext_entities):
    """Turn a sequence of external entities into a 2-level dict with entity
    type and extid as keys.
    """
    entities_dict = {}
    for extentity in ext_entities:
        entities_dict.setdefault(extentity.etype, {})[extentity.extid] = extentity.values
    return entities_dict


class RDFLibRDFGraphTC(TestCase):

    def test_add(self):
        graph = RDFLibRDFGraph()
        bob = graph.uri("http://example.org/people/Bob")
        knows = graph.uri("http://foaf.com/knows")
        alice = graph.uri("http://example.org/people/Alice")
        firstname = graph.uri("http://foaf.com/firstname")
        age = graph.uri("http://foaf.com/age")
        desc = graph.uri("http://dc.com/description")
        graph.add(bob, knows, alice)
        graph.add(bob, firstname, "bob")
        graph.add(bob, age, 45)
        graph.add(bob, desc, ul("man", "en"))
        graph.add(alice, firstname, "alice")
        graph.add(alice, age, 25)

        result = list(graph.objects(bob, knows))
        self.assertEqual(result, ["http://example.org/people/Alice"])
        result = list(graph.objects(bob, age))
        self.assertEqual(result, [45])
        result = list(graph.objects(bob, desc))
        self.assertEqual(result, [ul("man", "en")])
        result = list(graph.objects(alice, firstname))
        self.assertEqual(result, ["alice"])


class RDFGraphToEntitiesTC(TestCase):

    @require_module('rdflib')
    def test_rdflib(self):
        self._test(RDFLibRDFGraph())

    @require_module('RDF')
    def test_librdf(self):
        self._test(LibRDFRDFGraph())

    def _test(self, graph):
        xy = RDFRegistry()
        xy.register_prefix('dc', 'http://purl.org/dc/elements/1.1/')
        xy.register_prefix('skos', 'http://www.w3.org/2004/02/skos/core#')
        xy.register_etype_equivalence('ConceptScheme', 'skos:ConceptScheme')
        xy.register_etype_equivalence('Concept', 'skos:Concept')
        xy.register_attribute_equivalence('ConceptScheme', 'title', 'dc:title')
        xy.register_relation_equivalence('Concept', 'in_scheme', 'ConceptScheme', 'skos:inScheme')
        xy.register_relation_equivalence('Concept', 'broader_concept', 'Concept', 'skos:broader')
        xy.register_relation_equivalence('Concept', 'broader_concept', 'Concept', 'skos:narrower',
                                         reverse=True)
        xy.register_relation_equivalence('Concept', 'narrower_concept', 'Concept', 'skos:narrower')
        xy.register_relation_equivalence('Concept', 'narrower_concept', 'Concept', 'skos:broader',
                                         reverse=True)
        xy.register_relation_equivalence('Concept', 'related_concept', 'Concept', 'skos:related')
        xy.register_relation_equivalence('Label', 'pref_label_of', 'Concept', 'skos:prefLabel',
                                         reverse=True)
        xy.register_relation_equivalence('Label', 'alt_label_of', 'Concept', 'skos:altLabel',
                                         reverse=True)

        graph.load(self.datapath('siaf_matieres_shortened.xml'))
        id_count = count()

        def build_label(extentity, rtype, uris):
            for label in uris:
                yield ExtEntity('Label', next(id_count),
                                {'label': set([label]),
                                 'language_code': set([label.lang]),
                                 rtype: set([extentity.extid])})

        etypes = ('ConceptScheme', 'Concept')  #, 'Label')
        rcb = {'pref_label_of': build_label,
               'alt_label_of': build_label}
        ext_entities = rdf_graph_to_entities(xy, graph, etypes,
                                             relation_callbacks=rcb)
        e = ext_entities_to_dict(ext_entities)
        self.assertEqual(e['ConceptScheme'][dcf('Matiere')],
                         {'title': set([u"Thésaurus-matières pour l'indexation des archives locales"])})
        pref_labels = [k for k, v in e['Label'].iteritems()
                       if dcf('T1-1073') in v.get('pref_label_of', ())]
        self.assertEqual(len(pref_labels), 1)
        alt_labels = [k for k, v in e['Label'].iteritems()
                      if dcf('T1-1073') in v.get('alt_label_of', ())]
        self.assertEqual(len(alt_labels), 2)
        self.assertEqual(e['Concept'][dcf('T1-1073')],
                         {'broader_concept': set([dcf('T1-3')]),
                          'in_scheme': set([dcf('Matiere')]),
                          'related_concept': set([dcf('T1-760')]),
                         })
        self.assertEqual(e['Label'][pref_labels.pop()],
                         {'label': set([ul(u'société savante', 'fr-fr')]),
                          'language_code': set([u'fr-fr']),
                          'pref_label_of': set([dcf('T1-1073')])})


if __name__ == '__main__':
    unittest_main()
