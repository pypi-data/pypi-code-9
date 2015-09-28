import logging
import os
import sys

from .base import DatabaseBackendBase, QuerySet, QueryError
from bson.objectid import ObjectId
from pymongo import MongoClient, DESCENDING, ASCENDING, TEXT, MongoReplicaSetClient
from pymongo.errors import BulkWriteError, OperationFailure


logger = logging.getLogger(__name__)


ALREADY_INDEXED = []

try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    has_django = True
except ImportError, e:
    has_django = False


DEFAULT_DB_NAME = 'domingo'
if has_django:
    try:
        MONGO_REPLICA_SET_URI = getattr(settings, 'MONGO_REPLICA_SET_URI', None)
        MONGO_REPLICA_SET_NAME = getattr(settings, 'MONGO_REPLICA_SET_NAME', None)
        MONGO_DB_NAME = getattr(settings, 'MONGO_DB_NAME', DEFAULT_DB_NAME)
        TEST_MODE = getattr(settings, 'TEST_MODE', True)
    except ImproperlyConfigured, e:
        has_django = False


if not has_django:
    MONGO_REPLICA_SET_URI = os.environ.get('DOMINGO_MONGO_REPLICA_SET_URI')
    MONGO_REPLICA_SET_NAME = os.environ.get('DOMINGO_MONGO_REPLICA_SET_NAME')
    MONGO_DB_NAME = os.environ.get('DOMINGO_MONGO_DB_NAME', DEFAULT_DB_NAME)
    TEST_MODE = os.environ.get('DOMINGO_TEST_MODE', False)

if MONGO_REPLICA_SET_URI and MONGO_REPLICA_SET_NAME:
    M = MongoReplicaSetClient(
        MONGO_REPLICA_SET_URI, replicaSet=MONGO_REPLICA_SET_NAME
    )
else:
    M = MongoClient()


class MongoQuerySet(QuerySet):

    def count(self):
        return self.query.count()

    def sort(self, key, order=ASCENDING):
        if isinstance(key, list):
            self.query = self.query.sort(key)
        else:
            if key.startswith('-'):
                key = key.strip('-')
                order = DESCENDING
            self.query = self.query.sort(key, order)
        return self

    def skip(self, skip):
        self.offset = skip
        self.query = self.query.skip(skip)
        return self

    def limit(self, limit):
        self.query = self.query.limit(limit)
        return self

    def inflate(self, field, **kwargs):
        """
            used when a model has a field that is a reference
            to another model stored in the database.

            this will parse the current model's data
            and return a second queryset which contains
            the result of the query on the 2nd model
            referred to by the 1st model's field
        """
        meta_field = getattr(self.model._meta, field)
        if hasattr(meta_field, 'model_class'):
            field_model = meta_field.model_class

            if hasattr(field_model, 'refers_to'):
                inflate_model = field_model.refers_to['model']
                inflate_field = field_model.refers_to['on_field']

                parent_model_refs = {}
                lists = [getattr(o, field) for o in self]

                # lists = [a list of references to a submodel for each result
                # in this queryset]

                for olist in lists:
                    # for each list of model references

                    # add to the global list of IDs we will pull from the database...
                    for o in olist:
                        parent_model_refs[ObjectId(str(o.fields[inflate_field]))] = {
                            field : o[field].value
                        for field in o.applied_fields
                        }
                return inflate_model.filter(
                    _id__in=parent_model_refs.keys(),
                    offset_query=self.offset,
                    apply_data={
                        'data': parent_model_refs,
                        'namespace': self.model.namespace
                    },
                    **kwargs
                )

        return self


