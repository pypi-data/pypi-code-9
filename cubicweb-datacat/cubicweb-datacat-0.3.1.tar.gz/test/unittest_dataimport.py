# -*- coding: utf-8 -*-
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

"""Tests for data import of DCAT entities."""

from datetime import date, datetime
from io import StringIO
from urllib2 import HTTPError, URLError

from logilab.common.testlib import TestCase
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.devtools import TestServerConfiguration
from cubicweb.schema import CubicWebSchemaLoader

from cubicweb.dataimport import RQLObjectStore

# XXX: rdfio library is currently in the SKOS cube but should move to CubicWeb.
# This will remove dependency on SKOS cube.
from cubes.skos.rdfio import ExtEntity, RDFLibRDFGraph

# XXX: SimpleImportLog class is currently in the SKOS cube but should move to CubicWeb.
# This will remove dependency on SKOS cube.
from cubes.skos.dataimport import SimpleImportLog

from cubes.datacat.dataimport import (fetch_rdf_dcat_ext_entities, import_dcat_ext_entities,
                                      _load_rdf, valid_value_for_schema, valid_extentity_for_schema)


# The three following functions are a hack because ExtEntity does not define __eq__
def are_equal(ext_entity1, ext_entity2):
    """Returns ``True`` if the two given external entities are equal.

    Equality means ext entities have same extid, same etype, and same values
    """
    return (ext_entity1.extid == ext_entity2.extid
            and ext_entity1.etype == ext_entity2.etype
            and ext_entity1.values == ext_entity2.values)


def found_in(ext_entity, ext_entities):
    """Returns ``True`` if the given ext entity is equal to one of the ext entities in the given
    iterable."""
    for other_ext_entity in ext_entities:
        if are_equal(ext_entity, other_ext_entity):
            return True
    return False


def same_ext_entities(ext_entities, expected_ext_entities):
    """Returns a 2-uple ``(bool, msg)`` depending on ext entities in both iterables.

    If both iterables contains the same ext entities, returns ``(True, 'Same ext entities')``.

    If not, returns ``(False, msg)`` where ``msg`` explains what is the problem.
    """
    i = 0  # Just in case there is nothing in ext_entities, next if will not fail
    for i, ext_entity in enumerate(ext_entities, 1):
        if not found_in(ext_entity, expected_ext_entities):
            return False, u'Ext entity {} in first variable not found in second one.'.format(
                ext_entity.extid)
    if i == len(expected_ext_entities):
        return True, u'Same ext entities'
    else:
        return False, u'There are ext entities in second variable not found in first one.'


def same_entities(eids, expected, cnx):
    """Returns a 2-uple ``(bool, msg)`` depending on entities given by their eids.

    Returns ``(True, 'Same entities')`` if the entities match the given expected values.

    Returns ``(False, msg)`` in the other case.

    ``expected`` parameter is a dictionary with the following format.

    .. code-block:: python

        {<cwuri>:
            (<etype>,
            {<attr1>: set([<value1>]),
             <attr2>: set([<value2>]),
             <rel1>: set([<eid1>, <eid2>]),
            ...
            })
        }

    ``cnx`` is the connection object to CubicWeb used to get an entity from its eid.
    """
    if len(eids) != len(expected):
        return False, u'Not the same number of entities'
    for eid in eids:
        entity = cnx.entity_from_eid(eid)
        uri = entity.cwuri
        expected_type, expected_values = expected[uri]
        # Check type
        if entity.cw_etype != expected_type:
            return False, u"Not same type '{}' & '{}' for entity {}".format(
                entity.cw_etype, expected_type, uri)
        # Check attributes and relations
        for attr, expected_value in expected_values.iteritems():
            value = getattr(entity, attr)
            if isinstance(value, (list, tuple)):  # attr is a relation
                value = set([rel_entity.cwuri for rel_entity in value])
            else:
                value = set([value])
            if value != expected_value:
                return False, u"Not same value '{}' & '{}' for attribute '{}' on entity {}".format(
                    value, expected_value, attr, uri)
    return True, u'Same entities'


