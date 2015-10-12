import calendar
import json
import sys


import logging
logger = logging.getLogger(__name__)
time_logger = logging.getLogger('time_logger')

from collections import defaultdict

from datetime import timedelta

from twisted.internet import defer, reactor, task
from twisted.internet.threads import deferToThread
from twisted.web._newclient import ResponseNeverReceived

from .fields import (
    Id, TimeStamp, List, Dict, AbstractBaseField, NonIter, Iter,
    ModelList, ObjectId, AbstractSet, timeseries_namespace
)
from .backends.redis_backend import get_redis
from .connection import databases
from .query import QueryMixin
from .data_access import DataAccessBase
from .utils import classproperty, utcnow, utcstamp

# leave this in for now as we need to also refactor our YouTube code in the
# same way.
# from apps.platforms.api.youtube import YoutubeApiError


MAX_LIST_LENGTH = 3


class AppCache(object):

    def __init__(self):
        self.model_cache = {}

    def get_model(self, app_label, model_name):
        return self.model_cache.get(
            app_label.lower(), {}
        ).get(model_name.lower())

    def register_model(self, app_label, model_name, model):

        if self.model_cache.get(app_label):
            if self.model_cache.get(app_label.lower()).get(model_name):
                return
            else:
                self.model_cache[app_label.lower()][model_name.lower()] = model
        else:
            self.model_cache[app_label.lower()] = {model_name.lower(): model}


cache = AppCache()
get_model = cache.get_model
register_model = cache.register_model


class MetaModel(object):

    def __init__(self, field_list):
        self.fields = {}
        self.fieldmap = defaultdict(list)
        for name, field in field_list:
            setattr(self, name, field)
            self.fields[name] = field
            self.fieldmap[field.__class__].append(name)
        self.fieldmap = dict(self.fieldmap)


class ModelBaseMeta(type):
    def __new__(meta, classname, bases, classDict):

        app_label = bases[0].__module__.split('.')[-2]

        # first look in the cache and see if we made this already
        existing = get_model(app_label, classname)
        if existing:
            return existing

        # find fields from all base classes of this model
        field_list = []
        for base in bases:
            if hasattr(base, '_meta'):
                field_list += base._meta.fields.items()

        # now remove all fields from this field's class dict
        # so we don't put them directly on the class
        # store them to put them on the _meta
        for key, val in classDict.items():
            if issubclass(val.__class__, AbstractBaseField):
                field_list.append((key, val))
                del classDict[key]

        newmeta = MetaModel(field_list)
        # make the class
        new_class = type.__new__(meta, classname, bases, classDict)
        new_class._meta = newmeta

        # save it
        register_model(app_label, classname, new_class)

        return get_model(app_label, classname)


class AbstractModelBase(object):

    data_access_class = DataAccessBase

    @classproperty
    def namespace(cls):
        return cls.__name__.lower()

    @classproperty
    def store(cls):
        return databases[cls]

    @property
    def data(self):
        if hasattr(self, 'data_access_class'):
            if not hasattr(self, '__data_access'):
                self.__data_access = self.data_access_class(self)
            return self.__data_access
        else:
            raise AttributeError('a data_access_class has not been defined for this instance')


class CacheModelBase(AbstractModelBase):

    __metaclass__ = ModelBaseMeta

    storage = 'redis'

    def __init__(self, *args, **kwargs):
        self._fields = {}
        for name, field in self._meta.fields.items():
            FieldClass = field.__class__
            if name in kwargs:
                instance = FieldClass(kwargs[name], owner=self, name=name)
            else:
                instance = FieldClass(owner=self, name=name)
            self._fields[name] = instance
            setattr(self, name, instance)

    def save(self):
        raise NotImplementedError

    def as_dict(self):
        return {
            name: field.value
            for name, field in self._fields.items()
        }


