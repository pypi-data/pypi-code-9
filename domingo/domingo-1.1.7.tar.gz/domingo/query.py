from .support import calculate_derivatives
from logging import getLogger


logger = getLogger('time_logger')


class QueryMixin(object):

    def pre_save(self):
        """
            called before save
        """
        pass

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.store.filter(*args, **kwargs)

    @classmethod
    def all(cls):
        return cls.store.all()

    @classmethod
    def search(cls, keyword, **kwargs):

        return cls.store.filter(
            text_search=keyword,
            projection = {'db_text_score': {'$meta': "textScore"}},
            **kwargs).sort("textScore")

    @classmethod
    def get(cls, **kwargs):
        """
            needs a kwarg like:
                outlet_token=qlrejfnweiruybf
        """
        return cls.store.get(**kwargs)

    def get_derivative(self, attribute_pair, depth=2):
        if hasattr(self, 'time_series') and len(self.time_series) >= depth:
            return calculate_derivatives(
                self.time_series, [attribute_pair], depth
            )
        return 0

    @classmethod
    def get_latest_maxima_list(cls, exclude=None):
        obj = cls()
        pipe = obj.redis.pipeline()

        outfields = []

        for name, field in obj.number_fields.items():
            if exclude is not None and name in exclude:
                continue
            outfields.append(name)
            pipe.zrevrangebyscore(
                '%s.%s' % (obj.namespace, field.key),
                'INF', 0, 0, 1, withscores=True
            )
        data = pipe.execute()
        if data:
            return {f: data[i][0][1] for i, f in enumerate(outfields)}

    @classmethod
    def create(cls, data=None, pipe=None):
        data = data if isinstance(data, list) else [data]
        cls.store.save(data=data, created=True)
        return data

    @classmethod
    def update(cls, queryset, **kwargs):
        for m in queryset:
            for key, val in kwargs.items():
                getattr(m,key).set(val)
            m._id.updated = True
        cls.store.save(data=queryset, created=True, fields=kwargs.keys())

        return queryset

    def save(self, fields=None):
        self.store.save(data=[self], fields=fields)
        return self
