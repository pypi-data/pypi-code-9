# -*- coding: utf-8 -*-
import copy
import types
import re
from promises.csv_loader.creator import PromiseCreator
from promises.csv_loader import HEADER_TYPES, CREATION_ORDER, match_with


class HeaderReader():
    def __init__(self, headers=None):
        self.headers = headers
        self.instructions = {}

        for column_number in range(len(self.headers)):
            key_and_instruction = self.what_to_do_with_column(column_number)
            if key_and_instruction is None:
                continue
            key, instruction = key_and_instruction
            if key not in self.instructions.keys():
                self.instructions[key] = {}
                setattr(self, key, self.instructions[key])
                def make_get_kwargs(k):
                    def f(self, row):
                        return self.get_kwargs_for(getattr(self, k), row)
                    return f
                setattr(self, "get_" + key + "s", types.MethodType(make_get_kwargs(key), self))
            self.instructions[key][column_number] = instruction

    def get_creation_instructions(self):
        order = []
        for item in CREATION_ORDER:
            instruction = {}
            instruction['creation_method'] = 'create_' + item['name']
            instruction['kwargs_getter'] = 'get_' + item['name'] + '_kwargs'
            instruction['multiple'] = item['multiple']
            order.append(instruction)
        return order

    def get_kwargs_for(self, dictionary, row):
        kwargs = {}
        for key in dictionary.keys():
            instruction = dictionary[key]
            if isinstance(dictionary[key], dict):
                kwargs[key] = {}
                kwargs[key][instruction['use_this_as']] = row[key]
                other_index = self.headers.index(instruction['match_with'])
                kwargs[key][instruction['use_other_as']] = row[other_index]
            else:
                kwargs[dictionary[key]] = row[key]
        return kwargs

    def what_to_do_with_column(self, column_number):
        for key in HEADER_TYPES.keys():
            pattern = re.compile(key)
            if pattern.search(self.headers[column_number]):
                instruction_alias = self.headers[column_number]
                instruction = instruction_alias
                raw_instructions = copy.copy(HEADER_TYPES[key])
                if 'as' in raw_instructions.keys():
                    instruction = raw_instructions['as']
                if 'match' in raw_instructions.keys():
                    the_match =  match_with(raw_instructions['match'], instruction_alias)
                    raw_instructions['match_with'] = the_match
                    instruction = raw_instructions
                return HEADER_TYPES[key]['what'], instruction

class RowProcessor():
    def __init__(self, rows, reader_class=HeaderReader, creator_class=PromiseCreator, **kwargs):
        self.reader_class = reader_class
        self.creator_class = creator_class
        self.creator = self.creator_class(**kwargs)
        self.header_reader = self.reader_class(rows[0])
        self.rows = rows[1:]
        self.warnings = []

    def read_row(self, row):
        order = self.header_reader.get_creation_instructions()
        for instruction in order:
            getter = getattr(self.header_reader, instruction['kwargs_getter'])
            kwargs = getter(row)
            creator_method = getattr(self.creator, instruction['creation_method'])
            if instruction['multiple']:
                for index in kwargs:
                    creator_method(**kwargs[index])
            else:
                creator_method(**kwargs)
            if self.creator.warnings is not None:
                self.warnings = self.warnings + self.creator.warnings

    def process(self):
        for row in self.rows:
            self.read_row(row)
