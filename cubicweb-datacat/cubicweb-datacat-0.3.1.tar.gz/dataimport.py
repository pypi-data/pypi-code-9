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

"""Module containing tools to parse external sources in order to import data from them.

Only relevant data of interest are retrieved and they are turned into ExtEntity instances before
being imported (that is converted into instance's entities according to the data model).
"""

from urllib2 import HTTPError, URLError
from functools import partial

from rdflib.plugin import PluginException

from cubicweb.schema import META_RTYPES

# XXX: ExtEntitiesImport is currently in the SKOS cube but should move to CubicWeb.
# This will remove dependency on SKOS cube.
from cubes.skos.dataimport import ExtEntitiesImporter, cwuri2eid
from cubes.skos import ExtEntity

# XXX: rdfio library is currently in the SKOS cube but should move to CubicWeb.
# This will remove dependency on SKOS cube.
from cubes.skos.rdfio import RDFRegistry, RDFLibRDFGraph, rdf_graph_to_entities
# XXX: rdfreasoner library is currently in the Datacat cube but should move with rdfio.
from cubes.datacat.rdfreasoner import RDFGraphReasoner


def register_dcat_cw_rdf_mapping(reg):
    """Declare mapping between CubicWeb DCAT entities and RDF DCAT ontology.

    ``reg`` parameter must be an ``RDFRegistry`` instance.
    """
    reg.register_prefix('dcat', 'http://www.w3.org/ns/dcat#')
    reg.register_prefix('dct', 'http://purl.org/dc/terms/')
    reg.register_prefix('adms', 'http://www.w3.org/ns/adms#')
    reg.register_etype_equivalence('DataCatalog', 'dcat:Catalog')
    reg.register_attribute_equivalence('DataCatalog', 'title', 'dct:title')
    reg.register_attribute_equivalence('DataCatalog', 'description', 'dct:description')
    reg.register_attribute_equivalence('DataCatalog', 'issued', 'dct:issued')
    reg.register_attribute_equivalence('DataCatalog', 'modified', 'dct:modified')
    reg.register_etype_equivalence('Dataset', 'dcat:Dataset')
    reg.register_attribute_equivalence('Dataset', 'title', 'dct:title')
    reg.register_attribute_equivalence('Dataset', 'description', 'dct:description')
    reg.register_attribute_equivalence('Dataset', 'issued', 'dct:issued')
    reg.register_attribute_equivalence('Dataset', 'modified', 'dct:modified')
    reg.register_attribute_equivalence('Dataset', 'identifier', 'adms:identifier')
    reg.register_relation_equivalence('Dataset', 'in_catalog', 'DataCatalog', 'dcat:dataset',
                                      reverse=True)
    reg.register_etype_equivalence('Distribution', 'dcat:Distribution')
    reg.register_attribute_equivalence('Distribution', 'title', 'dct:title')
    reg.register_attribute_equivalence('Distribution', 'description', 'dct:description')
    reg.register_attribute_equivalence('Distribution', 'issued', 'dct:issued')
    reg.register_attribute_equivalence('Distribution', 'modified', 'dct:modified')
    reg.register_attribute_equivalence('Distribution', 'access_url', 'dcat:accessURL')
    reg.register_attribute_equivalence('Distribution', 'download_url', 'dcat:downloadURL')
    reg.register_relation_equivalence('Distribution', 'of_dataset', 'Dataset',
                                      'dcat:distribution', reverse=True)


