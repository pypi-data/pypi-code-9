import logging
import sys
from bson.objectid import ObjectId
from .backends.redis_backend import get_redis
from .utils import utcstamp


logger = logging.getLogger(__name__)
time_logger = logging.getLogger('time_logger')


def timeseries_namespace(name):
    return name + '_timeseries'


class AbstractBaseField(object):
    has_dependencies = False
    updated = False

    reserved = dir(object) + ['set', 'append', 'to_json', 'reserved']

    def __init__(self, *args, **kwargs):
        # time_logger.info('start field init')
        self.name = None
        self.unique = False
        self.save_on_create = True
        self._original_kwargs = kwargs
        self._timeseries = kwargs.get('time_series', False)

        for k, v in kwargs.items():
            if k not in self.reserved:
                setattr(self, k, v)

        self.set(*args)
        # time_logger.info('end field init')

    @property
    def timeseries(self):
        if self._timeseries:
            return self.owner[timeseries_namespace(self.name)]
        return None

    def __repr__(self):
        return unicode(self.value)

    def __eq__(self, other):
        if self.value is None:
            if other is None:
                return True
            else:
                return False
        elif other is None:
            return False
        else:
            value = self.value
            if issubclass(other.__class__, AbstractBaseField):
                other_value = other.value
                return not value < other_value and not other_value < value
            else:
                return not value < other and not other < value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, (int, long, float)):
            return self.value > other
        if issubclass(other.__class__, AbstractBaseField):
            return self.value > other.value

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

    def __sub__(self, other):
        if issubclass(other.__class__, AbstractBaseField):
            return self.value - other.value
        else:
            return self.value - other

    def __add__(self, other):
        if issubclass(other.__class__, AbstractBaseField):
            return self.value + other.value
        else:
            return self.value + other

    def __radd__(self, other):
        if issubclass(other.__class__, AbstractBaseField):
            return other.value + self.value
        else:
            return other + self.value

    def __mul__(self, other):
        if issubclass(other.__class__, AbstractBaseField):
            return self.value * other.value
        else:
            return self.value * other

    def __div__(self, other):
        if issubclass(other.__class__, AbstractBaseField):
            return self.value / other.value
        else:
            return self.value / other

    def __int__(self):
        return int(self.value)

    def __hash__(self):
        return self.value

    def __neg__(self):
        return self.value * -1

    @property
    def key(self):
        """
        Returns a unique name to be used in a cache store.
        We can change this method to return a shorter value if we want
        """
        return self.name

    def to_json(self):
        return self.value

    def get_default(self):
        if hasattr(self, 'default'):
            return self.default
        else:
            return self.encoder()

    def set(self, *args, **kwargs):
        try:
            self.value = self.encoder(args[0])
            self.updated = True
        except IndexError:
            self.value = self.get_default()

    def prep_query_value(self, value):
        return value

    def is_not_empty(self):
        return self.value != self.encoder() or (
            hasattr(self, 'default') and self.value == self.default)


###############################################################################
# Delineate field by whether they are iterable or not.
class Iter(AbstractBaseField):

    iterable = True

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)


class NonIter(AbstractBaseField):

    iterable = False


class Bool(NonIter):

    encoder = staticmethod(bool)

    def to_json(self):
        return int(self.value)


class Id(NonIter):

    encoder = staticmethod(ObjectId)

    def to_json(self):
        return str(self.value)


class FKey(NonIter):

    encoder = staticmethod(ObjectId)

    def to_json(self):
        return str(self.value)


class Char(NonIter):

    def encoder(self, *args):
        if args:
            return unicode(args[0]).encode("utf-8")


class TimeStamp(NonIter):

    encoder = staticmethod(utcstamp)

    def __eq__(self, other):

        return utcstamp(self.value) == utcstamp(other)


class Number(NonIter):

    _min = None
    _max = None

    def __repr__(self):
        return str(self.value)


class Float(Number):

    encoder = staticmethod(float)


class Int(Number):

    encoder = staticmethod(int)


