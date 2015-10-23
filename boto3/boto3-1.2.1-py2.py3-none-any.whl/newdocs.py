# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

"""
This module is used to generate both high and low-level reference
documentation for services. Currently, it does this by inspecting
the service and resource models, as well as instantiating dummy
clients to introspect some values. It is likely to change
significantly in the future!

Currently this is not used for docstrings, just for the Sphinx
documentation. RST is generated which Sphinx turns into HTML.

The generated output can be found here:

    http://boto3.readthedocs.org/en/latest/

"""
import inspect
from bcdoc.restdoc import DocumentStructure

from boto3.session import Session


def py_type_name(type_name):
    """
    Get the Python type name for a given model type.

        >>> py_type_name('list')
        'list'
        >>> py_type_name('structure')
        'dict'

    :rtype: string
    """
    return {
        'blob': 'bytes',
        'character': 'string',
        'double': 'float',
        'long': 'integer',
        'map': 'dict',
        'structure': 'dict',
        'timestamp': 'datetime',
    }.get(type_name, type_name)


def py_default(type_name):
    """
    Get the Python default value for a given model type, useful
    for generated examples.

        >>> py_default('string')
        '\'string\''
        >>> py_default('list')
        '[...]'
        >>> py_default('unknown')
        '...'

    :rtype: string
    """
    return {
        'double': '123.0',
        'long': '123',
        'integer': '123',
        'string': "'string'",
        'blob': "b'bytes'",
        'boolean': 'True|False',
        'list': '[...]',
        'map': '{...}',
        'structure': '{...}',
        'timestamp': 'datetime(2015, 1, 1)',
    }.get(type_name, '...')