def fetch_rdf_dcat_ext_entities(uri, schema, dcat_meta_uri, rdf_format=None,
                                import_log=None, raise_on_error=False):
    """Harvest a RDF DCAT catalog given by its URI.

    Returns an iterator containing relevant ExtEntity instances retrieved from the catalog.

    URI must reference RDF data that can be loaded into a graph (that is URI can be given as a
    parameter to the ``load()`` method of an ``RDFLibDFGraph`` Instance).

    ``schema`` parameter is the CubicWeb schema to which fetched ext entities are related.

    ``dcat_meta_uri`` parameter is the uri where the DCAT definitions can be found in OWL syntax.
    """
    # Declare mapping between the CW schema and DCAT terms
    reg = RDFRegistry()
    register_dcat_cw_rdf_mapping(reg)
    # Create a graph, load it with triples found at URI
    graph = RDFLibRDFGraph()
    graph.load(uri, rdf_format=rdf_format)
    # Add triples found by following DCAT types
    for type_uri in ['dcat:Catalog', 'dcat:Dataset', 'dcat:Distribution']:
        type_uri = reg.normalize_uri(type_uri)
        for uri in graph.uris_for_type(type_uri):
            _load_rdf(graph, uri, rdf_format=rdf_format, import_log=import_log,
                      raise_on_error=raise_on_error)
    # Add triples found by following DCAT predicates
    for predicate_uri in ['dcat:dataset', 'dcat:distribution']:
        predicate_uri = reg.normalize_uri(predicate_uri)
        for object_uri in graph.objects(predicate_uri=predicate_uri):
            _load_rdf(graph, object_uri, rdf_format=rdf_format, import_log=import_log,
                      raise_on_error=raise_on_error)
    # Derive new information from the graph
    reasoner = RDFGraphReasoner()
    reasoner.load_rdfs(dcat_meta_uri)
    reasoner.apply_to_data(graph)
    # Parse the graph, extract ext entities, but yield only those who conform to the schema
    valid_extentity = partial(valid_extentity_for_schema, schema,
                              import_log=import_log, raise_on_error=raise_on_error)
    for raw_ext_entity in rdf_graph_to_entities(reg, graph,
                                                ('DataCatalog', 'Dataset', 'Distribution')):
        ext_entity = valid_extentity(raw_ext_entity)
        if ext_entity is not None:
            yield ext_entity


def _load_rdf(graph, uri, rdf_format=None, import_log=None, raise_on_error=False):
    """Load RDF triples at given URI into the specified graph, catching errors.

    Currently, the following errors are catched:

        * ``IOError`` when URI is not well-formed and redirects to a local file (eg.
          ``/home/jdoe/file/n3`` or ``_:123456789`` which is the kind of URI commonly found in the
          wild),

        * ``HTTPError`` when HTTP return code is not 2XX or 3XX (eg. ``404 Not Found``),

        * ``URLError`` when URI is invalid.

    The ``graph`` parameter must be an instance of RDFLibRDFGraph.
    """
    try:
        graph.load(uri, rdf_format=rdf_format)
    except (IOError, HTTPError, URLError, PluginException):
        if import_log:
            import_log.record_error('Unable to parse found URI: {}'.format(uri))
        if raise_on_error:
            raise


def valid_extentity_for_schema(schema, ext_entity, import_log=None, raise_on_error=False):
    """From the given ext entity, returns a valid one, that is conform to the given schema.

    Returns ``None`` if it is impossible to do so.

    Please recall that an ext entity is an instance of the ``ExtEntity`` class. It has the following
    properties:

    * ``extid`` (external id), an identifier for the ext entity,
    * ``etype`` (entity type), a string which must be the name of one entity type in the schema
      (eg. ``'DataCatalog'``, ``'Dataset'``, ...),
    * ``values``, a dictionary whose keys are name of attributes or relations in the schema (eg.
      ``'title'``, ``'in_catalog'``) and whose values are *sets* of data found for this attribute
      at the external source. For instance::

        {'title': set([u"My title", u"Mon titre"]), 'issued': set(["2015-01-01"])}

    This function will return a new ext entity with a valid ``values`` dictionary. In the preceding
    example, the ``title`` will only have one value, and ``issued`` will hold a datetime object::

        {'title': set([u"My title"]), 'issued': set([datetime(2015, 1, 1)])}

    """
    eschema = schema.eschema(ext_entity.etype)  # Entity definition
    valid_values = {}
    # Loop over each attribute and relation in entity definition
    for rschema in eschema.subject_relations():
        # Skip if this is not user defined
        if rschema in META_RTYPES or eschema.is_metadata(rschema):
            continue
        # Compute a valid value for this attribute/relation in the ext entity
        rname, valid_value = valid_value_for_schema(eschema, rschema, ext_entity,
                                                    import_log=import_log,
                                                    raise_on_error=raise_on_error)
        if rname is None:  # Missing required attribute
            return None
        if not valid_value:
            continue
        valid_values[rname] = valid_value
    # Return new ext entity
    return ExtEntity(etype=ext_entity.etype, extid=ext_entity.extid, values=valid_values)