def harvest_rdf_dcat_check(uri, expected_ext_entities, expected_entities, schema, dcat_meta_uri,
                           cnx):
    """Returns a 2-uple ``(bool, msg)`` depending if harvesting given URI leads to expected results.

    Returns ``(True, 'Same entities')`` if all steps of harvesting went fine.

    Returns ``(False, msg)`` in every other case:

    * if fetching data from URI doesn't give expected external entities,
    * or if importing ext entities doesn't give expected entities.

    ``expected_ext_entities`` parameter is an iterable of ext entities.

    ``expected_entities`` parameter is a dictionary with the following format.

    .. code-block:: python

        {<cwuri>:
            (<etype>,
            {<attr1>: set([<value1>]),
             <attr2>: set([<value2>]),
             <rel1>: set([<eid1>, <eid2>]),
            ...
            })
        }

    ``schema`` is the CubicWeb schema to which ext entities and entities are related.

    ``dcat_meta_uri`` is the URI where definitions of DCAT terms (OWL definitions) can be found.

    ``cnx`` is the connection object to CubicWeb used to get an entity from its eid.
    """
    # Harvest the sample catalog and check found ext entities
    # ext entities are stored into a list because there will be multiple iterations on them
    ext_entities = list(fetch_rdf_dcat_ext_entities(uri, schema, dcat_meta_uri, rdf_format='n3'))
    result, msg = same_ext_entities(ext_entities, expected_ext_entities)
    if not result:
        return result, msg
    # Import ext entities into database using a store
    store = RQLObjectStore(cnx=cnx)
    import_log = SimpleImportLog(StringIO())
    created, _ = import_dcat_ext_entities(ext_entities, store, cnx,
                                          import_log=import_log)
    return same_entities(created, expected_entities, cnx)


#
# Actual test cases
#