class MongoStore(DatabaseBackendBase):

    queryset_class = MongoQuerySet

    def __init__(self, model, **kwargs):
        self.db = M[MONGO_DB_NAME]
        self.offset_query = 0
        self.applied_data = kwargs.pop('applied_data', {})
        self.model = model
        self.namespace = model.namespace
        self.collection = self.db[self.namespace]
        if 'unique_on' not in self.collection.index_information():
            self.collection.create_index(
                [(name, 1) for name in self.model.unique_on],
                unique=True, name='unique_on', background=True
            )
        if self.namespace not in ALREADY_INDEXED:
            for name, field in self.model.classfields():
                self.set_index(name, field)

            if not TEST_MODE:
                if hasattr(self.model, 'text_index_fields'):
                    try:
                        self.collection.ensure_index(
                            [(f, TEXT) for f in self.model.text_index_fields],
                            name="text_index",
                            weights=getattr(
                                self.model, 'text_index_weights', {}
                            )
                            )
                    except OperationFailure as e:
                        # print e
                        # there is already a different index in place...
                        try:
                            # it is probably the original one where we did all
                            # fields...
                            self.collection.drop_index("$**_text")
                        except OperationFailure as e:
                            logger.error('could not drop index: %r', e)
                        try:
                            # or maybe we changed the options on the index?
                            self.collection.drop_index("text_index")
                        except OperationFailure as e:
                            logger.error('could not drop index: %r', e)

                        self.collection.ensure_index(
                            [(f, TEXT) for f in self.model.text_index_fields],
                            name="text_index",
                            weights=getattr(
                                self.model, 'text_index_weights', {}
                            )
                        )
            ALREADY_INDEXED.append(self.namespace)
        else:
            'indexing done'

    def set_index(self, name, field):
        if hasattr(field, 'unique') and field.unique:
            self.collection.ensure_index(name, unique=True, sparse=True)
        elif hasattr(field, 'index') and field.index:
            self.collection.ensure_index(name)
        # if hasattr(field, 'text_index') and field.text_index:
            # self.text_indexed[name] = 'text'

    def get_operator(self, operator):
        try:
            # TODO: test these
            return {
                'in': '$in',
                'gte': '$gte',
                'gt': '$gt',
                'lt': '$lt',
                'lte': '$lte',
                'not': '$not',
                'ne': '$ne',
                'eq': '$eq'
            }[operator]
        except KeyError:
            raise KeyError(
                'cannot resolve %s for query in %s' % (
                    operator, self.__class__.__name__
                )
            )

    def add_filter(self, key, value):
        out = {}
        if '__' in key:
            field, operator = key.split('__')
            field_class = getattr(self.model._meta,field)
            value = field_class.prep_query_value(value)

            if '__' in operator:
                modifier, primary = operator.split('__')
                out[field] = {
                    self.get_operator(modifier): {
                        self.get_operator(primary): value
                    }
                }
                return out
            elif operator == 'not':
                out[field] = {'$not': {'$eq': value}}
            else:
                out[field] = {self.get_operator(operator): value}
            return out
        field_class = getattr(self.model._meta, key)
        value = field_class.prep_query_value(value)

        out[key] = value
        return out

    def parse_conditions(self, **kwargs):
        """
        Returns a dictionary with the field name as the key and a dictionary
        of operators and values as the field name's value
        """
        conditions = {}
        for key, val in kwargs.items():
            if key == 'text_search':
                conditions['$text'] = {'$search': val}
            else:
                field = ''
                if '__' in key:
                    field, operator = key.split('__')
                if field in conditions:
                    conditions[field].update(self.add_filter(key, val)[field])
                else:
                    conditions.update(self.add_filter(key, val))
        return conditions

    def parse_projections(self, include, exclude, slice_args, elem_match):
        ret = {}
        for field in include:
            ret[field] = 1
        for field in exclude:
            ret[field] = 0

        if slice_args:
            self.offset_query = slice_args.get('start', 0)
            start = slice_args.get('start', 0)
            end = slice_args.get('end')
            if end:
                slice = [start, end]
            else:
                slice = start
            ret[slice_args.get('field')] = {'$slice': slice}
        if elem_match:
            for group in elem_match:
                for field in group['fields']:
                    # print field, group
                    ret[field] = {
                        '$elemMatch': {group['object']: group['value']}
                    }
        # print json.dumps(ret, indent=5)
        return ret

    def all(self):
        return self.queryset_class(
            self.collection.find(), self.model, self.db,
            offset=self.offset_query, apply_data=self.applied_data
        )

    def filter(self, raw=None, include=None, exclude=None, **kwargs):
        include = include or []
        exclude = exclude or []

        self.offset_query = kwargs.pop('offset_query', 0)
        self.applied_data = kwargs.pop('apply_data', self.applied_data)

        slice_args = kwargs.pop('slice', None)
        elem_match = kwargs.pop('elem_match', None)

        projection = kwargs.pop('projection', None)
        if not projection:
            projection = self.parse_projections(
                include, exclude, slice_args, elem_match
            )
        conditions = self.parse_conditions(**kwargs)

        if raw:
            conditions.update(raw)

        # print 'query:'
        # try:
        #     print json.dumps(conditions, indent=5)
        #     print json.dumps(projection, indent=5)
        # except:
        #     pass

        if projection:
            documents = self.collection.find(conditions, projection)
        else:
            documents = self.collection.find(conditions)

        return self.queryset_class(
            documents, self.model, self.db,
            offset=self.offset_query, apply_data=self.applied_data
        )

    def rawFilter(self, query, projection=None):
        if projection:
            documents = self.collection.find(
                query, projection,
                offset=self.offset_query, apply_data=self.applied_data
            )
        else:
            documents = self.collection.find(query)

        return self.queryset_class(
            documents, self.model, self.db,
            offset=self.offset_query, apply_data=self.applied_data
        )

    def get(self, include=None, exclude=None, **kwargs):

        conditions = self.parse_conditions(**kwargs)
        document = self.collection.find(conditions)
        count = document.count()

        if count > 1:
            raise QueryError(
                '%s.get returned too many documents: %s' % (self.model, kwargs)
            ), None, sys.exc_info()[2]
        if count == 1:
            return self.queryset_class(document, self.model, self.db).results[0]
        else:
            raise QueryError(
                '%s.object not found: %s' % (self.model, kwargs)
            ), None, sys.exc_info()[2]

    def save(self, data=None, sequential=True, created=False, fields=None):
        """
        data: list of model instances
        sequential: True if order is important, False otherwise
        created: True if the model instances are to have been created for
            the first time
        """

        if sequential:
            bulkop = self.collection.initialize_ordered_bulk_op()
        else:
            bulkop = self.collection.initialize_unordered_bulk_op()

        invalid_instances = []

        if not fields:
            fields = self.model.defaults.keys()

        for index, instance in enumerate(data):
            instance.pre_save()
            # print [name for name,f in instance.classfields() if f.updated]

            unique_key = {}
            not_empty = True
            for name in instance.unique_on:
                field = instance._fields[name]
                unique_key[name] = field.value
                # print name, field.value, field.is_not_empty()
                not_empty &= field.is_not_empty()
                # field is not_empty if any of the unique_on fields were not
                # instantiated with an actual value
            if not not_empty and instance._fields['_id'].value and instance._fields['_id'].updated:
                unique_key = {'_id': instance._id}


            if not not_empty:
                invalid_instances.append(instance)
                continue

            bulkop.find(unique_key).upsert().update(
                {'$setOnInsert': instance.defaults}
            )

            operations = {}

            operations.update({
                '$set': {
                    name: field.value
                    for name, field in instance.simple_fields.items()
                    if field.updated or name == 'modified' and name in fields
                }
            })

            if instance.timeseries_fields:
                operations.update({
                    '$push': {
                        key: value.value # value is a List() class, so we want its value...
                        for key, value in instance.timeseries_fields.items()
                        if not created or value.save_on_create and key in fields
                    }
                })

            if instance.set_fields:
                set_data = {
                    key: {'$each': field.value}
                    for key, field in instance.set_fields.items()
                    if field.updated and key in fields
                }
                if set_data:
                    operations.update({'$addToSet': set_data})

            if instance.list_fields:
                list_data = {
                    key: {'$each': field.value}
                    for key, field in instance.list_fields.items()
                    if field.updated and key in fields
                }
                if list_data:
                    op = {'$push': list_data}
                    if '$push' in operations:
                        operations['$push'].update(op)
                    else:
                        operations.update(op)

            if instance.model_list_fields:
                model_list_data = {
                    key: {'$each': [m.as_dict() for m in field.value]}
                    for key, field in instance.model_list_fields.items()
                    if field.updated and key in fields
                }
                if model_list_data:
                    op = {'$addToSet': model_list_data}

                    if '$addToSet' in operations:
                        operations['$addToSet'].update(op)
                    else:
                        operations.update(op)

                    for key, val in model_list_data.items():
                        operations['$set']['%s_count' % key] = len(val['$each'])

            for key, val in operations.items():
                if not val:
                    del operations[key]

            bulkop.find(unique_key).upsert().update(operations)

        if invalid_instances:
            raise QueryError(
                'Could not save the data, %d out of the %d instances were '
                'invalid.' % (
                    len(invalid_instances), len(data)
                )
            )

        try:
            result = bulkop.execute()
        except BulkWriteError, e:
            logger.error(str(e), exc_info=True, extra={'data': e.details})
            raise
        return result

        # self.model.update_min_max_fields(data)
    def update(self, filter=None, update=None):
        if not filter:
            raise QueryError('Please filter models to update')
        self.collection.update(filter, update)
