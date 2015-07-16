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
"""Utilities for RDF import/export"""

from os.path import abspath

from cubes.skos import ExtEntity


class unicode_with_language(unicode):
    """Extend an unicode string to hold a .lang attribute as well"""

    def __new__(cls, content, lang):
        self = unicode.__new__(cls, content)
        self.lang = lang
        return self

    def __eq__(self, other):
        if isinstance(other, unicode_with_language):
            return (unicode(self), self.lang) == (unicode(other), other.lang)
        return False

    def __ne__(self, other):
        return not self == other

def normalize_uri(uri, prefixes):
    """Normalize uri by attempting to substitute prefix by the associated namespace. Returns the
    normalized URI.
    """
    try:
        prefix, value = uri.split(':', 1)
    except ValueError:
        return uri
    try:
        return prefixes[prefix] + value
    except KeyError:
        return uri

class RDFRegistryError(Exception):
    pass


class RDFRegistry(object):
    """Class inspired from yams.xy / cubes.dataio.xy and holding static information about how to
    convert from a Yams model to RDF and the other way around.
    """
    def __init__(self):
        self.prefixes = {}
        self.etype2rdf = {}
        self.attr2rdf = {}
        self.rel2rdf = {}

    def normalize_uri(self, uri):
        return normalize_uri(uri, self.prefixes)

    def register_prefix(self, prefix, namespace, overwrite=False):
        """Associate a prefix to a namespace. If the prefix is already registered to a different
        namespace, an exception is raised unless overwrite is True. Registered prefixes may be used
        in RDF snippets used in `register_*` methods.
        """
        if not overwrite and self.prefixes.get(prefix, namespace) != namespace:
            raise RDFRegistryError('prefix %r is already defined with different value %r'
                                   % (prefix, self.prefixes[prefix]))
        self.prefixes[prefix] = namespace

    def register_etype_equivalence(self, etype, rdftype, overwrite=False):
        """Associate a Yams entity type to a RDF type. If the entity type is already registered to a
        different RDF type, an exception is raised unless overwrite is True.
        """
        rdftype = self.normalize_uri(rdftype)
        if not overwrite and self.etype2rdf.get(etype, rdftype) != rdftype:
            raise RDFRegistryError('entity type %r is already associated to RDF type %r'
                                   % (etype, self.etype2rdf[etype]))
        self.etype2rdf[etype] = rdftype

    def register_attribute_equivalence(self, etype, attr, rdftype, overwrite=False):
        """Associate a Yams entity attribute to a RDF predicate. If the entity attribute is already
        registered to a different RDF type, an exception is raised unless overwrite is True.
        """
        rdftype = self.normalize_uri(rdftype)
        if not overwrite and self.attr2rdf.get((etype, attr), rdftype) != rdftype:
            raise RDFRegistryError('entity attribute %s.%r is already associated to RDF type %r'
                                   % (etype, attr, self.attr2rdf[(etype, attr)]))
        self.attr2rdf[(etype, attr)] = rdftype

    def register_relation_equivalence(self, subject_etype, rel, object_etype, rdftype,
                                      reverse=False):
        """Associate a Yams entity relation to a RDF predicated. The `reverse` flag may be used to
        indicate that in RDF, the subject and object are reversed (e.g. 'E1 yams_relation E2' is
        'E2 predicate E1 in RDF').
        """
        rdftype = self.normalize_uri(rdftype)
        self.rel2rdf.setdefault((subject_etype, rel, object_etype), set()).add((rdftype, reverse))

    def predicates_for_subject_etype(self, etype):
        """Given a yams entity type, return (yams relation type, rdf predicate uri, reverse) 3-uple
        where the entity type is subject of the yams relation. `reverse` is a boolean flag telling
        wether the relation should be expected in the opposite direction in RDF (i.e. corresponding
        entity is the object of the rdf predicate), as they are not necessarily in the same order.
        """
        for (subject_etype, attr), rdftype in self.attr2rdf.items():
            if subject_etype == etype:
                yield attr, rdftype, False
        for (subject_etype, rel, _), rdf_relations in self.rel2rdf.items():
            if subject_etype == etype:
                for (rdftype, reverse) in rdf_relations:
                    yield rel, rdftype, reverse

    def additional_object_predicates(self, etype):
        """Given a yams entity type, return (yams relation type, rdf predicate uri, reverse) 3-uple
        where the entity type is object of the yams relation. `reverse` is a boolean flag telling
        wether the relation should be expected in the opposite direction in RDF (i.e. corresponding
        entity is the object of the rdf predicate), as they are not necessarily in the same order.

        Only relations whose subject is not a registered entity types (i.e. have had a mapping
        registered by :meth:`register_etype_equivalence`) will be returned.
        """
        for (subject_etype, rel, object_etype), rdf_relations in self.rel2rdf.items():
            if object_etype == etype and subject_etype not in self.etype2rdf:
                for (rdftype, reverse) in rdf_relations:
                    yield rel, rdftype, reverse