class ModelBase(AbstractModelBase, QueryMixin):
    """
    The objective of this class is to set the main functionaly of the
    interface between the database and the webapp.
    1. Django-like definition of fields on the class
    2.
    """
    __metaclass__ = ModelBaseMeta

    save_list = None
    storage = 'mongo'

    outlet = None
    max_time_series_length = MAX_LIST_LENGTH

    unique_on = []

    @classmethod
    def classfields(cls):
        return cls._meta.fields.items()

    @property
    def unique_key(self):
        return '.'.join([str(getattr(self, name)) for name in self.unique_on])

    @classproperty
    def timeseries_fieldnames(cls):
        "returns a list of strings referencing the field attribute handle"
        if not hasattr(cls, '_timeseries_fieldnames'):
            cls._timeseries_fieldnames = [
                name for name, field in cls.classfields() if field._timeseries
            ]
        return cls._timeseries_fieldnames

    @classproperty
    def redis(cls):
        if not hasattr(cls, '_redis'):
            cls._redis = get_redis(cls.namespace)
        return cls._redis

    def __init__(self, *args, **kwargs):
        self._fields = {}
        # save state on whether or not this model is coming out of the database
        self._read_from_db = False
        if '_read_from_db' in kwargs:
            self._read_from_db = True

        applied_data_lookup = kwargs.pop('_applied_data', None)

        self.context_order = kwargs.pop('_context_order', None)

        setattr(self, 'db_text_score', kwargs.pop('db_text_score', None))
        # time_logger.info('start setup fields')
        self.setup_fields(*args, **kwargs)

        if applied_data_lookup:
            # TODO: this kinda sucks that we need to "ObjectId" the key... it
            # makes it very specific... maybe break this out into a method
            # someday?
            setattr(
                self, applied_data_lookup['namespace'],
                applied_data_lookup['data'].get(ObjectId(self._id.value))
            )

    def __setattr__(self, name, value):
        "ammends setattr so to allow resetting of the local fields"
        # TODO: this may not be needed if we make fields able to somehow
        # correctly set their own values instead of needing "set"
        if not name == '_fields':
            if self._fields.get(name):
                self._fields[name].set(value)

        super(ModelBase, self).__setattr__(name, value)

    def field_init(self, fieldname, field, *args, **kwargs):
        """
        Initializes the field and stores it in self._fields. It also sets the
        fields owner and name, as well as setting the default value to the
        field if no custom value was specified at Model instantiation.
        """
        # time_logger.info('start field %r'%fieldname)
        try:
            FieldClass = field.__class__
            if fieldname in kwargs:
                val = kwargs.get(fieldname)
                newfield = FieldClass(
                    val, owner=self, name=fieldname, **field._original_kwargs
                )
                if kwargs.get('%s_count' % fieldname):
                    newfield.count = kwargs['%s_count' % fieldname]
            else:
                # time_logger.info('last field thing')
                newfield = FieldClass(
                    owner=self, name=fieldname, **field._original_kwargs
                )
            if self._read_from_db:
                newfield.updated = False

            setattr(self, fieldname, newfield.value)
            self._fields[fieldname] = newfield
        except:
            raise
        # time_logger.info('finished field %r'%fieldname)

    def _raise_unique_exception(self):
        if self.__class__.__name__ in ['ModelBase', 'AsyncModel']:
            return
        raise AttributeError(
            '''\n%r must have at least one field specified as unique.
            like this:
                unique_on = ['field_one', 'field_two']

            ''' % self
        ), None, sys.exc_info()[2]

    def setup_fields(self, *args, **kwargs):
        """
        Iterates over all of the attribute names in the model class in order to
        identify which objects are fields and then initialize the model
        instance specific fields (with values). These field instances are kept
        in the dict self._fields.
        """

        for name, field in self._meta.fields.items():
            self.field_init(name, field, *args, **kwargs)

    @property
    def fields(self):
        "Returns a list of the instances fields"
        return self._fields.values()

    @property
    def fieldnames(self):
        return self._fields.keys()

    def _filterFields(self, *args, **kwargs):
        """
        Filters the instances within _fields for the class type specified.
        """
        keep = kwargs.get('keep', True)
        cls = self.__class__
        key = ''.join([c.__name__.lower() for c in args]) + str(keep)
        if not hasattr(cls, key):
            if kwargs.get('exact'):
                ret = {
                    name: field
                    for name, field in self._fields.items()
                    if field.__class__ in args and name not in ['created', '_id']
                }
            else:
                ret = {
                    name: field
                    for name, field in self._fields.items()
                    if issubclass(field.__class__, args) == keep and name not in ['created', '_id']
                }
            setattr(cls, key, ret.keys())
        else:
            fieldnames = getattr(cls, key)
            ret = {name: self._fields[name] for name in fieldnames}
        return ret

    @property
    def list_fields(self):
        return self._filterFields(List, exact=True)

    @property
    def model_list_fields(self):
        return {
            name: field
            for name, field in self._fields.items()
            if isinstance(field, ModelList)
        }

    @property
    def set_fields(self):
        return self._filterFields(AbstractSet)

    @property
    def simple_fields(self):
        return self._filterFields(NonIter, Dict)

    @property
    def timeseries_fields(self):
        now = utcstamp()
        return {
            timeseries_namespace(name): List(
                [now, self._fields[name].value],
                save_on_create=self._fields[name].save_on_create)
            for name in self.timeseries_fieldnames
            if self._fields[name].updated
        }

    @classproperty
    def defaults(cls):
        if not hasattr(cls, '_defaults'):
            defaults = {
                name: field.to_json()
                for name, field in cls.classfields()
                if name not in ['_id'] + cls.unique_on and (isinstance(field, TimeStamp) or issubclass(field.__class__, Iter))
            }
            defaults.update(
                {
                    timeseries_namespace(name): []
                    for name in cls.timeseries_fieldnames
                }
            )
            cls._defaults = defaults
        else:
            defaults = cls._defaults
        return defaults

    @property
    def id(self):
        if not hasattr(self, 'id_cache'):
            self._id_cache = '.'.join(
                [str(self._fields[f]) for f in self.unique_on]
            )
        return self._id_cache

    @property
    def pk(self):
        return self.id

    @property
    def uid(self):
        return '%s.%s' % (self.namespace, self.id)

    def __repr__(self):
        return u'<%s %s>' % (
            self.__class__.__name__,
            self.id,
            # unicode(self.fields)
        )

    def as_dict(self):
        """
        For use in model serialization. It uses the dictionary returned from
        _fields property method (below).
        """
        if not hasattr(self, '__as_dict'):
            data = {
                name: field.to_json() for name, field in self._fields.items()
            }
            self.__as_dict = data
        return self.__as_dict

    def to_json(self):
        "Serializes the model instance"
        return json.dumps(self.as_dict())

    def ordered_values(self, fields=None):
        fields = fields or []
        try:
            return [
                self._fields.get(fieldname).to_json() for fieldname in fields
            ]
        except TypeError, e:
            raise

    def csv(self, fields):
        return '%s\n' % '\t'.join([str(self.fields[f]) for f in fields])

    @classmethod
    def instantiate_list(cls, data, from_json=False, read_from_db=False, offset=0, applied_data=None):
        if from_json:
            return [cls(_read_from_db=read_from_db, _context_order=i+offset, _applied_data=applied_data, **json.loads(r)) for i, r in enumerate(data)]
        return [cls(_read_from_db=read_from_db, _context_order=i+offset, _applied_data=applied_data, **r) for i, r in enumerate(data)]

    @classmethod
    def load_from_cache(cls, key, start, end):
        pipe = cls.redis.pipeline()
        pipe.lrange(key, start, end)
        pipe.llen(key)
        results, count = pipe.execute()

        if count:
            return cls.instantiate_list(results, read_from_db=True, offset=start, from_json=True), count
        return None, None

    @classmethod
    def invalidate_cache(cls, key):
        cls.redis.delete(key)

    @classmethod
    def update_cache(cls, key, match):
        try:
            cls.redis.lset(key, match.context_order, match.to_json())
        except:
            pass


