from django.db import IntegrityError
from django.db.models import Manager, signals
from django.db.models.fields import Field
from django.db.models.query import QuerySet, ValuesListQuerySet, ValuesQuerySet
from django.utils import six
from domingo.exceptions import QueryError

from collections import defaultdict


class DomingoForeignKey(object):
    """
        class MyModel(django.db.models.Model):
            ...
            ref_field = django.db.models.CharField(max_length=...)
            doc = DomingoForeignKey(
                MyDomingoModel, unique_on_field='ref_field'
            )
    """
    description = "Domingo foreign key"
    include_fields = None
    exclude_fields = None

    # Field flags
    auto_created = False
    concrete = False
    editable = False
    hidden = False

    is_relation = True
    many_to_many = False
    many_to_one = True
    one_to_many = False
    one_to_one = False
    related_model = None

    def __unicode__(self):
        return u'.'.join(['hello', ])

    def __init__(self, cls, *args, **kwargs):
        self.domingo_model = cls
        self.unique_on = cls.unique_on

        if 'include_fields' in kwargs:
            self.include_fields = kwargs.pop('include_fields')
        if 'exclude_fields' in kwargs:
            self.exclude_fields = kwargs.pop('exclude_fields')

        self.editable = False
        self.rel = None
        self.column = None

        # there should be a regular django field for each field listed in the
        # unique_on attribute on the referenced domingo model
        try:
            self.ref_fieldnames = {
                name: kwargs.pop(name) for name in self.unique_on
            }
        except KeyError:
            raise AttributeError(
                'Specify a reference field for each field listed in %s\'s %s.'
                'unique_on' % (self.__class__.__name__, cls.__name__)
            )
        super(DomingoForeignKey, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DomingoForeignKey, self).deconstruct()
        # Only include kwarg if it's not the default
        if self.separator != ",":
            kwargs['separator'] = self.separator
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        # django model
        self.django_model = cls
        cls._meta.add_field(self, virtual=True)
        if hasattr(cls._meta, 'domingo_foreign_key'):
            raise AttributeError('Only one DFK per model')
        # Only run pre-initialization field assignment on non-abstract models
        if not cls._meta.abstract:
            signals.pre_init.connect(self.instance_pre_init, sender=cls)
        cls._meta.domingo_foreign_key = name

        # Connect myself as the descriptor for this field
        setattr(cls, name, self)

    def instance_pre_init(self, signal, sender, args, kwargs, **_kwargs):
        if self.name in kwargs:
            domingo_instance = kwargs.pop(self.name)
            for fieldname, ref_fieldname in self.ref_fieldnames.items():
                kwargs[ref_fieldname] = getattr(domingo_instance, fieldname)
            setattr(self, self.cache_key, domingo_instance)

    @property
    def cache_key(self):
        return '_%s_domingo_instance' % self.name

    def __get__(self, instance, instance_type=None):
        if instance is None:
            raise AttributeError('')
        if not hasattr(instance, self.cache_key):
            search_opts = {
                fieldname: getattr(instance, ref_fieldname)
                for fieldname, ref_fieldname in self.ref_fieldnames.items()
            }
            if self.include_fields:
                search_opts['include'] = self.include_fields
            if self.exclude_fields:
                search_opts['exclude'] = self.exclude_fields
            try:
                domingo_instance = self.domingo_model.get(**search_opts)
            except QueryError, e:
                raise IntegrityError(str(e))
            setattr(instance, self.cache_key, domingo_instance)
        return getattr(instance, self.cache_key)

    def __set__(self, instance, value):
        if not isinstance(value, self.domingo_model):
            raise TypeError()
        for fieldname, ref_fieldname in self.ref_fieldnames.items():
            setattr(instance, ref_fieldname, getattr(value, fieldname))
        setattr(instance, self.cache_key, value)


