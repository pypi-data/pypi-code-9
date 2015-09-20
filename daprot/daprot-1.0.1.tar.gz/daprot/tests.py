
# -*- coding: utf-8 -*-

"""
daprot is a data flow prototyper and mapper library.
Copyright (C) 2015, Bence Faludi (bence@ozmo.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

import unittest
import datetime
import daprot as dp

class TestSchemaFlowClass(unittest.TestCase):
    class BasicSchema(dp.SchemaFlow):
        id = dp.Field()
        name = dp.Field()
        created_at = dp.Field()

    def setUp(self):
        self.list_data = [
            ['1', 'apple', '2014-05-06 17:22:32'],
            ['3', 'orange', '2015-02-01 13:42:32'],
            ['4', 'banana', '2015-04-07 11:06:51'],
            ['  5 ', '  ', '2015-06-20'],
            [' 9 ', '  grape', '2012-01-01 00:00:00'],
        ]

    def test_iteratable_ability(self):
        self.assertEqual(
            [ element for element in self.BasicSchema(self.list_data) ],
            list(self.BasicSchema(self.list_data))
        )

    def test_length(self):
        self.assertEqual(5, len(list(self.BasicSchema(self.list_data))))

    def test_offset(self):
        self.assertEqual(3, len(list(self.BasicSchema(self.list_data, offset=2))))

    def test_limit(self):
        self.assertEqual(2, len(list(self.BasicSchema(self.list_data, limit=2))))

    def test_offset_limit(self):
        self.assertEqual(2, len(list(self.BasicSchema(self.list_data, offset=2, limit=2))))

class TestSchemaFlowClassWithoutRoute(unittest.TestCase):
    class BasicSchema(dp.SchemaFlow):
        id = dp.Field()
        name = dp.Field()
        created_at = dp.Field()

    def setUp(self):
        self.list_data = [
            ['1', 'apple', '2014-05-06 17:22:32'],
            ['3', 'orange', '2015-02-01 13:42:32'],
            ['4', 'banana', '2015-04-07 11:06:51'],
            ['  5 ', '  ', '2015-06-20'],
            [' 9 ', '  grape', '2012-01-01 00:00:00'],
        ]
        
        self.dict_data = [
            {'created_at': '2014-05-06 17:22:32', 'id': '1', 'name': 'apple'},
            {'created_at': '2015-02-01 13:42:32', 'id': '3', 'name': 'orange'},
            {'created_at': '2015-04-07 11:06:51', 'id': '4', 'name': 'banana'},
            {'created_at': '2015-06-20', 'id': '  5 ', 'name': '  '},
            {'created_at': '2012-01-01 00:00:00', 'id': ' 9 ', 'name': '  grape'},
        ]

    def test_index_mapper_on_list(self):
        self.assertEqual([
            {'created_at': '2014-05-06 17:22:32', 'id': '1', 'name': 'apple'},
            {'created_at': '2015-02-01 13:42:32', 'id': '3', 'name': 'orange'},
            {'created_at': '2015-04-07 11:06:51', 'id': '4', 'name': 'banana'},
            {'created_at': '2015-06-20', 'id': '  5 ', 'name': '  '},
            {'created_at': '2012-01-01 00:00:00', 'id': ' 9 ', 'name': '  grape'}
        ], list(self.BasicSchema(self.list_data, mapper=dp.mapper.INDEX)))

    def test_name_mapper_on_list(self):
        self.assertEqual([
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None}
        ], list(self.BasicSchema(self.list_data, mapper=dp.mapper.NAME)) )

    def test_name_ignore_on_list(self):
        self.assertEqual([
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None}
        ], list(self.BasicSchema(self.list_data, mapper=dp.mapper.IGNORE)) )

    def test_without_mapper_on_list(self):
        self.assertEqual([
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None}
        ], list(self.BasicSchema(self.list_data)) )

    def test_index_mapper_on_dict(self):
        self.assertEqual([
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None}
        ], list(self.BasicSchema(self.dict_data, mapper=dp.mapper.INDEX)))

    def test_name_mapper_on_dict(self):
        self.assertEqual([
            {'created_at': '2014-05-06 17:22:32', 'id': '1', 'name': 'apple'},
            {'created_at': '2015-02-01 13:42:32', 'id': '3', 'name': 'orange'},
            {'created_at': '2015-04-07 11:06:51', 'id': '4', 'name': 'banana'},
            {'created_at': '2015-06-20', 'id': '  5 ', 'name': '  '},
            {'created_at': '2012-01-01 00:00:00', 'id': ' 9 ', 'name': '  grape'}
        ], list(self.BasicSchema(self.dict_data, mapper=dp.mapper.NAME)) )

    def test_name_ignore_on_dict(self):
        self.assertEqual([
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None}
        ], list(self.BasicSchema(self.dict_data, mapper=dp.mapper.IGNORE)) )

    def test_without_mapper_on_dict(self):
        self.assertEqual([
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None},
            {'created_at': None, 'id': None, 'name': None}
        ], list(self.BasicSchema(self.dict_data)) )

class TestSchemaFlowClassWithRoute(unittest.TestCase):
    class Schema(dp.SchemaFlow):
        id = dp.Field()
        name = dp.Field(route='title')
        created_at = dp.Field(route='other/date')
        updated_at = dp.Field(route='other/date')

    def setUp(self):
        self.dict_data = [
            {'other': {'date': '2014-05-06 17:22:32'}, 'id': '1', 'title': 'apple'},
            {'other': {'date': '2015-02-01 13:42:32'}, 'id': '3', 'title': 'orange'},
            {'other': {'date': '2015-04-07 11:06:51'}, 'id': '4', 'title': 'banana'},
            {'other': {'date': '2015-06-20'}, 'id': '  5 ', 'title': '  '},
            {'other': {'date': '2012-01-01 00:00:00'}, 'id': ' 9 ', 'title': '  grape'},
        ]

    def test_data_frame_after_mapping(self):
        self.assertEqual([
            {'updated_at': '2014-05-06 17:22:32', 'created_at': '2014-05-06 17:22:32', 'id': '1', 'name': 'apple'},
            {'updated_at': '2015-02-01 13:42:32', 'created_at': '2015-02-01 13:42:32', 'id': '3', 'name': 'orange'},
            {'updated_at': '2015-04-07 11:06:51', 'created_at': '2015-04-07 11:06:51', 'id': '4', 'name': 'banana'},
            {'updated_at': '2015-06-20', 'created_at': '2015-06-20', 'id': '  5 ', 'name': '  '},
            {'updated_at': '2012-01-01 00:00:00', 'created_at': '2012-01-01 00:00:00', 'id': ' 9 ', 'name': '  grape'}
        ], list(self.Schema(self.dict_data, mapper=dp.mapper.NAME)) )

    def test_data_frame_after_mapping_without_mapper(self):
        # Note: Because we did not defined the route of `id` field.
        self.assertEqual([
            {'updated_at': '2014-05-06 17:22:32', 'created_at': '2014-05-06 17:22:32', 'id': None, 'name': 'apple'},
            {'updated_at': '2015-02-01 13:42:32', 'created_at': '2015-02-01 13:42:32', 'id': None, 'name': 'orange'},
            {'updated_at': '2015-04-07 11:06:51', 'created_at': '2015-04-07 11:06:51', 'id': None, 'name': 'banana'},
            {'updated_at': '2015-06-20', 'created_at': '2015-06-20', 'id': None, 'name': '  '},
            {'updated_at': '2012-01-01 00:00:00', 'created_at': '2012-01-01 00:00:00', 'id': None, 'name': '  grape'}
        ], list(self.Schema(self.dict_data)) )

class TestSchemaFlowWithType(unittest.TestCase):
    class ValidSchema(dp.SchemaFlow):
        id = dp.Field(type=int)
        name = dp.Field(type=str)
        # Note: you can use dateutil package for this :)
        created_at = dp.Field(type=lambda x: datetime.date(*map(int,(x.split(' ',1)[0].split('-')))))

    def setUp(self):
        self.list_data = [
            ['1', 'apple', '2014-05-06 17:22:32'],
            ['3', 'orange', '2015-02-01 13:42:32'],
            ['4', 'banana', '2015-04-07 11:06:51'],
            ['  5 ', '  ', '2015-06-20'],
            [' 9 ', '  grape', '2012-01-01 00:00:00'],
        ]
        
        self.not_valid_list_data = [
            ['1', 'apple', '2014-05-06 17:22:32'],
            ['3', None, '2015-02-01 13:42:32'],
            ['4', 'banana', '2015-04-07 11:06:51'],
            ['  s5 ', None, '2015-06-20'],
            [' 9 ', '  grape', '2012-01-01 00:00:00'],
        ]

    def test_converted_value_on_valid_schema(self):
        self.assertEqual([
            {'created_at': datetime.date(2014,5,6), 'id': 1, 'name': 'apple'},
            {'created_at': datetime.date(2015,2,1), 'id': 3, 'name': 'orange'},
            {'created_at': datetime.date(2015,4,7), 'id': 4, 'name': 'banana'},
            {'created_at': datetime.date(2015,6,20), 'id': 5, 'name': '  '},
            {'created_at': datetime.date(2012,1,1), 'id': 9, 'name': '  grape'}
        ], list(self.ValidSchema(self.list_data, mapper=dp.mapper.INDEX)) )

    def test_value_will_be_hard_converted(self):
        # Note: None value will be converted to str.
        # You can use forcedtypes package instead of the std library.
        self.assertEqual([
            {'created_at': datetime.date(2015,2,1), 'id': 3, 'name': 'None'},
        ], list(self.ValidSchema(self.not_valid_list_data, mapper=dp.mapper.INDEX, limit=1, offset=1)) )

    def test_value_will_be_hard_converted(self):
        # Note: If a value is not convertable the flow will raise an exception.
        # You can use forcedtypes package instead of the std library.
        with self.assertRaises(ValueError):
            list(self.ValidSchema(self.not_valid_list_data, mapper=dp.mapper.INDEX))

class TestSchemaFlowWithDefaultValue(unittest.TestCase):
    class Schema(dp.SchemaFlow):
        date_start = dp.Field(route=2, default_value=datetime.datetime.now())
        date_current = dp.Field(route=2, default_value=datetime.datetime.now)

    def setUp(self):
        self.list_data = [
            ['1', 'apple', '2014-05-06 17:22:32'],
            ['3', 'orange', None],
            ['4', 'banana', ''],
            ['  5 ', '  ', None],
            [' 9 ', '  grape', '2012-01-01 00:00:00'],
        ]

    def test_filled_out_not_changed(self):
        data = list(self.Schema(self.list_data, mapper=dp.mapper.INDEX))
        self.assertEqual(data[0]['date_start'], data[0]['date_current'])
        self.assertEqual(data[0]['date_start'], '2014-05-06 17:22:32')

    def test_empty_not_changed(self):
        # Note: This package will not convert empty values into None
        # You can use forcedtypes package to force the types.
        data = list(self.Schema(self.list_data, mapper=dp.mapper.INDEX))
        self.assertEqual(data[2]['date_start'], data[2]['date_current'])
        self.assertEqual(data[2]['date_start'], '')

    def test_pre_evaulated_values_are_the_same(self):
        data = list(self.Schema(self.list_data, mapper=dp.mapper.INDEX))
        self.assertEqual(data[1]['date_start'], data[3]['date_start'])

    def test_not_pre_evaulated_values_are_different(self):
        data = list(self.Schema(self.list_data, mapper=dp.mapper.INDEX))
        self.assertNotEqual(data[1]['date_current'], data[3]['date_current'])

class TestSchemaFlowWithDefaultValue(unittest.TestCase):
    class Schema(dp.SchemaFlow):
        original_title = dp.Field(route=1, type=str)
        title = dp.Field(route=1, type=str, transforms=[str.strip, str.upper])

    def setUp(self):
        self.list_data = [
            ['1', 'apple', '2014-05-06 17:22:32'],
            ['3', 'orange', None],
            ['4', 'banana', ''],
            ['  5 ', '  ', None],
            [' 9 ', '  grape', '2012-01-01 00:00:00'],
        ]
    
    def test_transforms(self):
        data = list(self.Schema(self.list_data, mapper=dp.mapper.INDEX))
        self.assertEqual(data[-1]['original_title'], '  grape')
        self.assertEqual(data[-1]['title'], 'GRAPE')
