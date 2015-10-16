#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_netuitive
----------------------------------

Tests for `netuitive` module.
"""

import unittest
import json
import time
import netuitive


class TestClientInit(unittest.TestCase):

    def setUp(self):
        pass

    def test_custom_endpoint(self):

        # test custom endpoint url creation
        a = netuitive.Client('https://example.com/ingest', 'apikey')
        self.assertEqual(a.url, 'https://example.com/ingest')
        self.assertEqual(a.api_key, 'apikey')
        self.assertEqual(a.dataurl, 'https://example.com/ingest/apikey')
        self.assertEqual(
            a.eventurl, 'https://example.com/ingest/events/apikey')

    def test_infrastructure_endpoint(self):

        # test infrastructure endpoint url creation
        a = netuitive.Client(
            'https://example.com/ingest/infrastructure', 'apikey')
        self.assertEqual(a.url, 'https://example.com/ingest/infrastructure')
        self.assertEqual(a.api_key, 'apikey')
        self.assertEqual(
            a.dataurl, 'https://example.com/ingest/infrastructure/apikey')
        self.assertEqual(
            a.eventurl, 'https://example.com/ingest/events/infrastructure/apikey')

    def test_minimum(self):

        # test infrastructure endpoint url creation
        a = netuitive.Client(api_key='apikey')
        self.assertEqual(a.url, 'https://api.app.netuitive.com/ingest')
        self.assertEqual(a.api_key, 'apikey')
        self.assertEqual(
            a.dataurl, 'https://api.app.netuitive.com/ingest/apikey')
        self.assertEqual(
            a.eventurl, 'https://api.app.netuitive.com/ingest/events/apikey')

    def test_trailing_slash(self):

        # test negation of trailing / on the url
        a = netuitive.Client('https://example.com/ingest/', 'apikey')
        self.assertEqual(a.url, 'https://example.com/ingest')
        self.assertEqual(a.api_key, 'apikey')
        self.assertEqual(a.dataurl, 'https://example.com/ingest/apikey')
        self.assertEqual(
            a.eventurl, 'https://example.com/ingest/events/apikey')

    def tearDown(self):
        pass


class TestElementInit(unittest.TestCase):

    def setUp(self):
        pass

    def test_no_args(self):
        a = netuitive.Element()
        self.assertEqual(a.type, 'SERVER')

    def test_element_type(self):
        a = netuitive.Element('NOT_SERVER')
        self.assertEqual(a.type, 'NOT_SERVER')

    def tearDown(self):
        pass


class TestElementAttributes(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        a = netuitive.Element()
        a.add_attribute('Test', 'TestValue')
        self.assertEqual(a.attributes[0].name, 'Test')
        self.assertEqual(a.attributes[0].value, 'TestValue')

    def tearDown(self):
        pass


class TestElementTags(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        a = netuitive.Element()
        a.add_tag('Test', 'TestValue')

        self.assertEqual(a.tags[0].name, 'Test')
        self.assertEqual(a.tags[0].value, 'TestValue')

    def tearDown(self):
        pass


class TestElementSamples(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_sample(self):
        a = netuitive.Element()
        a.add_sample(
            'metricId', 1434110794, 1, 'COUNTER', host='hostname')

        self.assertEqual(a.id, 'hostname')
        self.assertEqual(a.name, 'hostname')

        self.assertEqual(a.metrics[0].id, 'metricId')
        self.assertEqual(a.metrics[0].type, 'COUNTER')

    def test_duplicate_metrics(self):
        a = netuitive.Element()

        a.add_sample(
            'metricId', 1434110794, 1, 'COUNTER', host='hostname')

        # don't allow duplicate metrics
        self.assertEqual(len(a.metrics), 1)

        self.assertEqual(a.samples[0].metricId, 'metricId')
        self.assertEqual(a.samples[0].timestamp, 1434110794000)
        self.assertEqual(a.samples[0].val, 1)

    def test_clear_samples(self):
        a = netuitive.Element()
        a.add_sample(
            'metricId', 1434110794, 1, 'COUNTER', host='hostname')
        # test clear_samples
        self.assertEqual(len(a.metrics), 1)
        a.clear_samples()
        self.assertEqual(len(a.metrics), 0)
        self.assertEqual(len(a.samples), 0)

    def test_with_sparseDataStrategy(self):
        a = netuitive.Element()

        # test sparseDataStrategy
        a.add_sample(
            'nonsparseDataStrategy', 1434110794, 1, 'COUNTER', host='hostname')
        a.add_sample(
            'sparseDataStrategy', 1434110794, 1, 'COUNTER', host='hostname', sparseDataStrategy='ReplaceWithZero')

        self.assertEqual(a.metrics[0].sparseDataStrategy, 'None')
        self.assertEqual(
            a.metrics[1].sparseDataStrategy, 'ReplaceWithZero')

        a.clear_samples()

    def test_with_unit(self):
        a = netuitive.Element()

        # test unit
        a.add_sample(
            'unit', 1434110794, 1, 'COUNTER', host='hostname', unit='Bytes')

        a.add_sample(
            'nonunit', 1434110794, 1, 'COUNTER', host='hostname')

        self.assertEqual(
            a.metrics[0].unit, 'Bytes')

        self.assertEqual(a.metrics[1].unit, '')

    def test_post_format(self):
        a = netuitive.Element()

        # test post format for element
        a = netuitive.Element()

        a.add_sample(
            'nonsparseDataStrategy', 1434110794, 1, 'COUNTER', host='hostname')
        a.add_sample(
            'sparseDataStrategy', 1434110794, 1, 'COUNTER', host='hostname', sparseDataStrategy='ReplaceWithZero')

        a.add_sample(
            'unit', 1434110794, 1, 'COUNTER', host='hostname', unit='Bytes')

        a.add_sample(
            'nonunit', 1434110794, 1, 'COUNTER', host='hostname')

        ajson = json.dumps(
            [a], default=lambda o: o.__dict__, sort_keys=True)
        j = '[{"attributes": [], "id": "hostname", "metrics": [{"id": "nonsparseDataStrategy", "sparseDataStrategy": "None", "type": "COUNTER", "unit": ""}, {"id": "sparseDataStrategy", "sparseDataStrategy": "ReplaceWithZero", "type": "COUNTER", "unit": ""}, {"id": "unit", "sparseDataStrategy": "None", "type": "COUNTER", "unit": "Bytes"}, {"id": "nonunit", "sparseDataStrategy": "None", "type": "COUNTER", "unit": ""}], "name": "hostname", "samples": [{"metricId": "nonsparseDataStrategy", "timestamp": 1434110794000, "val": 1}, {"metricId": "sparseDataStrategy", "timestamp": 1434110794000, "val": 1}, {"metricId": "unit", "timestamp": 1434110794000, "val": 1}, {"metricId": "nonunit", "timestamp": 1434110794000, "val": 1}], "tags": [], "type": "SERVER"}]'

        self.assertEqual(ajson, j)

    def tearDown(self):
        pass


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.everything = netuitive.Event('elementId', 'INFO', 'title', 'message', 'INFO',
                                          [('name0', 'value0'), ('name1', 'value1')], 1434110794, 'source')

        self.notags = netuitive.Event(
            'elementId', 'INFO', 'title', 'message', 'INFO', timestamp=1434110794, source='source')

        self.minimum = netuitive.Event(
            'elementId', 'INFO', 'title', 'message', 'INFO')

        self.everythingjson = json.dumps(
            [self.everything], default=lambda o: o.__dict__, sort_keys=True)

        self.notagsjson = json.dumps(
            [self.notags], default=lambda o: o.__dict__, sort_keys=True)

        self.minimumjson = json.dumps(
            [self.minimum], default=lambda o: o.__dict__, sort_keys=True)

    def test_all_options(self):

        # test event with all options

        self.assertEqual(self.everything.eventType, 'INFO')
        self.assertEqual(self.everything.title, 'title')
        self.assertEqual(self.everything.timestamp, 1434110794000)
        self.assertEqual(self.everything.tags[0].name, 'name0')
        self.assertEqual(self.everything.tags[0].value, 'value0')
        self.assertEqual(self.everything.tags[1].name, 'name1')
        self.assertEqual(self.everything.tags[1].value, 'value1')

        data = self.everything.data
        self.assertEqual(data.elementId, 'elementId')
        self.assertEqual(data.level, 'INFO')
        self.assertEqual(data.message, 'message')

    def test_no_tags(self):

        # test event without tags

        self.assertEqual(self.notags.eventType, 'INFO')
        self.assertEqual(self.notags.title, 'title')
        self.assertEqual(self.notags.timestamp, 1434110794000)
        self.assertEqual(hasattr(self.notags, 'tags'), False)

        data = self.notags.data
        self.assertEqual(data.elementId, 'elementId')
        self.assertEqual(data.level, 'INFO')
        self.assertEqual(data.message, 'message')

    def test_minimum(self):

        # test event with minimum options

        shouldbetrue = False
        t = int(time.time()) * 1000

        # minimum.timstamp has to be within the 10 second
        if t - 10000 < int(self.minimum.timestamp):
            shouldbetrue = True

        self.assertTrue(shouldbetrue)
        self.assertEqual(self.minimum.title, 'title')
        self.assertEqual(self.minimum.eventType, 'INFO')

        data = self.minimum.data
        self.assertEqual(data.elementId, 'elementId')
        self.assertEqual(data.level, 'INFO')
        self.assertEqual(data.message, 'message')

    def test_post_format(self):

        # test post format for event with all options

        j = '[{"data": {"elementId": "elementId", "level": "INFO", "message": "message"}, "eventType": "INFO", "source": "source", "tags": [{"name": "name0", "value": "value0"}, {"name": "name1", "value": "value1"}], "timestamp": 1434110794000, "title": "title"}]'

        self.assertEqual(self.everythingjson, j)

        # test post format for event without tags

        j = '[{"data": {"elementId": "elementId", "level": "INFO", "message": "message"}, "eventType": "INFO", "source": "source", "timestamp": 1434110794000, "title": "title"}]'

        self.assertEqual(self.notagsjson, j)

        # test post format for event with minimum options

        j = '[{"data": {"elementId": "elementId", "level": "INFO", "message": "message"}, "eventType": "INFO", "timestamp": ' + \
            str(self.minimum.timestamp) + ', "title": "title"}]'

        self.assertEqual(self.minimumjson, j)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
