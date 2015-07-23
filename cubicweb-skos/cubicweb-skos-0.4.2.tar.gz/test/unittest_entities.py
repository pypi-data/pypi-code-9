# coding: utf-8
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

from StringIO import StringIO

from cubicweb.devtools.testlib import CubicWebTC

from cubes.skos.entities import CSVIndentationError, CSVDecodeError


def get_narrower_concepts(concept):
    """Get a dictionnary matching the name of the concept to the dictionnary of its narrower
    concepts (recursive)
    """
    narrower_concepts = {}
    for concept in concept.narrower_concept:
        narrower_concepts[concept.dc_title()] = get_narrower_concepts(concept)
    return narrower_concepts

def build_result_dict(scheme):
    """Create a hierarchy with the concept names in a dictionary"""
    concepts = scheme.top_concepts
    result = {}
    for concept in concepts:
        result[concept.dc_title()] = get_narrower_concepts(concept)
    return result


class ConceptSchemeTC(CubicWebTC):

    def test_top_concepts(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'some classification')
            c1 = cnx.create_entity('Concept', in_scheme=scheme)
            cnx.create_entity('Label', label=u'hip', language_code=u'fr',
                              pref_label_of=c1)
            c2 = cnx.create_entity('Concept', in_scheme=scheme, broader_concept=c1)
            cnx.create_entity('Label', label=u'hop', language_code=u'fr',
                              pref_label_of=c2)
            cnx.commit()
            self.assertEqual(set(x.eid for x in scheme.top_concepts),
                             set((c1.eid,)))

    def test_add_concepts_from_file_interdoc(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'interdoc')
            cnx.commit()
        csv_file = self.datapath('thesaurus_interdoc_7_hierageneTab_shortened.csv')
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            with open(csv_file) as sourcefile:
                scheme.add_concepts_from_file(sourcefile, u'utf-8', u'fr', u',')
            result = build_result_dict(scheme)
        expected = {
            u'ADMINISTRATION': {
                u'ACTION PUBLIQUE': {
                    u'ACTE ADMINISTRATIF': {
                        u'ACTE CREATEUR DE DROITS': {},
                        u'ACTE UNILATERAL': {
                            u'VISA': {},
                        },
                        u'CONTRAT PUBLIC': {
                            u'CONTRAT ADMINISTRATIF': {
                                u'CLAUSE EXORBITANTE': {},
                                u'COTRAITANCE': {
                                    u'GROUPEMENT D\'ENTREPRISES': {
                                        u'GROUPEMENT CONJOINT': {},
                                        u'GROUPEMENT SOLIDAIRE': {},
                                    },
                                },
                                u'EQUILIBRE FINANCIER': {
                                    u'FAIT DU PRINCE': {}
                                },
                                u'VENTE EN L\'ETAT FUTUR D\'ACHEVEMENT': {},
                            },
                            u'CONVENTION D\'EXPLOITATION': {},
                            u'PARTENARIAT PUBLIC-PRIVE': {
                                u'SOCIETE LOCALE DE PARTENARIAT': {},
                            },
                        },
                    },
                },
            },
            u'AMENAGEMENT': {
                u'AMENAGEMENT DU TERRITOIRE': {
                    u'AMENAGEMENT DE LA MONTAGNE': {
                        u'PROTECTION DE LA MONTAGNE': {
                            u'RTM': {},
                        },
                        u'UTN': {},
                        u'ZONE MONTAGNE': {},
                    },
                    u'AMENAGEMENT DU LITTORAL': {
                        u'BANDE LITTORALE DES 100 METRES': {},
                    },
                },
            },
        }
        self.assertEqual(result, expected)

    def test_add_concepts_from_file_ok(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'rapport')
            cnx.commit()
        csv_file = self.datapath('hierarchical_csv_example_shortened.csv')
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            with open(csv_file) as sourcefile:
                scheme.add_concepts_from_file(sourcefile, u'utf-8', u'fr', u'\t')
            result = build_result_dict(scheme)
        expected = {u'APPELLATION DES LOIS ET DES RAPPORTS':
                    {u'LOIS RAPPORTS JURISPRUDENCE':
                     {u'APPELLATION DE DECISIONS DE JURISPRUDENCE':
                      {u'ARRET BERKANI': {}, u'ARRET TERNON': {}},
                      u'APPELLATION DES RAPPORTS':
                      {u'RAPPORT ARTHUIS': {}, u'LOLF': {}, u'LOV': {}}
                     }
                    },
                    u'LISTE DES MOTS OUTILS':
                    {u'CHAPITRE MOTS OUTILS':
                     {u'MOTS OUTILS':
                      {u'ABATTEMENT': {}, u'ACCORD': {}}
                     }
                    }
                   }
        self.assertEqual(result, expected)

    def test_add_concepts_from_file_sep_inside_concept(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'rapport')
            cnx.commit()
        rapport = StringIO('toto\n\tti\tti\n\ttata')
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            scheme.add_concepts_from_file(rapport, u'utf-8', u'fr', u'\t')
            result = build_result_dict(scheme)
        expected = {u'toto': {u'ti\tti': {},
                              u'tata' : {}}}
        self.assertEqual(result, expected)

    def test_add_concepts_from_file_decode_error(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'rapport')
            cnx.commit()
        with open(self.datapath('bad_encoding.csv')) as fobj:
            with self.admin_access.web_request() as req:
                scheme = req.entity_from_eid(scheme.eid)
                with self.assertRaises(CSVDecodeError) as cm:
                    scheme.add_concepts_from_file(fobj, u'utf-8', u'fr', u',')
                self.assertEqual(cm.exception.line, 3)
                # Now with the good encoding.
                fobj.seek(0)
                scheme.add_concepts_from_file(fobj, u'latin1', u'fr', u',')
                result = build_result_dict(scheme)
        expected = {u'voici mes concepts en latin1': {u'celui-ci est bon': {},
                                                      u'celui-là n\'est pas bon': {}}}
        self.assertEqual(result, expected)

    def test_add_concepts_from_file_wrong_indentation(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'rapport')
            cnx.commit()
        rapport = StringIO('toto\n\ttiti\n\t\t\ttata')
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            with self.assertRaises(CSVIndentationError) as cm:
                scheme.add_concepts_from_file(rapport, u'utf-8', u'fr', u'\t')
            self.assertEqual(cm.exception.line, 3)

    def test_add_concepts_from_file_multiple_deindentation(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'rapport')
            cnx.commit()
        rapport = StringIO('toto\n\ttiti\n\t\ttata\ntutu')
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            scheme.add_concepts_from_file(rapport, u'utf-8', u'fr', u'\t')
            result = build_result_dict(scheme)
        expected = {u'toto': {u'titi': {u'tata' : {}}},
                    u'tutu': {}}
        self.assertEqual(result, expected)

    def test_add_concepts_from_file_sep_comma(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'rapport')
            cnx.commit()
        rapport = StringIO('toto\n,titi\n,,tata\n,,  tati  \n tutu \n,tuti\n,,titu\n,toti\n')
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            scheme.add_concepts_from_file(rapport, u'utf-8', u'fr', u',')
            result = build_result_dict(scheme)
        expected = {u'toto': {u'titi': {u'tata' : {}, u'tati': {}}},
                    u'tutu': {u'tuti': {u'titu': {}}, u'toti': {}}}
        self.assertEqual(result, expected)

    def test_add_concepts_from_file_sep_space(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'rapport')
            cnx.commit()
        rapport = StringIO('toto\n titi   iti\n  tata\n  tati  \ntutu \n tuti\n  titu\n toti\n')
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            scheme.add_concepts_from_file(rapport, u'utf-8', u'fr', u' ')
            result = build_result_dict(scheme)
        expected = {u'toto': {u'titi   iti': {u'tata' : {}, u'tati': {}}},
                    u'tutu': {u'tuti': {u'titu': {}}, u'toti': {}}}
        self.assertEqual(result, expected)


class ConceptTC(CubicWebTC):
    def setUp(self):
        super(ConceptTC, self).setUp()
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'some classification')
            c1 = cnx.create_entity('Concept', in_scheme=scheme)
            cnx.create_entity('Label', label=u'hîp', language_code=u'fr-CA',
                              pref_label_of=c1)
            cnx.create_entity('Label', label=u'hip', language_code=u'en',
                              pref_label_of=c1)
            cnx.create_entity('Label', label=u'hop', language_code=u'fr',
                              alt_label_of=c1)
            cnx.commit()
        self.c1_eid = c1.eid

    def test_dc_title(self):
        with self.admin_access.client_cnx() as cnx:
            c1 = cnx.entity_from_eid(self.c1_eid)
            self.assertEqual(c1.dc_title(), u'hip')
            cnx.lang = 'fr'
            self.assertEqual(c1.dc_title(), u'hîp')

    def test_labels(self):
        with self.admin_access.client_cnx() as cnx:
            c1 = cnx.entity_from_eid(self.c1_eid)
            self.assertEqual(c1.labels,
                             {u'en': u'hip', u'fr': u'hîp'})


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
