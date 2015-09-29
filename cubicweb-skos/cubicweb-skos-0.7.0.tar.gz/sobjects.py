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
"""SKOS import is available through:

* a c-c command
* a repository service
* the datafeed source API

The first two will create local entities (i.e. whose `cw_source` relation points to system source)
while the last will create entities belonging to the external source.

This file contains generic import code, the datafeed parser and the repository service.
"""

from itertools import imap
from hashlib import md5
from uuid import uuid4

from cubicweb import schema
from cubicweb.predicates import match_kwargs, match_user_groups
from cubicweb.server import Service
from cubicweb.server.sources import datafeed

from cubicweb import dataimport
from cubes.skos import LABELS_RDF_MAPPING, ExtEntity, register_skos_rdf_input_mapping, rdfio, lcsv
from cubes.skos.dataimport import ExtEntitiesImporter, HTMLImportLog, cwuri2eid


def dump_relations(cnx, eid, etype):
    """Return a list of relation 3-uples `(subject_eid, relation, object_eid)` with None instead of
    `subject_eid` or `object_eid` depending on whether the entity type corresponding to `eid` is
    subject or object.
    """
    eschema = cnx.vreg.schema.eschema(etype)
    relations = []
    for rschema, _, role in eschema.relation_definitions():
        if rschema.rule:  # computed relation
            continue
        rtype = rschema.type
        if rtype in schema.VIRTUAL_RTYPES or rtype in schema.META_RTYPES:
            continue
        if role == 'subject':
            for object_eid, in cnx.execute('Any Y WHERE X %s Y, X eid %%(x)s' % rtype, {'x': eid}):
                if object_eid == eid:
                    object_eid = None
                relations.append((None, rtype, object_eid))
        else:
            for subject_eid, in cnx.execute('Any Y WHERE Y %s X, X eid %%(x)s' % rtype, {'x': eid}):
                if subject_eid == eid:
                    subject_eid = None
                relations.append((subject_eid, rtype, None))
    return relations


class RDFSKOSImportService(Service):
    """Cubicweb service to import a ConceptScheme from SKOS RDF"""
    __regid__ = 'rdf.skos.import'
    __select__ = match_kwargs('stream') & match_user_groups('managers')

    def call(self, stream, **kwargs):
        import_log = HTMLImportLog(getattr(stream, 'filename', u''))
        (created, updated), scheme_uris = self._do_import(stream, import_log, **kwargs)
        import_log.record_info('%s entities created' % len(created))
        import_log.record_info('%s entities updated' % len(updated))
        self._cw.commit()
        return import_log.logs, scheme_uris

    def _do_import(self, stream, import_log, **kwargs):
        """Extracted method to let a chance to client cubes to give more arguments to _skos_import
        function
        """
        return _skos_import_rdf(self._cw, stream, import_log, **kwargs)


class LCSVSKOSImportService(RDFSKOSImportService):
    """Cubicweb service to import a Concept and Label entities from LCSV file"""
    __regid__ = 'lcsv.skos.import'

    def _do_import(self, stream, import_log, **kwargs):
        """Import Concept and Label entities and related them to `scheme`"""
        return _skos_import_lcsv(self._cw, stream, import_log, **kwargs)


class SKOSParser(datafeed.DataFeedParser):
    __regid__ = 'rdf.skos'

    def process(self, url, raise_on_error=False):
        """Main entry point"""
        try:
            created, updated = self._do_import(url, raise_on_error=raise_on_error)[0]
        except Exception as ex:
            if raise_on_error:
                raise
            self.exception('error while importing %s', url)
            self.import_log.record_error(str(ex))
            return True
        self.stats['created'] = created
        self.stats['updated'] = updated
        return False

    def _do_import(self, url, raise_on_error, **kwargs):
        """Extracted method to let a chance to client cubes to give more arguments to _skos_import
        function
        """
        try:
            rdf_format = rdfio.guess_rdf_format(url)
        except ValueError:
            rdf_format = 'xml'
        return _skos_import_rdf(self._cw, url, self.import_log, source=self.source,
                                rdf_format=rdf_format, raise_on_error=raise_on_error, **kwargs)