class SimpleModel(ModelBase):
    """
        omits Id, created, and modified fields
    """


class AsyncModel(ModelBase):
    """
    This model must be used for models with one or more "AggregateScore" fields

    It may actually be the best type to use in general as it does not
    alter the base functionality of the standard ModelBase in
    any significant way.
    """

    _id = Id()
    created = TimeStamp(updated=True)
    modified = TimeStamp()

    def __init__(self, *args, **kwargs):
        super(AsyncModel, self).__init__(*args, **kwargs)
        # time_logger.info('begin model')
        self.in_progress = 0
        self.start_time = utcnow()
        self.finished = False
        self.timeout = timedelta(0, kwargs.pop('timeout', 15))
        self.latest_check = utcnow()

        self.processes = []

        self.functions = kwargs.pop('functions', [])
        self.input_data = kwargs.pop('function_args', [None])[0]
        # time_logger.info('end model')

    @property
    def meta_data_key(self):
        """
        This method utilises the microseconds in the time to create a
        unique namespace for the redis cache key-value store.
        """
        epoch_time = calendar.timegm(self.start_time.utctimetuple())
        time_signature = int(
            epoch_time * 1000000 + self.start_time.microsecond
        )
        return '%s.%d' % (self.namespace, time_signature)

    def _set_initial_data(self):
        """
            sets some state info in redis.
            not used for anything currently, but could be used for
            spreading activity across muliple processes
        """
        self.redis.hset(
            self.meta_data_key, 'in_progress', len(self.input_data)
        )

    def run(self, outfile=None):
        """
        sets up some conditions and starts the process for this aggregator
        """

        if hasattr(reactor, 'aggregator_count'):
            reactor.aggregator_count += 1
        else:
            reactor.aggregator_count = 1

        if outfile:
            self.outfile = outfile

        self._set_initial_data()
        self._spawn_chain(tuple(self.functions))

        lc = task.LoopingCall(self.signal_finished, check=True)
        lc.start(self.timeout.total_seconds()/5)

    def _spawn_chain(self, list_of_funcs):
        """
            used at the offset.
            could possibly be replaced by "branch".
        """

        defproc = defer.Deferred()
        for proc in list_of_funcs:
            if isinstance(proc, tuple):
                self._spawn_chain(proc)
            else:
                defproc.addCallback(proc, aggregator=self)
        defproc.callback(self.input_data)

    def branch(self, function=None, args=None,
               kwargs=None, callbacks=None, attempt=0):
        """
            branches callbacks into new deferred processes
        """
        if not callbacks:
            callbacks = []
        if not kwargs:
            kwargs = {}

        kwargs['aggregator'] = self
        if attempt > 0:
            print 'branching: %r attempt %d, args:%r' % (
                function, attempt+1, args)

        D = deferToThread(function, args, **kwargs)

        for c in callbacks:
            D.addCallback(c, **kwargs)

        def errfunction(failure, *args, **kwargs):
            r = failure.trap(
                # YoutubeApiError,
                ResponseNeverReceived,
                defer.CancelledError
            )
            print 'failure:', r
            print 'attempt %d of %r'% (attempt+1, function)
            print 'retrying'
            kwargs.get('aggregator').branch(
                function=function,
                args=args,
                callbacks=callbacks,
                attempt=attempt + 1
            )

        D.addErrback(errfunction, *args, **kwargs)

    def increment_conditions(self, fields=None):
        """
            this is so we can bulk set finishing conditions data across
            multiple fields.
        """
        if not fields:
            fields = {}

        pipe = self.redis.pipeline()
        for field, value in fields.items():
            f = self._fields[field]
            f.increment_condition(value, pipe=pipe)
        pipe.execute()

    def manage_work(self, value, token=None):
        """
            manages how many children are still actively aggregating data
        """
        self.in_progress += value
        if token:
            self.processes.append(token)

    def signal_finished(self, value=1, check=False):
        """
            when an instance spawned by this aggregator
            is done aggregating data, it signals it is finished.
            we then decrement our work counter and see if
            we are all done.
        """
        if check:
            if self.check_time():
                self.finish()
            else:
                print '.',

        self.manage_work(-value)

        if self.in_progress == 0 and self.check_time():
            self.finish()

    def finish(self):
        """
            checks if the reactor has more aggregators running,
            if not, stops the reactor.

            TODO:
            this should probably only be done during testing or script running
            contexts..., how do we know if that is the case?
        """
        if self.finished:
            return

        self.finished = True
        self.write_data()
        if hasattr(reactor, 'aggregator_count'):
            reactor.aggregator_count -= 1

            if reactor.aggregator_count <= 0:
                reactor.stop()

    def write_data(self):
        if not len(self.unique_on):
            self._raise_unique_exception()

        channel_stats = self.get_list(self.processes).values()

        for channel_stat in channel_stats:
            print channel_stat
            aggregation_fields = [
                f for f in channel_stat._fields.values()
                if isinstance(f, fields.AsyncInt)
            ]
            for field in aggregation_fields:
                field.save(force=True)

            print 'finished %s (views c %d, v %d), (count c %d, v %d)' % (
                channel_stat.id,
                channel_stat.channel_views,
                channel_stat.aggregate_views,
                channel_stat.channel_video_count,
                channel_stat.aggregate_video_count)

            out = open(self.outfile, 'a')
            out.write(
                channel_stat.csv([
                    'id',
                    'channel_views',
                    'aggregate_views',
                    'channel_video_count',
                    'aggregate_video_count'
                ])
            )
            out.close()

    def tick(self):
        self.latest_check = utcnow()

    def check_time(self):
        return utcnow() - self.latest_check > self.timeout

    @classmethod
    def post_bulk_create(cls, *args, **kwargs):
        pass
