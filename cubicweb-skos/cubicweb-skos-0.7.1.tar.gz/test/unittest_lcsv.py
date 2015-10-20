# coding: utf-8
import cubicweb.devtools  # set $PYTHONPATH
from logilab.common.testlib import TestCase, unittest_main
from cubes.skos import lcsv, rdfio
from cubes.skos.rdfio import unicode_with_language as ul


class LCSV2RDFTC(TestCase):

    def test_missing_prolog_column(self):
        stream = open(self.datapath('lcsv_example_missing_prolog.csv'))
        with self.assertRaises(lcsv.InvalidLCSVFile) as cm:
            lcsv.LCSV2RDF(stream, '\t', 'utf-8', lambda x: x, rdfio.RDFLibRDFGraph().uri)
        self.assertIn("missing prolog column", str(cm.exception))

    def test_missing_id_column(self):
        stream = open(self.datapath('lcsv_example_missing_id.csv'))
        with self.assertRaises(lcsv.InvalidLCSVFile) as cm:
            lcsv.LCSV2RDF(stream, '\t', 'utf-8', lambda x: x, rdfio.RDFLibRDFGraph().uri)
        self.assertIn("missing $id column", str(cm.exception))

    def test_lcsv_parsing(self):
        fpath = self.datapath('lcsv_example_shortened.csv')
        lcsv2rdf = lcsv.LCSV2RDF(open(fpath), '\t', 'utf-8', lambda x: x, lambda x: x, 'es')
        self.assertEqual(set(list(lcsv2rdf.triples())),
                         set([('#1', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                               'http://www.w3.org/2004/02/skos/core#Concept'),
                              ('#1', 'http://www.w3.org/2004/02/skos/core#definition',
                               ul(u"Définition de l'organisation politique de l'organisme,", 'fr')),
                              ('#1', 'http://www.w3.org/2004/02/skos/core#prefLabel',
                               ul(u"Vie politique", 'es')),
                              ('#2', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                               'http://www.w3.org/2004/02/skos/core#Concept'),
                              ('#2', 'http://www.w3.org/2004/02/skos/core#definition',
                               ul(u"Définition (évolution) des règles de fonctionnement", 'fr')),
                              ('#2', 'http://www.w3.org/2004/02/skos/core#prefLabel',
                               ul(u"Assemblée délibérante", 'es')),
                              ('#2', 'http://www.w3.org/2004/02/skos/core#broader',
                               '#1'),
                              ('#3', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                               'http://www.w3.org/2004/02/skos/core#Concept'),
                              ('#3', 'http://www.w3.org/2004/02/skos/core#definition',
                               ul(u"Création volontaire ou en application de la loi", 'fr')),
                              ('#3', 'http://www.w3.org/2004/02/skos/core#prefLabel',
                               ul(u"Instances consultatives", 'es')),
                              ('#3', 'http://www.w3.org/2004/02/skos/core#broader',
                               '#1'),
                              ('#4', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                               'http://www.w3.org/2004/02/skos/core#Concept'),
                              ('#4', 'http://www.w3.org/2004/02/skos/core#definition',
                               ul(u"Fonction de définition d'objectifs à long terme", 'fr')),
                              ('#4', 'http://www.w3.org/2004/02/skos/core#prefLabel',
                               ul(u"Pilotage de l'organisation", 'es')),
                              ('#5', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                               'http://www.w3.org/2004/02/skos/core#Concept'),
                              ('#5', 'http://www.w3.org/2004/02/skos/core#definition',
                               ul(u"Définition du projet d'administration", 'fr')),
                              ('#5', 'http://www.w3.org/2004/02/skos/core#prefLabel',
                               ul(u"Pilotage de Bordeaux Metropole", 'es')),
                              ('#5', 'http://www.w3.org/2004/02/skos/core#broader',
                               '#4')
                             ])
                        )

if __name__ == "__main__":
    unittest_main()
