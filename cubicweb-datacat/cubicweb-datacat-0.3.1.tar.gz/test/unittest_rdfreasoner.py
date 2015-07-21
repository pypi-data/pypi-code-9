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

"""Tests for RDF inference engine."""

from logilab.common.testlib import unittest_main, TestCase
import cubicweb.devtools  # Needed to add cubes in PYTHONPATH

from cubes.skos.rdfio import RDFLibRDFGraph
from cubes.datacat import site_cubicweb  # Needed for having monkeypatchs
from cubes.datacat.rdfreasoner import RDFGraphReasoner


class RDFGraphReasonerTC(TestCase):
    """Simple test case for an rdf inference engine."""

    def test_derive_object_types_from_predicate_ranges(self):
        """Check correct inference of object type from predicate range."""
        # Sample data
        dataset_predicate_uri = u'http://www.w3.org/ns/dcat#dataset'
        dataset_type_uri = u'http://www.w3.org/ns/dcat#Dataset'
        distribution_predicate_uri = u'http://www.w3.org/ns/dcat#distribution'
        distribution_type_uri = u'http://www.w3.org/ns/dcat#Distribution'
        subject_uri = u'http://www.expample.org/id/subject'
        object_uri = u'http://www.expample.org/id/object'
        # Add sample data to a graph
        graph = RDFLibRDFGraph()
        graph.add(graph.uri(subject_uri),
                  graph.uri(dataset_predicate_uri),
                  graph.uri(object_uri))
        graph.add(graph.uri(subject_uri),
                  graph.uri(distribution_predicate_uri),
                  graph.uri(object_uri))
        # Derive information and check
        reasoner = RDFGraphReasoner()
        reasoner.load_rdfs(self.datapath('sample-rdfs.n3'))
        reasoner.apply_to_data(graph)
        self.assertIn(dataset_type_uri, graph.types_for_uri(object_uri))
        self.assertIn(distribution_type_uri, graph.types_for_uri(object_uri))


if __name__ == '__main__':
    unittest_main()