class RDFDCATDataImportTC(CubicWebTC):
    """Import of RDF DCAT data test case."""

    def test_import_simple_clean_data(self):
        """Test importing simple and clean RDF DCAT data."""
        # Sample catalog and datasets
        dcat_uri = u'file://' + self.datapath('dcat.n3')
        dset1_uri = u'file://' + self.datapath('dset1.n3')
        dset2_uri = u'file://' + self.datapath('dset2.n3')
        dset3_uri = u'file://' + self.datapath('dset3.n3')
        dset4_uri = u'file://' + self.datapath('dset4.n3')
        # Data in catalog and datasets
        expected_entities = {
            dcat_uri: (
                'DataCatalog',
                {
                    'title': set([u'ODP EU']),
                    'issued': set([datetime(2015, 1, 9, 20, 0)]),
                }
            ),
            dset1_uri: (
                'Dataset',
                {
                    'title': set([u'Special Eurobarometer 376: Women in decision-making '
                                  'positions']),
                    'issued': set([datetime(2014, 12, 11, 20, 0)]),
                    'in_catalog': set([dcat_uri]),
                }),
            dset2_uri: (
                'Dataset',
                {
                    'title': set([u'Test data for small punch fracture on material P91 wm at -192 '
                                  'Celsius and a displacement rate of 0.003 mm/s (first repeat '
                                  'test)']),
                    'issued': set([datetime(2013, 12, 20, 20, 0)]),
                    'in_catalog': set([dcat_uri]),
                }),
            dset3_uri: (
                'Dataset',
                {
                    'title': set([u"Individuals' level of internet skills"]),
                    'issued': set([datetime(2014, 12, 16, 20, 0)]),
                    'in_catalog': set([dcat_uri]),
                }),
            dset4_uri: (
                'Dataset',
                {
                    u'title': set(['Erasmus mobility statistics 2012-13']),
                    'issued': set([datetime(2014, 11, 13, 20, 0)]),
                    'in_catalog': set([dcat_uri]),
                }),
            u'file://' + self.datapath('dist1-1.n3'): (
                'Distribution',
                {
                    'title': set([u'Detailed information on public opinion website']),
                    'issued':  set([datetime(2015, 1, 8, 12, 11, 14, 272879)]),
                    'of_dataset': set([dset1_uri]),
                }),
            u'file://' + self.datapath('dist1-2.n3'): (
                'Distribution',
                {
                    'title': set([u'Link to OP_VolumeAEB761DGJustWomen20110923.zip']),
                    'issued':  set([datetime(2015, 1, 8, 12, 11, 14, 272954)]),
                    'of_dataset': set([dset1_uri]),
                }),
            u'file://' + self.datapath('dist2-1.n3'): (
                'Distribution',
                {
                    'title': set([u'XML File']),
                    'issued': set([datetime(2014, 8, 13, 15, 7, 1, 122391)]),
                    'of_dataset': set([dset2_uri]),
                }),
            u'file://' + self.datapath('dist3-1.n3'): (
                'Distribution',
                {
                    'title': set([u'Zip File']),
                    'issued':  set([datetime(2014, 12, 22, 10, 57, 8, 360289)]),
                    'of_dataset': set([dset3_uri]),
                }),
            u'file://' + self.datapath('dist3-2.n3'): (
                'Distribution',
                {
                    'title': set([u'More information on Eurostat Website']),
                    'issued':  set([datetime(2014, 12, 22, 10, 57, 8, 360264)]),
                    'of_dataset': set([dset3_uri]),
                }),
            u'file://' + self.datapath('dist4-1.n3'): (
                'Distribution',
                {
                    u'title': set(['Zip File']),
                    'issued':  set([datetime(2014, 11, 18, 11, 36, 37, 830297)]),
                    'of_dataset': set([dset4_uri]),
                }),
            u'file://' + self.datapath('dist4-2.n3'): (
                'Distribution',
                {
                    'title': set([u'Comma Seperated Values File']),
                    'issued':  set([datetime(2014, 11, 18, 11, 36, 37, 830334)]),
                    'of_dataset': set([dset4_uri]),
                }),
        }
        expected_ext_entities = [ExtEntity(etype, uri, values)
                                 for uri, (etype, values) in expected_entities.iteritems()]
        with self.admin_access.repo_cnx() as cnx:
            result, msg = harvest_rdf_dcat_check(dcat_uri, expected_ext_entities, expected_entities,
                                                 self.vreg.schema, self.datapath('dcat.ttl'), cnx)
            self.assertTrue(result, msg)

    def test_import_multi_root_rdf_dcat(self):
        """Test importing RDF DCAT data whith multiple root nodes.

        Namely, check import of multiple catalogs and dataset which is not linked to any catalog.
        """
        # Sample catalog and datasets
        dcat_uri = u'file://' + self.datapath('dcata.n3')
        cat1_uri = u'file://' + self.datapath('cat1a.n3')
        cat2_uri = u'file://' + self.datapath('cat2a.n3')
        dset1_uri = u'file://' + self.datapath('dset1a.n3')
        dset2_uri = u'file://' + self.datapath('dset2a.n3')
        # Data in catalog and datasets
        expected_entities = {
            cat1_uri: (
                'DataCatalog',
                {
                    'title': set([u'ODP EU']),
                    'issued': set([datetime(2015, 1, 9, 20, 0)]),
                }),
            cat2_uri: (
                'DataCatalog',
                {
                    'title': set([u'ODP EU 2']),
                    'issued': set([datetime(2015, 4, 1, 20, 0)]),
                }),
            dset1_uri: (
                'Dataset',
                {
                    'title': set([u'Special Eurobarometer 376: Women in decision-making '
                                  'positions']),
                    'issued': set([datetime(2014, 12, 11, 20, 0)]),
                    'in_catalog': set([cat1_uri]),
                }),
            dset2_uri: (  # Standalone dataset
                'Dataset',
                {
                    'title': set([u'Test data for small punch fracture on material P91 wm at -192 '
                                  'Celsius and a displacement rate of 0.003 mm/s (first repeat '
                                  'test)']),
                    'issued': set([datetime(2013, 12, 20, 20, 0)]),
                }),
            u'file://' + self.datapath('dist1-1a.n3'): (
                'Distribution',
                {
                    'title': set([u'Detailed information on public opinion website']),
                    'issued': set([datetime(2015, 1, 8, 12, 11, 14, 272879)]),
                    'of_dataset': set([dset1_uri]),
                }),
            u'file://' + self.datapath('dist1-2a.n3'): (
                'Distribution',
                {
                    'title': set([u'Link to OP_VolumeAEB761DGJustWomen20110923.zip']),
                    'issued': set([datetime(2015, 1, 8, 12, 11, 14, 272954)]),
                    'of_dataset': set([dset1_uri]),
                }),
            u'file://' + self.datapath('dist2-1a.n3'): (
                'Distribution',
                {
                    'title': set([u'XML File']),
                    'issued': set([datetime(2014, 8, 13, 15, 7, 1, 122391)]),
                    'of_dataset': set([dset2_uri]),
                }),
        }
        expected_ext_entities = [ExtEntity(etype, uri, values)
                                 for uri, (etype, values) in expected_entities.iteritems()]
        with self.admin_access.repo_cnx() as cnx:
            result, msg = harvest_rdf_dcat_check(dcat_uri, expected_ext_entities, expected_entities,
                                                 self.vreg.schema, self.datapath('dcat.ttl'), cnx)
            self.assertTrue(result, msg)

    def test_import_problematic_rdf_dcat(self):
        """Test import of RDF DCAT data with commonly encountered problems."""
        # Sample catalog and datasets
        dcat_uri = u'file://' + self.datapath('dcatb.n3')
        dset1_uri = u'file://' + self.datapath('dset1b.n3')
        dset3_uri = u'file://' + self.datapath('dset3b.n3')
        dist1_1_uri = u'file://' + self.datapath('dist1-1b.n3')
        dist1_2_uri = u'file://' + self.datapath('dist1-2b.n3')
        dist3_1_uri = u'file://' + self.datapath('dist3-1b.n3')
        dist3_2_uri = u'file://' + self.datapath('dist3-2b.n3')
        # Expected final entities after import with cleaned attributes and discarded ext entities
        expected_entities = {
            dcat_uri: (
                'DataCatalog',
                {
                    'title': set([u'ODP EU']),
                    'issued': set([datetime(2015, 1, 9, 20, 0)]),
                }),
            dset1_uri: (
                'Dataset',
                {
                    'title': set([u'Special Eurobarometer 376: Women in decision-making '
                                  'positions']),
                    'issued': set([datetime(2014, 12, 11, 20, 0)]),
                    'in_catalog': set([dcat_uri]),
                }),
            dist1_1_uri: (
                'Distribution',
                {
                    'title': set([u'Detailed information on public opinion website']),
                    'of_dataset': set([dset1_uri]),
                }),
            dist1_2_uri: (
                'Distribution',
                {
                    'of_dataset': set([dset1_uri]),
                }),
        }
        # Expected ext entities
        expected_fetch = expected_entities.copy()
        expected_fetch[dist3_1_uri] = (  # Fetched but not imported since dset3 is discarded
            'Distribution',
            {
                'of_dataset': set([dset3_uri]),
            })
        expected_fetch[dist3_2_uri] = (  # Same here
            'Distribution',
            {
                'title': set([u'More information on Eurostat Website']),
                'issued': set([datetime(2014, 12, 22, 10, 57, 8, 360264)]),
                'of_dataset': set([dset3_uri]),
            })
        expected_ext_entities = [ExtEntity(etype, uri, values)
                                 for uri, (etype, values) in expected_fetch.iteritems()]
        with self.admin_access.repo_cnx() as cnx:
            result, msg = harvest_rdf_dcat_check(dcat_uri, expected_ext_entities, expected_entities,
                                                 self.vreg.schema, self.datapath('dcat.ttl'), cnx)
            self.assertTrue(result, msg)