def _skos_import_lcsv(cnx, stream, import_log, scheme_uri, delimiter,
                      encoding, language_code=None, **kwargs):
    """import SKOS from LCSV stream or URL (by transforming it to RDF first)"""
    graph = rdfio.RDFLibRDFGraph()
    # add LCSV statements to the RDF graph
    lcsv2rdf = lcsv.LCSV2RDF(stream, delimiter, encoding, default_lang=language_code,
                             uri_cls=graph.uri, uri_generator=lambda x: str(uuid4()) + x)
    for (subj, pred, obj) in lcsv2rdf.triples():
        graph.add(subj, pred, obj)

    # we need an extra transform that link Concept to the parent concept skeme
    def relate_concepts(extentity):
        """Relate Concept ExtEntities to the ConceptScheme"""
        if extentity.etype == 'Concept':
            extentity.values.setdefault('in_scheme', set([])).add(scheme_uri)
        return extentity

    entities = imap(relate_concepts, _skos_entities(graph))
    # now import the extentities stream
    return _skos_import(cnx, entities, import_log, use_extid_as_cwuri=False, **kwargs)


def _skos_import_rdf(cnx, stream_or_url, import_log, rdf_format=None, **kwargs):
    """import SKOS from RDF stream or URL"""
    # build the RDF graph
    graph = rdfio.RDFLibRDFGraph()
    graph.load(stream_or_url, rdf_format)
    entities = _skos_entities(graph)
    return _skos_import(cnx, entities, import_log, **kwargs)


def _skos_entities(graph):
    """return external entities from a SKOS stream or URL"""
    reg = rdfio.RDFRegistry()
    register_skos_rdf_input_mapping(reg)
    all_label_rtypes = frozenset(LABELS_RDF_MAPPING)
    # transform direct mapping of RDF as ExtEntity into Yams compatible ExtEntity by turning label
    # literals into entities.
    for extentity in rdfio.rdf_graph_to_entities(reg, graph, ('ConceptScheme', 'Concept')):
        label_rtypes = frozenset(extentity.values) & all_label_rtypes
        if not label_rtypes:
            yield extentity
            continue
        labels = []
        for rtype in label_rtypes:
            kind = rtype.split('_', 1)[0]  # drop '_label' suffix
            for label in extentity.values.pop(rtype):
                lang = getattr(label, 'lang', None)
                md5hash = md5(str(lang) + label.encode('utf-8'))
                labelid = str(extentity.extid) + '#' + rtype + md5hash.hexdigest()
                labels.append(ExtEntity('Label', labelid,
                                        {'label': set([label]),
                                         'language_code': set([lang]),
                                         'kind': set([kind]),
                                         'label_of': set([extentity.extid])}))
        # yield extentity before labels since it must be handled first in case the ExternalUri
        # to Concept transformation apply
        yield extentity
        for label in labels:
            yield label