def valid_value_for_schema(eschema, rschema, ext_entity, import_log=None, raise_on_error=False):
    """Returns a 2-uple ``(name, set([values]))`` where ``values`` are valid values for the
    specified attribute (``rschema``) in the ext entity, and ``name`` is the attribute name.

    Valid value means a value conform to the given entity definition (``eschema``).

    Since this function is used in an ext entity context, valid values are returned in a set.

    Consequently, if ``rschema`` defines an attribute or an inlined relation, the returned set will
    hold only one valid value.

    If no valid value can be found for the attribute in the ext entity, and attribute is required in
    the schema, the first element returned is None, that is the function returns ``(None, None)``.
    """
    tschema = eschema.destination(rschema)  # Definition of target type
    # Get attribute/relation name and current value
    rname = rschema.type
    current_set = ext_entity.values.get(rname, set())
    # Compute valid set
    valid_set = set()
    if rschema.final:  # If this is an attribute: try to find a valid value
        valid_value = valid_literal_value(tschema, current_set)
        valid_set = set([valid_value]) if valid_value is not None else set()
    elif rschema.inlined:  # If this is an inlined relation, returns a one element set
        valid_set = set([current_set.pop()]) if current_set else set()
    else:  # Else relation is non-inlined: just copy the values
        valid_set = current_set.copy()
    # Log a warning if we are discarding some values
    if import_log is not None and 1 <= len(valid_set) < len(current_set):
        original_set_str = ', '.join(unicode(value) for value in current_set)
        final_set_str = ', '.join(unicode(value) for value in valid_set)
        import_log.record_warning(
            u"{}: multiple values for attribute {} ({}), picking only {}".format(
                ext_entity.extid, rname, original_set_str, final_set_str))
    # Log an error if this is a missing required attribute
    if not valid_set and rschema.rdef(eschema, tschema).role_cardinality('subject') == '1':
        msg = "Discarding external entity {} (attribute '{}' required)".format(ext_entity.extid,
                                                                               rname)
        if import_log is not None:
            import_log.record_error(msg)
        if raise_on_error:
            raise ValueError(msg)
        return None, None
    return rname, valid_set


def valid_literal_value(tschema, values):
    """Among the given values, returns one which is valid according to the type definition
    ``tschema`` (``Int``, ``String``, ``Datetime``, etc.), maybe after conversion.

    Returns ``None`` if no value is valid or can be converted to a valid one.
    """
    for value in values:
        try:
            valid_value = tschema.convert_value(value)
        except ValueError:
            continue
        if tschema.check_value(valid_value):
            return valid_value
    return None


def import_dcat_ext_entities(ext_entities, store, cnx, import_log, source=None,
                             raise_on_error=False):
    """Import DCAT external entities into CubicWeb entities using the given store.

    The ``cnx`` parameter gives the CubicWeb connection used to import the ext entities.

    The ``source`` parameter gives the CubicWeb source from which ext_entities are coming. This
    is optional since CubicWeb stores currently do not make use of sources.
    """
    etypes_order_hint = ['DataCatalog', 'Dataset', 'Distribution']
    importer = NoSourceConstraintExtEntitiesImporter(
        cnx=cnx, store=store, source=source, etypes_order_hint=etypes_order_hint,
        import_log=import_log, raise_on_error=raise_on_error)
    return importer.import_entities(ext_entities)


# XXX: this is a hack because RQLObjectStore does not support CWSources, thus leading to duplicate
# already imported entities
class NoSourceConstraintExtEntitiesImporter(ExtEntitiesImporter):
    """Ext entities importer who do not check from which sources entitites are imported.

    By default, an ExtEntitiesImporter instance will check the source of already imported entities.
    This mean that two ext entities with same URI (``cwuri``) but coming from different sources will
    be imported as two distinct entities in repository.

    At the opposite, an instance of this class will, by default, import only the first encountered
    ext entity. The other one will be discarded because it has the same ``cwuri``, regardless of the
    source.
    """

    def __init__(self, cnx, store, import_log, source=None,
                 raise_on_error=False, etypes_order_hint=(), extid2eid=None):
        if extid2eid is None:
            extid2eid = cwuri2eid(cnx, etypes_order_hint)
        super(NoSourceConstraintExtEntitiesImporter, self).__init__(
            cnx, store, import_log, source=source, raise_on_error=raise_on_error,
            etypes_order_hint=etypes_order_hint, extid2eid=extid2eid
        )

    def existing_relations(self, rtype):
        """Returns a set of tuple (subject_eid, object_eid) already related by given ``rtype``"""
        rql = 'Any X, O WHERE X {} O'.format(rtype)
        return set(tuple(x) for x in self.cnx.execute(rql))
