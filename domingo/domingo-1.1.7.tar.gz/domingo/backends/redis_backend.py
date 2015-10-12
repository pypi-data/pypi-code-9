import json
import os
import redis
import sys

from .base import DatabaseBackendBase, QuerySet, QueryError
from collections import defaultdict

try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    has_django = True
except ImportError, e:
    has_django = False


if has_django:
    try:
        REDIS_HOST = getattr(settings, 'DOMINGO_REDIS_HOST', 'localhost')
        REDIS_PORT = getattr(settings, 'DOMINGO_REDIS_PORT', '6379')
        REDIS_DB = getattr(settings, 'DOMINGO_REDIS_DB', 10)
        REDIS_PW = getattr(settings, 'DOMINGO_REDIS_PW', None)
    except ImproperlyConfigured, e:
        has_django = False


if not has_django:
    REDIS_HOST = os.environ.get('DOMINGO_REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('DOMINGO_REDIS_PORT', '6379')
    REDIS_DB = os.environ.get('DOMINGO_REDIS_DB', 10)
    REDIS_PW = os.environ.get('DOMINGO_REDIS_PW', None)


R = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PW
)


class RedisQuerySet(QuerySet):
    def count(self):
        pass


def get_redis(key=None):
    return R


class RedisStore(DatabaseBackendBase):

    queryset_class = RedisQuerySet

    def __init__(self, model, **kwargs):
        self.connection = get_redis(model.namespace)
        self.model = model
        self.namespace = model.namespace

    def commit_bulk_save(self):
        pipe = R.pipeline()
        for k, v in self.bulk_query:
            pipe.lpush(k, v.to_json())
        return pipe.execute()

    def commit_bulk_get(self, time_series=0):
        pipe = R.pipeline()
        for k in self.bulk_query:
            pipe.lrange(
                k, 0, time_series
            )

        data = pipe.execute()

        return [json.loads(d[0]) for d in data]

    def get(self, key):
        d = self.connection.lindex(key, 0)
        return d

    def unique_key(self, instance):
        names = []
        valid = True
        for name in instance.unique_on:
            field = getattr(instance, name)
            names.append(str(name))
            valid &= field.updated
        if not valid:
            raise QueryError(
                "%r does not have a complete unique_on key" % instance
            ), None, sys.exc_info()[2]
        return ".".join(names)

    @staticmethod
    def model_keys(keys):
        return [key for key in keys if len(key.split(':')) <= 2]

    @staticmethod
    def field_keys(keys):
        return [key for key in keys if len(key.split(':')) > 2]

    def all(self):
        """
        an all query method based on using : for delimiting the model, instance,
        field values in the key. The majority of the model is to be saved in a
        hash and the list fields extend the key to include the field name.
        The idea here is that the has can be updated with the list structures
        after grabbing the data.
        """
        keys = self.connection.keys(self.namespace + ":*")
        ret = defaultdict(dict)
        pipe = self.connection.pipeline()
        model_keys = self.model_keys(keys)
        field_keys = self.field_keys(keys)
        for key in model_keys:
            pipe.hgetall(key)
        model_data = pipe.execute()
        for idx, key in enumerate(model_keys):
            namespace, unique_key = key.split(":")
            ret[unique_key].update(
                dict(zip(self.model.unique_on, unique_key.split(".")))
            )
            ret[unique_key].update(model_data[idx])
        pipe = self.connection.pipeline()
        for key in field_keys:
            name, method = key.split('.')
            getattr(pipe, method)(key)
        pipe.execute()


    def save(self, data=None, sequential=True, created=False, fields=None):
        """
        data: list of model instances
        sequential: True if order is important, False otherwise
        created: True if the model instances are to have been created for
            the first time
        """
        bulkop = self.connection.pipe()

        if not fields:
            fields = []

        invalid_instances = []
        for instance in data:
            unique_key = {}
            valid = True

            for name in instance.unique_on:
                field = getattr(instance, name)
                unique_key[name] = field.value
                valid &= field.updated
                # valid is false if any of the unique_on fields were not
                # instantiated with an actual value

            if not valid:
                invalid_instances.append(instance)
                continue

            unique_key = '%s.%s' % (
                self.model.namespace, '.'.join(unique_key.values()))

            print unique_key

            bulkop.set(unique_key, instance.defaults)

            for name, field in instance.simple_fields.items():
                if field.updated or name == 'modified':
                    bulkop.hset(unique_key, name, field.value)

            if instance.timeseries_fields:
                for key, value in instance.timeseries_fields.items():
                    if not created or value.save_on_create:
                        bulkop.lpush('%s.%s' % (unique_key, key), value)

            if instance.set_fields:
                for key, value in instance.set_fields.items():
                    bulkop.sadd('%s.%s' % (unique_key, key), value)

            if instance.list_fields:
                for key, field in instance.list_fields.items():
                    if field.updated:
                        bulkop.lpush('%s.%s' % (unique_key, key), field.value)

            return
            """
            if instance.model_list_fields:
                # get the full models...
                for key in instance.unique_on:


                self.model.filter()


                model_list_data = {
                    key: {'$each': [m.as_dict() for m in field.value]}
                    for key, field in instance.model_list_fields.items() if field.updated
                }
                if model_list_data:
                    op = {'$addToSet': model_list_data}

                    if '$addToSet' in operations:
                        operations['$addToSet'].update(op)
                    else:
                        operations.update(op)
            # print json.dumps(operations, indent=5)
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
        """