class WorkingWithRDFTC(TestCase):
    """Test case for working with RDF data."""

    def test_load_rdf(self):
        """Check if loading wrong URI error is catch."""
        # Invalid uris
        uri1 = u'file://' + self.datapath('wrong_file.n3')
        uri2 = u'http://www.example.org/wrong_uri.n3'
        uri3 = u'http://www.notadomain.org/wrong_uri.n3'
        # Check that the function does not raise any error, while the method do
        graph = RDFLibRDFGraph()
        with self.assertRaises(IOError):
            graph.load(uri1, rdf_format='n3')
        _load_rdf(graph, uri1, rdf_format='n3')
        with self.assertRaises(HTTPError):
            graph.load(uri2, rdf_format='n3')
        _load_rdf(graph, uri2, rdf_format='n3')
        with self.assertRaises(URLError):
            graph.load(uri3, rdf_format='n3')
        _load_rdf(graph, uri3, rdf_format='n3')
        # If asked, the function will raise the exception
        with self.assertRaises(IOError):
            _load_rdf(graph, uri1, rdf_format='n3', raise_on_error=True)
        with self.assertRaises(HTTPError):
            _load_rdf(graph, uri2, rdf_format='n3', raise_on_error=True)
        with self.assertRaises(URLError):
            _load_rdf(graph, uri3, rdf_format='n3', raise_on_error=True)


