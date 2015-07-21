# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

import urllib2
import StringIO
from datetime import datetime

from dateutil.parser import parse as parse_datetime

from yams.constraints import BASE_CONVERTERS, BASE_CHECKERS

from logilab.common.decorators import monkeypatch

from cubicweb.server.sources import datafeed
from cubicweb.xy import xy
from cubicweb.web.views import rdf

from cubes.skos import rdfio


xy.register_prefix('dct', 'http://purl.org/dc/terms/')
xy.register_prefix('adms', 'http://www.w3.org/ns/adms#')
xy.register_prefix('dcat', 'http://www.w3.org/ns/dcat#')
xy.register_prefix('vcard', 'http://www.w3.org/2006/dcat/ns#')
xy.add_equivalence('Agent name', 'foaf:name')
xy.add_equivalence('Agent name', 'vcard:fn')  # XXX overrides ^?
xy.add_equivalence('Agent email', 'vcard:hasEmail')
xy.add_equivalence('Dataset identifier', 'dct:identifier')
xy.add_equivalence('Dataset title', 'dct:title')
xy.add_equivalence('Dataset creation_date', 'dct:issued')
xy.add_equivalence('Dataset modification_date', 'dct:modified')
xy.add_equivalence('Dataset description', 'dct:description')
xy.add_equivalence('Dataset keyword', 'dcat:keyword')
xy.add_equivalence('Dataset keyword', 'dcat:theme')
xy.add_equivalence('Dataset landing_page', 'dcat:landingPage')
xy.add_equivalence('Dataset frequency', 'dct:accrualPeriodicity')
xy.add_equivalence('Dataset spatial_coverage', 'dct:spatial')
xy.add_equivalence('Dataset provenance', 'dct:provenance')
xy.add_equivalence('Dataset dataset_distribution', 'dcat:distribution')
xy.add_equivalence('Dataset dataset_publisher', 'dct:publisher')
xy.add_equivalence('Dataset dataset_contact_point', 'adms:contactPoint')
xy.add_equivalence('Distribution access_url', 'dcat:accessURL')
xy.add_equivalence('Distribution description', 'dct:description')
xy.add_equivalence('Distribution format', 'dct:format')
xy.add_equivalence('Distribution licence', 'dct:license')


# Monkeypatch RDF view (https://www.cubicweb.org/4745929).

@monkeypatch(rdf.RDFView)
def entity2graph(self, graph, entity):
    # aliases
    CW = rdf.CW
    urijoin = rdf.urijoin
    RDF = rdf.RDF
    URIRef = rdf.URIRef
    SKIP_RTYPES = rdf.SKIP_RTYPES
    Literal = rdf.Literal

    cwuri = URIRef(entity.cwuri)
    add = graph.add
    add( (cwuri, RDF.type, CW[entity.e_schema.type]) )
    try:
        for item in xy.xeq(entity.e_schema.type):
            add( (cwuri, RDF.type, urijoin(item)) )
    except xy.UnsupportedVocabulary:
        pass
    for rschema, eschemas, role in entity.e_schema.relation_definitions('relation'):
        rtype = rschema.type
        if rtype in SKIP_RTYPES or rtype.endswith('_permission'):
            continue
        for eschema in eschemas:
            if eschema.final:
                try:
                    value = entity.cw_attr_cache[rtype]
                except KeyError:
                    continue # assuming rtype is Bytes
                if value is not None:
                    add( (cwuri, CW[rtype], Literal(value)) )
                    try:
                        for item in xy.xeq('%s %s' % (entity.e_schema.type, rtype)):
                            add( (cwuri, urijoin(item[1]), Literal(value)) )
                    except xy.UnsupportedVocabulary:
                        pass
            else:
                for related in entity.related(rtype, role, entities=True, safe=True):
                    if role == 'subject':
                        add( (cwuri, CW[rtype], URIRef(related.cwuri)) )
                        try:
                            for item in xy.xeq('%s %s' % (entity.e_schema.type, rtype)):
                                add( (cwuri, urijoin(item[1]), URIRef(related.cwuri)) )
                        except xy.UnsupportedVocabulary:
                            pass
                    else:
                        add( (URIRef(related.cwuri), CW[rtype], cwuri) )


#
# Monkeypatch rdfio
#
# See:
# * https://www.cubicweb.org/ticket/5307471
# * https://www.cubicweb.org/ticket/5582296
# * https://www.cubicweb.org/ticket/5313853

@monkeypatch(rdfio.RDFLibRDFGraph)
def objects(self, entity_uri=None, predicate_uri=None):
    """Return an iterator on object URIs or literals that are linked to `entity_uri` through
    `predicate_uri`.
    """
    if entity_uri is not None:
        entity_uri = self.uri(entity_uri)
    if predicate_uri is not None:
        predicate_uri = self.uri(predicate_uri)
    for obj in self._graph.objects(entity_uri, predicate_uri):
        if isinstance(obj, self.uri):
            yield unicode(obj)
        elif hasattr(obj, 'language') and obj.language is not None:
            yield rdfio.unicode_with_language(obj.toPython(), obj.language)
        else:
            yield obj.toPython()


@monkeypatch(rdfio.RDFLibRDFGraph)
def subjects(self, predicate_uri=None, entity_uri=None):
    """Return an iterator on subject URIs that are linked to `entity_uri` through
    `predicate_uri`.
    """
    if predicate_uri is not None:
        predicate_uri = self.uri(predicate_uri)
    if entity_uri is not None:
        entity_uri = self.uri(entity_uri)
    for subj in self._graph.subjects(predicate_uri, entity_uri):
        yield unicode(subj)


@monkeypatch(rdfio.RDFLibRDFGraph)
def types_for_uri(self, uri):
    """Return an iterator that yields all the types (as URI) of the given URI"""
    for obj in self.objects(uri, unicode(self._namespace.RDF.type)):
        yield unicode(obj)


#
# Extend BASE CONVERTERS & CHECKERS for datetime objects
#

def is_datetime(eschema, value):
    """Returns ``True`` if value is a `datetime` object, else ``False``."""
    return isinstance(value, datetime)


def date_time(value):
    """Returns a `datetime` object, as a result of converting the given value.

    Raise a ``ValueError`` if the value cannot be converted to `datetime`.
    """
    if isinstance(value, datetime):
        return value
    try:
        return parse_datetime(unicode(value))
    except TypeError:  # Unable to convert value to datetime
        raise ValueError('Invalid literal for datetime: {}'.format(value))


BASE_CHECKERS['Datetime'] = is_datetime
BASE_CONVERTERS['Datetime'] = date_time