class ServiceDocGenerator(object):
    def __init__(self, service_name):
        self.session = Session()
        self.botocore_session = self.session._session
        self.service_name = service_name
        self._official_name = None

        self.client = self.session.client(
            service_name, region_name='us-east-1', aws_access_key_id='foo',
            aws_secret_access_key='bar')

        self.sections = [
            'title',
            'table-of-contents',
            'client_api'
        ]

    @property
    def official_service_name(self):
        if self._official_name is None:
            official_name = self.client.meta.service_model.metadata.get(
                'serviceFullName')
            short_name = self.client.meta.service_model.metadata.get(
                'serviceAbbreviation', '')
            if short_name.startswith('Amazon'):
                short_name = short_name[7:]
            if short_name.startswith('AWS'):
                short_name = short_name[4:]
            if short_name and short_name.lower() not in official_name.lower():
                official_name += ' ({0})'.format(short_name)
            self._official_name = official_name
        return self._official_name

    def _register_sections(self):
        for section in self.sections:
            self.client.meta.events.register(
                'docs-adding-section.%s->%s' % (self.service_name, section),
                getattr(self, section.replace('-', '_')),
                unique_id='%s-%s' % (self.service_name, section))

    def generate_ref_api_docs(self):
        self._register_sections()
        doc_structure = DocumentStructure(
            self.service_name, self.client.meta.events,
            section_names=self.sections)
        return doc_structure.flush_structure()

    def title(self, section, **kwargs):
        section.style.h2(self.official_service_name)

    def table_of_contents(self, section, **kwargs):
        section.style.table_of_contents(title='Table of Contents', depth=2)

    def client_api(self, section, **kwargs):
        # Create the title and class definition.
        section.style.h3('Client')

        # Define the client class.
        section.style.start_sphinx_py_class(
            class_name='%s.Client' % self.service_name)
        self._do_client_intro_section(section)
        self._do_client_attributes(section)

        #section.style.end_sphinx_py_class()

    def _do_client_intro_section(self, section):
        section = section.add_new_section('intro')
        # Write out the top level description for the client.
        section.write(
            'A low-level client representing %s' % self.official_service_name)
        #section.style.new_line()

        # Write out the client example instantiation.
        section.style.start_codeblock()
        section.write('import boto3')
        section.style.new_line()
        section.write(
            '{service} = boto3.client(\'{service}\')'.format(
                service=self.service_name)
        )
        section.style.end_codeblock()

    def _do_client_attributes(self, section):
        section = section.add_new_section('attributes')
        client_members = inspect.getmembers(self.client)
        client_variables = {}
        client_methods = {}
        for name, member in client_members:
            if not name.startswith('_'):
                if inspect.ismethod(member):
                    client_methods[name] = member
                else:
                    client_variables[name] = member
        self._do_client_variables(section, client_variables)
        self._do_client_methods(section, client_methods)

    def _do_client_variables(self, section, client_variables):
        pass

    def _do_client_methods(self, section, client_methods):
        section = section.add_new_section('methods')
        for method_name in sorted(client_methods):
            self._do_client_method(
                section, method_name, client_methods[method_name])

    def _do_client_method(self, section, name, method):
        section = section.add_new_section(name)
        if self._is_data_driven_method(name):
            self._do_data_driven_client_method(section, name)
        else:
            self._do_custom_client_method(section, name, method)

    def _is_data_driven_method(self, method_name):
        return method_name in self.client._PY_TO_OP_NAME

    def _get_client_operation_model(self, method_name):
        service_model = self.client.meta.service_model
        operation_name = self.client._PY_TO_OP_NAME[method_name]
        return service_model.operation_model(operation_name)

    def _do_data_driven_client_method(self, section, name):
        operation_model = self._get_client_operation_model(name)
        params = self._get_data_driven_method_signature_params(operation_model)
        # Write out the name and kwargs for the client data driven method
        section.style.start_sphinx_py_method(name, params)
        # Write out the doc description for the method.
        section.include_doc_string(operation_model.documentation)
        # Add an example
        self._do_data_driven_client_method_example(
            section, name, operation_model)
        # Document the parameters.
        # Document the return value
        self._do_data_driven_client_return(section, name, operation_model)
        section.style.end_sphinx_py_method()        

    def _get_data_driven_method_signature_params(self, operation_model):
        params = {}
        required = []
        if operation_model.input_shape:
            params = operation_model.input_shape.members
            required = operation_model.input_shape.required_members

        required_params = [k for k in params.keys() if k in required]
        optional_params = [k for k in params.keys() if k not in required]
        signature_params = ', '.join([
            ', '.join(['{0}=None'.format(k) for k in required_params]),
            ', '.join(['{0}=None'.format(k) for k in optional_params])
        ]).strip(', ')
        return signature_params

    def _do_custom_client_method(self, section, name, method):
        params = self._get_custom_method_signature_params(name, method)
        section.style.start_sphinx_py_method(name, params)
        doc_string = inspect.getdoc(method)
        if doc_string is not None:
            section.style.write_py_doc_string(doc_string)
        section.style.end_sphinx_py_method()

    def _get_custom_method_signature_params(self, name, method):
        args, varargs, keywords, defaults = inspect.getargspec(method)
        args = args[1:]
        signature_params = inspect.formatargspec(
            args, varargs, keywords, defaults)
        signature_params = signature_params.lstrip('(')
        signature_params = signature_params.rstrip(')')
        return signature_params

    def _do_data_driven_client_method_example(self, section, name,
                                              operation_model):
        section = section.add_new_section('example')
    
        section.style.start_codeblock()
        example = 'response = client.%s' % name

        if operation_model.input_shape:
            section.write(example)
            self._do_example_input(section, operation_model)
        else:
            section.write(example + '()')

        section.style.end_codeblock()

    def _do_example_input(self, section, operation_model):
        shape_history = []
        self._document_shape_type_structure(
            section, operation_model.input_shape, is_top_level_input=True,
            history=shape_history)

    def _do_data_driven_client_return(self, section, name, operation_model):
        section = section.add_new_section('return')
        section.style.new_line()
        if operation_model.output_shape is not None:
            section.write(':rtype: dict')
            section.style.new_line()
            section.write(':returns: The following structure')
            section.style.start_codeblock()
            self._document_shape(
                section, operation_model.output_shape, history=[])
            section.style.end_codeblock()
            section.style.new_line()
            section.write('``foo``')
            section.style.new_paragraph()
            section.include_doc_string(operation_model.output_shape.documentation)
            section.style.indent()
            section.style.new_line()
            section.write('``bar``')
            section.style.indent()
            section.style.new_line()
            section.write('baz')
        else:
            section.write(':returns: None')

    def _document_shape(self, section, shape, history):
        param_type = shape.type_name
        if shape.name in history:
            self._document_recursive_shape(section)
        else:
            history.append(shape.name)
            getattr(self, '_document_shape_type_%s' % param_type,
                    self._document_shape_default)(
                    section, shape, history=history)
            history.pop()

    def _document_recursive_shape(self, section):
        section.write('{ ... recursive ... }')

    def _document_shape_type_string(self, section, shape, history):
        if 'enum' in shape.metadata:
            for i, enum in enumerate(shape.metadata['enum']):
                section.write('\'%s\'' % enum)
                if i < len(shape.metadata['enum']) - 1:
                    section.write('|')
        else:
            self._document_shape_default(section, shape, history)

    def _document_shape_default(self, section, shape, history):
        py_type = py_default(shape.type_name)
        section.write(py_type)

    def _document_shape_type_list(self, section, shape, history):
        self._start_nested_param(section, '[')
        param_shape = shape.member
        self._document_shape(section, param_shape, history)
        section.write(',')
        self._end_nested_param(section, ']')

    def _document_shape_type_structure(self, section, shape, history,
                                       is_top_level_input=False):
        input_members = shape.members

        param_format = '\'%s\''
        operator = ': '
        start = '{'
        end = '}'
        if is_top_level_input:
            operator = '='
            start = '('
            end = ')'
            param_format = '%s'

        self._start_nested_param(section, start)

        for i, param in enumerate(input_members):
            section.write(param_format % param)
            section.write(operator)
            param_shape = input_members[param]
            self._document_shape(section, param_shape, history)
            if i < len(input_members) - 1:
                section.write(',')
                section.style.new_line()

        self._end_nested_param(section, end)

    def _document_shape_type_map(self, section, shape, history):
        self._start_nested_param(section, '{')
        value_shape = shape.value
        section.write('\'string\': ')
        self._document_shape(section, value_shape, history)
        self._end_nested_param(section, '}')

    def _start_nested_param(self, section, start):
        section.write(start)
        section.style.indent()
        section.style.indent()
        section.style.new_line()

    def _end_nested_param(self, section, end):
        section.style.dedent()
        section.style.dedent()
        section.style.new_line()
        section.write(end)
