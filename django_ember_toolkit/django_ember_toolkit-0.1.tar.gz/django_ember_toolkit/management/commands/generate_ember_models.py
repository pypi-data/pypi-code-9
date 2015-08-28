from django.apps import apps as django_apps
from django.core.management import call_command
from django.db.models import fields
from inflection import camelize, dasherize, underscore

from ._base import EmberCommand

# keys are ember model types, values are Django fields they're compatible with
FIELD_TYPE_MAP = {
    'belongs-to': (
        fields.related.ForeignKey,
        fields.related.OneToOneField),
    'has-many': (
        fields.related.ManyToManyField,),
    'boolean': (
        fields.BooleanField,
        fields.NullBooleanField),
    'date': (
        fields.DateField,
        fields.DateTimeField),
    'number': (
        fields.BigIntegerField,
        fields.DecimalField,
        fields.FloatField,
        fields.IntegerField,
        fields.PositiveIntegerField,
        fields.PositiveSmallIntegerField,
        fields.SmallIntegerField),
}

# fields of other types are mapped onto Ember's 'string' type


def model_to_command_args(Model):
    '''Take a model class and return a list of args that will create an
    equivalent model in Ember.'''

    fields_to_generate = {
    }

    # iterate over all the fields in this model and create args to build
    # equivalent fields in the Ember model
    for field in Model._meta.get_fields():

        if field.name == 'id':
            # Ember automatically generates the id field, we shouldn't
            # include it
            continue

        was_assigned = False

        for ember_type, django_field_classes in FIELD_TYPE_MAP.items():
            if field.__class__ in django_field_classes:
                if ember_type not in fields_to_generate:
                    fields_to_generate[ember_type] = []

                fields_to_generate[ember_type].append(field)
                was_assigned = True

        if not was_assigned:
            # 'string' is the default tpye -- we didn't match anything else, so
            # we'll assign to that
            if 'string' not in fields_to_generate:
                fields_to_generate['string'] = []

            fields_to_generate['string'].append(field)

    field_args = []
    for ember_type, model_fields in fields_to_generate.items():
        for field in model_fields:
            emberized_field_name = camelize(
                underscore(field.name), uppercase_first_letter=False)

            field_arg = emberized_field_name + ':' + ember_type

            if ember_type in ('belongs-to', 'has-many'):
                # relation fields should also specify what they're related to
                relation_emberized = dasherize(underscore(
                    field.rel.to.__name__))
                field_arg += ':' + relation_emberized

            field_args.append(field_arg)

    full_args = ['generate', 'model', dasherize(underscore(Model.__name__))]
    full_args += field_args

    return full_args


class Command(EmberCommand):
    help = 'Generate Ember models based on Django models from INSTALLED APPS'

    def handle(self, *args, **options):
        self.assert_required_settings('EMBER_APP_PATH', 'MODELS_TO_SYNC')
        call_command('generate_ember_config')

        model_name_set = set(self.get_setting('MODELS_TO_SYNC'))
        model_set = set()

        for app_config in django_apps.get_app_configs():
            for Model in app_config.get_models():
                key = Model._meta.app_label + '.' + Model.__name__
                app_star = Model._meta.app_label + '.*'

                if key in model_name_set or app_star in model_name_set:
                    model_set.add(Model)

        self.notify('Generating Ember models for: ' +
            ', '.join([
                Model._meta.app_label + '.' + Model.__name__
                for Model in model_set]))

        for Model in model_set:
            self.run_ember_command(*model_to_command_args(Model))