class LibRDFRDFGraph(object):
    """redland's librdf based RDF graph"""

    def __init__(self, options_string="new='yes',hash-type='memory',dir='.'"):
        import RDF
        storage = RDF.HashStorage("test", options_string)
        self._model = RDF.Model(storage)
        self._parser = RDF.Parser('raptor')
        self._uri = RDF.Uri
        self._node = RDF.Node
        self._stmt = RDF.Statement

    def load(self, path_or_url, rdf_format=None):
        """Add RDF triplets from a file path or URL into the graph. `rdf_format` may be one of 'nt',
        'n3' or 'xml'. If not specified, it will be guessed from the file or URL extension.
        """
        if rdf_format not in (None, 'nt', 'n3', 'xml', 'rdfa', 'grddl'):
            raise ValueError('unknown rdf_format: %s' % rdf_format)
        if not ':/' in path_or_url:
            path_or_url = 'file://' + abspath(path_or_url)
        uri = self._uri(string=path_or_url)
        self._parser.parse_into_model(self._model, uri)
        self._model.sync() # in case model use a persistent storage

    def uris_for_type(self, type_uri):
        """Yield URIs of the given RDF type"""
        qs = self._stmt(subject=None,
                        predicate=self._node(uri_string='http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                        object=self._node(uri_string=type_uri))
        for statement in self._model.find_statements(qs):
            yield str(statement.subject.uri)

    def objects(self, entity_uri, predicate_uri):
        """Yield object URIs or literals that are linked to `entity_uri` through
        `predicate_uri`.
        """
        qs = self._stmt(subject=self._node(uri_string=entity_uri),
                        predicate=self._node(uri_string=predicate_uri),
                        object=None)
        for statement in self._model.find_statements(qs):
            if statement.object.is_literal():
                string_value, language, datatype_uri = statement.object.literal
                if language is not None:
                    yield unicode_with_language(string_value, language)
                else:
                    yield string_value #XXX type according to datatype_uri
            else:
                yield str(statement.object.uri)

    def subjects(self, predicate_uri, entity_uri):
        """Yield subject URIs that are linked to `entity_uri` through
        `predicate_uri`.
        """
        qs = self._stmt(subject=None,
                        predicate=self._node(uri_string=predicate_uri),
                        object=self._node(uri_string=entity_uri))
        for statement in self._model.find_statements(qs):
            yield str(statement.subject.uri)


class RDFLibRDFGraph(object):
    """rdflib based RDF graph (http://rdflib.readthedocs.org)"""

    def __init__(self):
        import rdflib
        self.uri = rdflib.URIRef
        self._namespace = rdflib.namespace
        self._literal = rdflib.Literal
        self._guess_format = rdflib.util.guess_format
        self._graph = rdflib.ConjunctiveGraph()
        from rdflib.plugin import register, Parser
        register('text/rdf+n3', Parser, 'rdflib.plugins.parsers.notation3', 'N3Parser')

    def add(self, subj, predicate, obj):
        """Add statement to graph. subject and predicate are expected to be URIs and object may
        be either a URI or a literal value.
        """
        assert isinstance(subj, self.uri)
        assert isinstance(predicate, self.uri)
        if not isinstance(obj, self.uri):
            if isinstance(obj, unicode_with_language):
                obj = self._literal(obj, lang=obj.lang)
            else:
                obj = self._literal(obj)
        self._graph.add((subj, predicate, obj))


    def load(self, path_or_url, rdf_format=None):
        """Add RDF triplets from a file stream, path or URL into the graph. `rdf_format` may be one
        of 'nt', 'n3' or 'xml'. If not specified, it will be guessed from the file or URL extension.
        """
        assert rdf_format in (None, 'nt', 'n3', 'xml', 'rdfa', 'grddl'), rdf_format
        if rdf_format is None and isinstance(path_or_url, basestring):
            rdf_format = self._guess_format(path_or_url)
        self._graph.parse(path_or_url, format=rdf_format)

    def uris_for_type(self, type_uri):
        """Return an iterator on URIs of the given RDF type"""
        for subj in self._graph.subjects(self._namespace.RDF.type, self.uri(type_uri)):
            yield unicode(subj)

    def objects(self, entity_uri, predicate_uri):
        """Return an iterator on object URIs or literals that are linked to `entity_uri` through
        `predicate_uri`.
        """
        for obj in self._graph.objects(self.uri(entity_uri), self.uri(predicate_uri)):
            if isinstance(obj, self.uri):
                yield unicode(obj)
            elif obj.language is not None:
                yield unicode_with_language(obj.toPython(), obj.language)
            else:
                yield obj.toPython()

    def subjects(self, predicate_uri, entity_uri):
        """Return an iterator on subject URIs that are linked to `entity_uri` through
        `predicate_uri`.
        """
        for subj in self._graph.subjects(self.uri(predicate_uri), self.uri(entity_uri)):
            yield unicode(subj)


def rdf_graph_to_entities(reg, graph, etypes, relation_callbacks=None):
    """Turns RDF data into an transitional ExtEntity representation that may
    be then imported into some database easily.

    Mapping is done using a RDF registry `reg` (see :class:`RDFRegistry`).

    A `relation_callbacks` dictionary may be given, containing some relation type as key and a
    callback function to be called in place of the default behaviour. This function will be given
    (extentity, relation type, uri or literal values) as arguments.
    """
    def default_callback(extentity, rtype, uris):
        uris = set(uris)
        if uris:
            extentity.values[rtype] = set(uris)
        return ()

    if relation_callbacks is None:
        relation_callbacks = {}
    for etype in etypes:
        type_uri = reg.etype2rdf[etype]
        for uri in graph.uris_for_type(type_uri):
            extentity = ExtEntity(etype, uri)
            for rtype, predicate_uri, reverse in reg.predicates_for_subject_etype(etype):
                if reverse:
                    uris = graph.subjects(predicate_uri, uri)
                else:
                    uris = graph.objects(uri, predicate_uri)
                callback = relation_callbacks.get(rtype, default_callback)
                for edict in callback(extentity, rtype, uris):
                    yield edict
            for rtype, predicate_uri, reverse in reg.additional_object_predicates(etype):
                if reverse:
                    uris = graph.objects(uri, predicate_uri)
                else:
                    uris = graph.subjects(predicate_uri, uri)
                callback = relation_callbacks.get(rtype, default_callback)
                for edict in callback(extentity, rtype, uris):
                    yield edict
            yield extentity