class DomingoQuerySet(QuerySet):
    """
    Overrides the __iter__ method on the queryset so to allow the addition of
    the outlet instance into the model (relative to the outlet_key field)
    """

    _domingo_filter_opts = None
    _domingo_order_keys = None
    _domingo_instances_list = None

    def select_related(self, *args, **kwargs):
        if hasattr(self.model._meta, 'domingo_foreign_key'):
            if self.model._meta.domingo_foreign_key in args:
                self.requires_domingo = True
        return super(DomingoQuerySet, self).select_related(
            *[
                arg
                for arg in args
                if arg != getattr(
                    self.model._meta, 'domingo_foreign_key', None
                )
            ],
            **kwargs
        )

    @property
    def requires_domingo(self):
        if not hasattr(self, '_requires_domingo'):
            query = self.query
            if isinstance(query.select_related, bool):
                self._requires_domingo = query.select_related
            else:
                self._requires_domingo = False
        return self._requires_domingo

    @requires_domingo.setter
    def requires_domingo(self, value):
        self._requires_domingo = value

    def django_unique_key(self, instance):
        unique_on = self.dfk_field.domingo_model.unique_on
        ref_fieldnames = self.dfk_field.ref_fieldnames
        return '.'.join([
            unicode(getattr(instance, ref_fieldnames[name]))
            for name in unique_on
        ])

    def __iter__(self):
        self._fetch_all()

        is_data = isinstance(self, (ValuesQuerySet, ValuesListQuerySet))
        if is_data or not self.requires_domingo:
            for res in self._result_cache:
                yield res
        else:
            self._fetch_domingo_data()

            if self._domingo_order_keys:
                # logic for returning instances in the order specified by the
                # domingo outlets

                instance_lookup = defaultdict(list)
                for django_instance in self._result_cache:
                    unique_key = self.django_unique_key(django_instance)
                    instance_lookup[unique_key].append(
                        django_instance
                    )

                all_tokens = set(instance_lookup.keys())
                domingo_tokens = []

                for domingo_instance in self._domingo_instances_list:
                    token = domingo_instance.unique_key
                    instances = instance_lookup.get(token, [])
                    for instance in instances:
                        setattr(
                            instance,
                            '_%s_domingo_instance' % self.dfk_field.name,
                            domingo_instance
                        )
                        yield instance
                    domingo_tokens.append(token)

            else:

                all_tokens = []
                domingo_tokens = []

                for django_instance in self._result_cache:
                    unique_key = self.django_unique_key(django_instance)
                    domingo_instance = self._domingo_instances_lookup.get(
                        unique_key
                    )
                    all_tokens.append(unique_key)
                    if domingo_instance:
                        setattr(
                            django_instance,
                            '_%s_domingo_instance' % self.dfk_field.name,
                            domingo_instance
                        )
                        domingo_tokens.append(domingo_instance.unique_key)
                        yield django_instance

    def _get_domingo_opts(self):
        name = self.dfk_field.name
        ret = defaultdict(list)
        ref_fieldnames = self.dfk_field.ref_fieldnames
        for instance in self._result_cache:
            for fieldname, ref_fieldname in ref_fieldnames.items():
                ret[fieldname + "__in"].append(
                    getattr(instance, ref_fieldname)
                )
        setattr(self, '_%s_opts' % name, dict(ret))
        opts = getattr(self, '_%s_opts' % name)
        self._domingo_filter_opts = getattr(self, '_domingo_filter_opts') or {}
        opts.update(self._domingo_filter_opts)
        return opts

    @property
    def dfk_field(self):
        if not hasattr(self, '_dfk_field'):
            self._dfk_field = self.model._meta.get_field(
                self.model._meta.domingo_foreign_key
            )
        return self._dfk_field

    def _fetch_domingo_data(self):
        """
        Get the outlets via a mongo cursor and assign them to the 'hidden'
        attribute _domingo_instances_lookup. _domingo_instances_lookup is a
        dict that returns the outlet instance for a given outlet_token.
        """
        opts = self._get_domingo_opts()
        DomingoModel = self.dfk_field.domingo_model
        count = DomingoModel.filter(**opts).count()
        _lim = 40
        self._domingo_instances_lookup = {}
        self._domingo_instances_list = []

        key_parts = None
        if self._domingo_order_keys:
            key = self._domingo_order_keys[0]
            key_parts = (key, int(not key.startswith('-')))

        if count > 2 * _lim:
            pages = count / _lim
            for idx in range(0, pages + 1):
                cursor = DomingoModel.filter(**opts)
                if key_parts:
                    cursor = cursor.sort(*key_parts)
                cursor = cursor.limit(_lim).skip(idx * _lim)
                if self._domingo_order_keys:
                    for outlet in cursor:
                        self._domingo_instances_list.append(outlet)
                else:
                    self._domingo_instances_lookup.update(
                        {
                            outlet.unique_key: outlet
                            for outlet in cursor
                        }
                    )
        else:
            cursor = DomingoModel.filter(**opts)
            if key_parts:
                cursor = DomingoModel.filter(**opts)
                self._domingo_instances_list = cursor.sort(*key_parts)
            else:
                self._domingo_instances_lookup.update(
                    {
                        outlet.unique_key: outlet for outlet in cursor
                    }
                )

    def __getitem__(self, k):
        """
        Retrieves an item or slice from the set of results.
        """
        if not isinstance(k, (slice,) + six.integer_types):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0)) or
                (isinstance(k, slice) and (k.start is None or k.start >= 0) and
                 (k.stop is None or k.stop >= 0))), \
            "Negative indexing is not supported."

        # if self._result_cache is not None:
        #     return self._result_cache[k]

        if isinstance(k, slice):
            qs = self._clone()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.query.set_limits(start, stop)
            return list(qs)[::k.step] if k.step else qs

        qs = self._clone()
        qs.query.set_limits(k, k + 1)
        return list(qs)[0]

    def filter(self, *args, **kwargs):
        _domingo_filter_opts = {}
        dfk_fieldname = self.dfk_field.name
        domingo_model = self.dfk_field.domingo_model
        for key, value in kwargs.items():
            key_parts = key.split('__')
            if dfk_fieldname in key_parts:
                idx = key_parts.index(dfk_fieldname)
                lk = '__'.join(key_parts[idx + 1:])
                if isinstance(value, domingo_model) and not lk:
                    for name in domingo_model.unique_on:
                        _domingo_filter_opts[name] = getattr(value, name)
                elif lk == 'in' and hasattr(value, '__iter__'):
                    for name in domingo_model.unique_on:
                        _domingo_filter_opts[name + '__in'] = []
                    for val in value:
                        for name in domingo_model.unique_on:
                            try:
                                _domingo_filter_opts[name + '__in'].append(
                                    getattr(val, name)
                                )
                            except AttributeError:
                                pass
                else:
                    _domingo_filter_opts[lk] = value
                del kwargs[key]
        ###################################################################
        # Ensures that the filter will always generate sql
        # TODO: use the ids from this query to later retrieve the outlet
        # data
        if _domingo_filter_opts:
            dfk_field = self.dfk_field
            DomingoModel = self.dfk_field.domingo_model
            domingo_instances = DomingoModel.filter(
                include=DomingoModel.unique_on,
                **_domingo_filter_opts
            )
            ref_fieldnames = dfk_field.ref_fieldnames
            for fieldname, ref_fieldname in ref_fieldnames.items():
                kwargs.update(
                    {
                        ref_fieldname + '__in': [
                            getattr(instance, fieldname)
                            for instance in domingo_instances
                        ]
                    }
                )
        #######################################################################
        qs = super(DomingoQuerySet, self).filter(*args, **kwargs)
        qs._domingo_filter_opts = dict(_domingo_filter_opts)
        return qs

    def values_list(self, *fields, **kwargs):
        if self.requires_domingo:
            for field in fields:
                if self.dfk_field.name in field.split('__'):
                    raise NotImplementedError(
                        'values_list has not been impletemented for '
                        'domingo models'
                    )
        return super(DomingoQuerySet, self).values_list(*fields, **kwargs)

    def values(self, *fields, **kwargs):
        if self.requires_domingo:
            for field in fields:
                if self.dfk_field.name in field.split('__'):
                    raise NotImplementedError(
                        'values has not been impletemented for domingo '
                        'models'
                    )
        return super(DomingoQuerySet, self).values(*fields, **kwargs)

    def order_by(self, *args, **kwargs):
        pattern = '%s__' % self.dfk_field.name
        keys = [
            key for key in args
            if key.startswith(pattern) or key.startswith('-' + pattern)
        ]
        _domingo_order_keys = [
            key.replace(pattern, '') for key in keys
        ]
        if len(_domingo_order_keys) > 1:
            raise ValueError(
                "Domingo models can only be sorted by one field at a time. "
                "'%s' keys found." % _domingo_order_keys
            )

        args = tuple(set(args) - set(keys))
        self._domingo_order_keys = _domingo_order_keys
        self.requires_domingo = bool(_domingo_order_keys)
        return super(DomingoQuerySet, self).order_by(*args, **kwargs)

    def _clone(self):
        clone = super(DomingoQuerySet, self)._clone()
        clone._domingo_order_keys = self._domingo_order_keys
        clone._domingo_filter_opts = self._domingo_filter_opts
        clone.requires_domingo = self.requires_domingo
        # clone._domingo_instances_list = self._domingo_instances_list
        return clone

    def exists(self):
        django_exists = super(DomingoQuerySet, self).exists()
        if self.requires_domingo and self._domingo_filter_opts:
            if not self._result_cache:
                self._fetch_all()
            DomingoModel = self.dfk_field.domingo_model
            opts = self._get_domingo_opts()
            domingo_exists = bool(
                DomingoModel.filter(**opts).count()
            )
            return django_exists and domingo_exists
        return django_exists

    def count(self):
        if self.requires_domingo and self._domingo_filter_opts:
            return len(list(self))
        return super(DomingoQuerySet, self).count()


class DomingoManager(Manager):

    def get_queryset(self):
        return DomingoQuerySet(self.model)