class AsyncNumber(Number):
    """
    The value of this score is the result of aggregating data that may
    come from multiple sources or api calls.  This field contains
    mechanisms for dealing the collection and incrementing of such score
    data.
    """

    # datetimes
    started = None
    finished = None

    def __init__(self, *args, **kwargs):
        """
        The following enforces the setting of the instance attributes that
        are needed to specify the finishing condition.
        """
        condition_reqs = ('condition_type', 'condition_key')
        reqs = {req: req not in kwargs for req in condition_reqs}
        if any(reqs.values()):  # checks if any of the reqs are not included
            raise AttributeError(
                "%s.%s needs to have a %s specified" % (
                    self.owner, self.name,
                    ' & '.join([req for req, met in reqs.items() if met])
                )
            ), None, sys.exc_info()[2]
        super(AsyncNumber, self).__init__(*args, **kwargs)

    @property
    def aggregate_key(self):
        """
        The key where we will store the aggregate value in progress.

        N.B. self.owner is defined on the instance specific initialisation of
        the field. (so is self.name)... self.owner refers to the model instance
        that initialised the field (i.e. the model in which the field lives)
        Goto AbstractModelBase._setup_fields for more info.
        """
        return '%s.%s.%s' % (self.namespace, self.owner.id, self.key)

    def get_data(self):
        """
        Gets the temporary value stored in redis and re-sets the value of this
        field.
        Returns a dict containing the value
        """
        connection = get_redis(self.namespace)
        self._data = connection.hgetall(self.aggregate_key)
        self.set(self._data.get('value', 0))
        return self._data

    @property
    def is_complete(self):
        """
        Checks if the aggregation process is complete by checking the localized
        data store against the logic associated to the type of condition is
        associated to the field.
        """
        data = self.get_data()
        actual_count = int(data.get(self.condition_key))
        if self.condition_type == 'decrement':
            return actual_count <= 0
        else:
            return actual_count >= 0

    def add_data(self, value, samples=1):
        """
        Call to asynchronously add data to the temporary redis store and to
        update the condition_key by the given number of samples.
        """
        connection = get_redis(self.namespace)
        pipe = connection.pipeline()
        pipe.hincrby(self.aggregate_key, 'value', value)
        if self.condition_type == 'decrement':
            pipe.hincrby(self.aggregate_key, self.condition_key, -samples)
        else:
            pipe.hincrby(self.aggregate_key, self.condition_key, samples)
        data = pipe.execute()
        self.set(data[0])

    def increment_condition(self, value, pipe=None):
        if not pipe:
            pipe = get_redis(self.namespace)
        pipe.hincrby(self.aggregate_key, self.condition_key, value)

    def save(self, force=False):
        """
        Saves the final value to a redis key-value store specific to the
        field's model. It saves the value and the model id.

        At the moment this function is only used in the write_data method in
        the ScoreModel class.
        """
        self.get_data()
        connection = get_redis(self.namespace)
        # if force is true then is_complete will not be evaluated
        if not force and not self.is_complete:
            return False
        try:
            # stores the model.id in a sorted set ordered by the value.
            connection.zadd(
                '%s.%s' % (self.owner.namespace, self.key),
                self.value,
                self.owner.id
            )
        except Exception, e:
            print 'could not save %r for %s.  value was %r - %s' % (
                self, self.owner.id, self.value, str(e)
            )

        self.owner.save()
        return self.value


class AsyncInt(AsyncNumber, Int):

    namespace = 'sc-agg'



class AbstractSet(object):
    "A hack to prevent the import of django dependent fields"
    pass


def to_list(*args):
    if not args:
        return []
    value = args[0]
    return list(value) if isinstance(value, (list, tuple, set)) else [value,]


class FKList(Iter, AbstractSet):

    encoder = staticmethod(to_list)

    def to_json(self):
        return [str(element) for element in self.value]



class List(Iter):

    encoder = staticmethod(to_list)

    def append(self, value):
        self.value.append(value)

    def __getitem__(self, index):
        return self.value[index]


class ModelList(List):

    def encoder(self, *args):
        if args:
            if type(args[0]) == list:
                if type(args[0][0]) == dict:
                    return [self.model_class(**v) for v in args[0]]
                elif type(args[0][0]) == self.model_class:
                    return args[0]
            else:
                if type(args[0]) == dict:
                    return self.model_class(**args[0])
                elif type(args[0]) == self.model_class:
                    return args[0]
        return []

    def set(self, *args, **kwargs):
        try:
            self.value = self.encoder(args[0])
            if self.order_by:
                self.value = sorted(
                    self.value, key=lambda m: getattr(m, self.order_by),
                    reverse=True
                )
            self.updated = True
        except IndexError:
            self.value = self.get_default()

    def to_json(self):
        return [m.to_json() for m in self.value]


class Set(Iter, AbstractSet):

    encoder = staticmethod(to_list)

    def append(self, value):
        self.value = list(set(self.value).add(value))

    def get(self, name):
        if name in self.value:
            return name
        else:
            raise ValueError(
                '%r.%s does not contain the value you are looking for...' % (
                    self.owner, self.name
                )
            ), None, sys.exc_info()[2]


class Dict(Iter):

    encoder = staticmethod(dict)

    def items(self):
        return self.value.items()

    def get(self, key):
        return self.value.get(key)