def _skos_import(cnx, entities, import_log, source=None, raise_on_error=False, metagenerator=None,
                 use_extid_as_cwuri=True):
    """import SKOS external entities"""
    # use NoHookRQLObjectStore for insertion in the database, with a custom metagenerator to
    # properly set the source for created entities
    if metagenerator is None:
        metagenerator = dataimport.MetaGenerator(cnx, source=source)
    store = dataimport.NoHookRQLObjectStore(cnx, metagenerator)
    # only consider the system source for schemes and labels
    if source is None:
        source_eid = cnx.repo.system_source.eid
    else:
        source_eid = source.eid
    extid2eid = cwuri2eid(cnx, ('ConceptScheme', 'Label'), source_eid=source_eid)
    # though concepts and external URIs may come from any source
    extid2eid.update(cwuri2eid(cnx, ('Concept', 'ExternalUri')))
    # plug function that turn previously known external uris by newly inserted concepts
    restore_relations = {}

    def externaluri_to_concept(extentity, cnx=cnx, extid2eid=extid2eid,
                               restore_relations=restore_relations):
        try:
            eid = extid2eid[extentity.extid]
        except KeyError:
            pass
        else:
            if extentity.etype == 'Concept' and cnx.entity_metas(eid)['type'] == 'ExternalUri':
                # We have replaced the external uri by the new concept. As entities.extid column is
                # unique, we've to drop the external uri before inserting the concept, so we:
                #  1. record every relations from/to the external uri,
                #  2. remove it,
                #  3. insert the concept and
                #  4. reinsert relations using the concept instead
                #
                # 1. record relations from/to the external uri
                restore_relations[extentity.extid] = dump_relations(cnx, eid, 'ExternalUri')
                # 2. remove the external uri entity
                cnx.execute('DELETE ExternalUri X WHERE X eid %(x)s', {'x': eid})
                # 3. drop its extid from the mapping to trigger insertion of the concept by the
                # importer
                del extid2eid[extentity.extid]
                # 4. will be done in SKOSExtEntitiesImporter
        return extentity

    entities = imap(externaluri_to_concept, entities)
    # plug function to detect the concept scheme
    concept_schemes = []

    def record_scheme(extentity):
        if extentity.etype == 'ConceptScheme':
            concept_schemes.append(extentity.extid)
        return extentity

    entities = imap(record_scheme, entities)
    etypes_order_hint = ('ConceptScheme', 'Concept', 'Label')
    importer = SKOSExtEntitiesImporter(cnx, store, import_log, source=source, extid2eid=extid2eid,
                                       raise_on_error=raise_on_error,
                                       etypes_order_hint=etypes_order_hint,
                                       restore_relations=restore_relations)
    stats = importer.import_entities(entities, use_extid_as_cwuri=use_extid_as_cwuri)
    return stats, concept_schemes


class SKOSExtEntitiesImporter(ExtEntitiesImporter):
    """Override ExtEntitiesImporter to handle creation of additionnal relations to newly created
    concepts that replace a former external uri, and to create ExternalUri entities for URIs used in
    exact_match / close_match relations which have no known entity in the repository yet.
    """

    def __init__(self, *args, **kwargs):
        self.restore_relations = kwargs.pop('restore_relations')
        super(SKOSExtEntitiesImporter, self).__init__(*args, **kwargs)

    def create_entity(self, extentity):
        entity = super(SKOSExtEntitiesImporter, self).create_entity(extentity)
        # (4.) restore relations formerly from/to an equivalent external uri
        try:
            relations = self.restore_relations.pop(extentity.extid)
        except KeyError:
            return entity
        for subject_eid, rtype, object_eid in relations:
            if subject_eid is None:
                subject_eid = entity.eid
            if object_eid is None:
                object_eid = entity.eid
            self.store.relate(subject_eid, rtype, object_eid)
        return entity

    def create_deferred_relations(self, deferred):
        # create missing targets for exact_match and close_match relations
        for rtype in ('exact_match', 'close_match'):
            relations = deferred.get(rtype, ())
            for subject_uri, object_uri in relations:
                if object_uri not in self.extid2eid:
                    extentity = ExtEntity('ExternalUri', object_uri,
                                          values=dict(uri=unicode(object_uri),
                                                      cwuri=unicode(object_uri)))
                    assert self.create_entity(extentity).cw_etype == 'ExternalUri'
        return super(SKOSExtEntitiesImporter, self).create_deferred_relations(deferred)

    def existing_relations(self, rtype):
        """return a set of (subject, object) eids already related by `rtype`"""
        if rtype in ('exact_match', 'close_match'):
            rql = 'Any X,O WHERE X %s O' % rtype
            return set(tuple(x) for x in self.cnx.execute(rql))
        return super(SKOSExtEntitiesImporter, self).existing_relations(rtype)