class ExtEntitySchemaConformTC(TestCase):
    """Tests for functions that makes external entities attributes conforming to a schema."""

    def setUp(self):
        schema_loader = CubicWebSchemaLoader()
        config = TestServerConfiguration()
        config.bootstrap_cubes()
        self.schema = schema_loader.load(config)
        self.eschema = self.schema.eschema('Thing')
        self.title_rschema = self.schema.rschema('title')
        self.issued_rschema = self.schema.rschema('issued')

    def test_conform_preserve_original(self):
        """Check that conform ext entity does not modify it"""
        etype = 'Thing'
        extid = 1
        values = {'title': set([u'Title']), 'child_of': set([2]), 'linked_to': set([3]),
                  'additional_attribute': set([u'value']), 'additional_relation': set([4])}
        expected_values = {'title': set([u'Title']), 'child_of': set([2]), 'linked_to': set([3])}
        ext_entity = ExtEntity(etype=etype, extid=extid, values=values)
        new_ext_entity = valid_extentity_for_schema(self.schema, ext_entity)
        # Original has not been modified
        self.assertEqual(ext_entity.etype, etype)
        self.assertEqual(ext_entity.extid, extid)
        self.assertEqual(ext_entity.values, values)
        # New one has information only relevant to schema
        self.assertEqual(new_ext_entity.etype, etype)
        self.assertEqual(new_ext_entity.extid, extid)
        self.assertEqual(new_ext_entity.values, expected_values)

    def test_conform_string(self):
        """Check conform string attribute"""
        valid_values = set([u'3.14'])
        ext_entity = ExtEntity(etype='Thing', extid=1)
        ext_entity.values['title'] = set([3.14])  # float will be cast to string
        # Check valid value computation
        rname, values = valid_value_for_schema(self.eschema, self.title_rschema, ext_entity)
        self.assertEqual(rname, 'title')
        self.assertEqual(values, valid_values)

    def test_conform_multiple_strings(self):
        """Check conform string attribute when having multiple values"""
        valid_values = set([u'A String', u'Other String'])
        ext_entity = ExtEntity(etype='Thing', extid=2)
        ext_entity.values['title'] = valid_values
        # Check valid value computation
        rname, values = valid_value_for_schema(self.eschema, self.title_rschema, ext_entity)
        self.assertEqual(rname, 'title')
        self.assertLess(values, valid_values)

    def test_conform_datetime(self):
        """Check conform datetime attribute"""
        dt1 = datetime(2015, 1, 1, 20, 0)
        valid_values = set([dt1])
        ext_entity = ExtEntity(etype='Thing', extid=4, values={'title': u'Title'})
        ext_entity.values['issued'] = set([dt1.isoformat()])  # str will be cast to datetime
        # Check valid value computation
        rname, values = valid_value_for_schema(self.eschema, self.issued_rschema, ext_entity)
        self.assertEqual(rname, 'issued')
        self.assertEqual(values, valid_values)

    def test_conform_multiple_datetimes(self):
        """Check conform datetime attribute when having multiple values"""
        dt1 = datetime(2015, 1, 1, 20, 0)
        dt2 = datetime(2015, 1, 2, 20, 0)
        valid_values = set([dt1, dt2])
        ext_entity = ExtEntity(etype='Thing', extid=5, values={'title': u'Title'})
        ext_entity.values['issued'] = valid_values
        # Check valid value computation
        rname, values = valid_value_for_schema(self.eschema, self.issued_rschema, ext_entity)
        self.assertEqual(rname, 'issued')
        self.assertLess(values, valid_values)

    def test_conform_wrong_datetime(self):
        """Check conform datetime attribute with wrong value"""
        ext_entity = ExtEntity(etype='Thing', extid=6, values={'title': u'Title'})
        ext_entity.values['issued'] = set(["two thousand"])
        # Check valid value computation
        rname, values = valid_value_for_schema(self.eschema, self.issued_rschema, ext_entity)
        self.assertEqual(rname, 'issued')
        self.assertEqual(values, set())
        # Check attribute has been discarded
        ext_entity = valid_extentity_for_schema(self.schema, ext_entity)
        self.assertNotIn('issued', ext_entity.values)

    def test_conform_datetime_from_other_type(self):
        """Check conform datetime attribute when value is neither datetime nor string."""
        ext_entity = ExtEntity(etype='Thing', extid=6, values={'title': u'Title'})
        dt1 = datetime(2015, 1, 1, 0, 0)
        d1 = date(2015, 1, 1)
        valid_values = set([dt1])
        ext_entity.values['issued'] = set([d1])
        # Check valid value computation
        rname, values = valid_value_for_schema(self.eschema, self.issued_rschema, ext_entity)
        self.assertEqual(rname, 'issued')
        self.assertEqual(values, valid_values)

    def test_conform_multiple_datetimes_with_wrong(self):
        """Check conform datetime attribute when having multiple values, some of them are wrong"""
        dt1 = datetime(2015, 1, 1, 20, 0)
        valid_values = set([dt1])
        ext_entity = ExtEntity(etype='Thing', extid=7, values={'title': u'Title'})
        ext_entity.values['issued'] = set(["two thousand", dt1.isoformat()])
        rname, values = valid_value_for_schema(self.eschema, self.issued_rschema, ext_entity)
        self.assertEqual(rname, 'issued')
        self.assertEqual(values, valid_values)

    def test_conform_missing_required_attribute(self):
        """Check conform ext entity missing required attribute"""
        dt1 = datetime(2015, 1, 1, 20, 0)
        ext_entity = ExtEntity(etype='Thing', extid=8)
        ext_entity.values['issued'] = set([dt1])
        # Check valid value computation
        rname, values = valid_value_for_schema(self.eschema, self.title_rschema, ext_entity)
        self.assertIsNone(rname)
        self.assertIsNone(values)
        rname, values = valid_value_for_schema(self.eschema, self.issued_rschema, ext_entity)
        self.assertEqual(rname, 'issued')
        self.assertEqual(values, set([dt1]))
        # Check ext entity has been discarded
        self.assertIsNone(valid_extentity_for_schema(self.schema, ext_entity))


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
