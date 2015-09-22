# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

import os
import re
from datetime import datetime
from optparse import make_option

from django.apps import apps
from django.core import serializers
from django.core.exceptions import FieldError
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS


ROOT_DIRECTORY = 'dumpdata'


def get_app_model(app_model):
    '''Receives a string like 'app_label.Model' and return the model'''
    try:
        model = apps.get_model(app_model)
    except LookupError:
        raise CommandError('app.model not found: {}'.format(app_model))
    except ValueError:
        raise CommandError('You must inform the model with app.model syntax: {}'.format(app_model))

    return model


def get_data(model_object, database, to, models_list):
    def to_serialize(model_object, database, to, models_list):
        def model_can_be_serialized(model):
            return to == 'include' and model in models_list or to == 'exclude' and model not in models_list

        def get_related_dependencies(model_object):
            related_objects = [
                (related_object.model, {related_object.field.name: model_object})
                for related_object in model_object._meta.get_all_related_objects()
                if model_can_be_serialized(related_object.model)
            ]

            for model, filter_data in related_objects:
                for value in model.objects.using(database).filter(**filter_data):
                    if value and value not in serialize_list:
                        related_data_list.add(value)

                        # Serialize itself
                        to_serialize(value, database, to, models_list)

        def get_direct_dependencies(model_object):
            for field in model_object._meta.fields:
                if hasattr(field.rel, 'to') and field.rel.to != model_object._meta.model:
                    value = getattr(model_object, field.name)

                    if value and value not in direct_data_list:
                        model = value._meta.model

                        if model_can_be_serialized(model):
                            direct_data_list.add(value)
                            get_direct_dependencies(value)

        direct_data_list = set()
        get_direct_dependencies(model_object)

        related_data_list = set()
        get_related_dependencies(model_object)

        if model_can_be_serialized(model_object._meta.model) and model_object not in serialize_list:
            serialize_list.append(model_object)

        for data in direct_data_list | related_data_list:
            if data not in serialize_list:
                serialize_list.append(data)

    serialize_list = []
    to_serialize(model_object, database, to, models_list)

    return serialize_list


def primary_object_regex(primary_object_str):
    '''The string must be splitted by app_label.Model.field:value'''

    pattern = re.compile(r'(?P<app_label>\w+)\.(?P<model>\w+)\.(?P<field>\w+)\:(?P<value>.+)')

    return pattern.match(primary_object_str)


def get_primary_object(primary_object_str):
    obj_regex = primary_object_regex(primary_object_str)

    app_model = '{}.{}'.format(obj_regex.group('app_label'), obj_regex.group('model'))
    model = get_app_model(app_model)

    filter_data = {obj_regex.group('field'): obj_regex.group('value')}

    try:
        primary_object = model.objects.get(**filter_data)
    except model.MultipleObjectsReturned:
        raise CommandError('You must inform a filter to get a unique register')
    except FieldError:
        raise CommandError('The field specified does not exists')

    return primary_object


def data_by_model(data_to_serialize):
    organized_data = {}
    for data in data_to_serialize:
        organized_data.setdefault(data._meta.model, []).append(data)

    return organized_data


class Command(BaseCommand):
    args = '[a valid username]'

    option_list = BaseCommand.option_list + (
        make_option('--include', dest='include',
                    help='Specifies this app.models to dump fixtures from. You cannot use this with --exclude'),

        make_option('--exclude', dest='exclude',
                    help='Do not dump this specific app.models splitted by a comma'),

        make_option('--format', dest='output_format', default='json',
                    help='Specifies the output serialization format for fixtures.'),

        make_option('--database', dest='database', default=DEFAULT_DB_ALIAS,
                    help='Nominates a specific database to dump fixtures from. '
                         'Defaults to the "default" database.'),

        make_option('--indent', dest='indent', default=None, type=int,
                    help='Specifies the indent level to use when pretty-printing output.'),

        make_option('-o', '--output-mode', dest='output_mode', choices=('directory', 'file'),
                    help='Specifies the output-mode. If the mode choosed is [directory], the models will be splitted by '
                    'file. If the mode choosed is [file], just one file is created for all fixture. Directory and file '
                    'will be named with the username of the User'),
    )

    def create_directories(self):
        if not os.path.exists(ROOT_DIRECTORY):
            try:
                os.mkdir(ROOT_DIRECTORY)
            except Exception:
                raise CommandError('Problem to create the dump directory')

        date = datetime.now().strftime('%Y%m%d-%H:%M:%S')

        try:
            path = os.path.join(ROOT_DIRECTORY, '{}-dumpdata'.format(date))
            os.mkdir(path)
        except Exception:
            raise CommandError('Problem to create the dump directory. Path: {}'.format(path))

        return path

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('You must use specify a unique object app_label.Model.field:value properly')

        primary_object_str = args[0]
        if not primary_object_regex(primary_object_str):
            raise CommandError('You must use specify app_label.Model.field:value properly')

        exclude_models_args = options.get('exclude', [])
        include_models_args = options.get('include', [])
        if exclude_models_args and include_models_args:
            raise CommandError('You cannot use --exclude and --include options at the same time')

        exclude = exclude_models_args.split(',') if exclude_models_args else []
        include = include_models_args.split(',') if include_models_args else []

        output_format = options.get('output_format')
        if output_format not in serializers.get_public_serializer_formats():
            raise CommandError('Unknown serialization format: {}'.format(output_format))

        output_mode = options.get('output_mode')
        database = options.get('database')
        indent = options.get('indent')

        primary_object = get_primary_object(primary_object_str)

        if include:
            models_to_include = [get_app_model(app_model) for app_model in include]
            data_to_serialize = get_data(primary_object, database, 'include', models_to_include)
        else:
            models_to_exclude = [get_app_model(app_model) for app_model in exclude]
            data_to_serialize = get_data(primary_object, database, 'exclude', models_to_exclude)

        if output_mode not in ('directory', 'file'):
            raise CommandError('You must specify an output mode to dump the fixtures')

        valid_path = self.create_directories()

        if output_mode == 'directory':
            organized_data = data_by_model(data_to_serialize)

            for model, data in organized_data.iteritems():
                filename = '{filename}.{extension}'.format(filename=model._meta.model_name, extension=output_format)

                with open(os.path.join(valid_path, filename), 'w') as stream:
                    serializers.serialize(output_format, data, indent=indent, stream=stream)

        elif output_mode == 'file':
            filename = 'objectdump.{extension}'.format(extension=output_format)

            with open(os.path.join(valid_path, filename), 'w') as stream:
                for data in map(lambda data: [data], data_to_serialize):
                    serializers.serialize(output_format, data, indent=indent, stream=stream)
