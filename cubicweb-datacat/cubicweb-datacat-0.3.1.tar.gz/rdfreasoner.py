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

"""Contains tools to do some reasoning on RDF graphs.

The main goal is to derive additional RDF statements from an RDF graph, using additional semantic
information, namely RDFS data, and inference rules.

Currently, only an extremely limited subset of inference rules is implemented:

* if ``<subject> <predicate> <object>`` and ``<predicate> <range> <Type>``, then we can derive a new
  RDF statement: ``<object> <rdf:type> <Type>``.

"""

# XXX: rdfio library is currently in the SKOS cube but should move to CubicWeb.
# This will remove dependency on SKOS cube.
from cubes.skos.rdfio import RDFRegistry, RDFLibRDFGraph


class RDFGraphReasoner(object):
    """An instance of `RDFGraphReasoner` can derive additional RDF assertions from an RDF graph.
    """

    def __init__(self):
        self._meta_graph = RDFLibRDFGraph()
        self._prefix_reg = RDFRegistry()
        self._prefix_reg.register_prefix('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
        self._prefix_reg.register_prefix('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
        self._property_range_map = set()

    def load_rdfs(self, rdfs, rdf_format=None):
        """Load given RDFS data into the reasoner's internal knowledge base."""
        self._meta_graph.load(rdfs, rdf_format=rdf_format)
        self._update_property_range_map()

    def apply_to_data(self, graph):
        """Given an RDFLibRDFGraph instance, derive some more information from the graph.

        In other words: add new RDF triples to the graph, deduced from already existing ones, using
        the reasoner's internal knowledge base (from loaded RDFS data) and inference rules.
        """
        self._derive_object_types_from_predicate_ranges(graph)

    def _update_property_range_map(self):
        """Update mapping between properties and ranges in the reasoner's internal knowledge base.

        When finding RDFS triples like ``<predicate> rdfs:range <Type>``, add a new mapping
        ``<predicate> -> <Type>``.
        """
        uri = self._prefix_reg.normalize_uri
        rdf_property_uri = uri('rdf:Property')
        rdfs_range_uri = uri('rdfs:range')
        for property_uri in self._meta_graph.uris_for_type(rdf_property_uri):
            for range_uri in self._meta_graph.objects(entity_uri=property_uri,
                                                      predicate_uri=rdfs_range_uri):
                self._property_range_map.add((property_uri, range_uri))

    def _derive_object_types_from_predicate_ranges(self, graph):
        """Given an RDFLibRDFGraph instance, derive object types from predicates ranges.

        In other words: add in the graph new RDF triples ``<object> rdf:type <Type>``, deduced from
        triples ``<subject> <predicate> <object>`` already in the graph and
        ``<predicate> rdfs:range <Type>`` in the reasoner`s knowledge base.
        """
        rdf_type_uri = self._prefix_reg.normalize_uri('rdf:type')
        for property_uri, range_uri in self._property_range_map:
            for object_uri in graph.objects(predicate_uri=property_uri):
                graph.add(graph.uri(object_uri),
                          graph.uri(rdf_type_uri),
                          graph.uri(range_uri))
