import random
from datetime import datetime, date, timedelta
from faker import Factory


fake = Factory.create()

class Field(object):
    def __init__(self, *args, **kwargs):
        self.var = kwargs.pop('var', None)
        self.transform = kwargs.pop('transform', lambda x: x)

        self.setup(*args, **kwargs)

    def get(self, context):
        try:
            return context['_' + self.var]

        except:
            result = self.process(context)
            result =  self.transform(result)

            if self.var:
                context['_' + self.var] = result

            return result

    def setup(self, value=None):
        self.value = value
        
    def process(self, context):
        return hasattr(self.value, '__call__') and self.value() or self.value 


class NameField(Field):
    def setup(self):
        self.value = fake.name
        

class ListField(Field):
    def setup(self, seq):
        self.seq = seq

    def process(self, context):
        return random.choice(self.seq)


class WeightedListField(ListField):
    def process(self, context):
        cumulative_weights = sum(x[1] for x in self.seq)
        r = random.uniform(0, cumulative_weights)

        offset = 0
        for value, weight in self.seq:
            offset += weight
            if r < offset:
                return value


class GaussianField(Field):
    def setup(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def process(self, context):
        return random.gauss(self.mu, self.sigma)


class CloneField(Field):
    def setup(self, cloning):
        self.cloning = cloning

    def process(self, context):
        return context.get(self.cloning)


class MapField(CloneField):
    def setup(self, cloning, mapping, default=None):
        super(MapField, self).setup(cloning)
        self.mapping = mapping
        self.default = default

    def process(self, context):
        result = super(MapField, self).process(context)
        return self.mapping.get(result, self.default)


class IncrementField(Field):
    def setup(self, start=1):
        self.idx = start-1

    def process(self, context):
        self.idx += 1
        return self.idx


class DateTimeField(Field):
    def setup(self, minimum=None, maximum=None, format=None):
        self.min = minimum
        self.max = maximum
        self.format = format

    def process(self, context):
        min_dt = self.min or datetime.now()
        max_dt = self.max or datetime.now()

        delta = int((max_dt - min_dt).total_seconds())
        random_seconds = random.randint(0, delta)
        random_dt = min_dt + timedelta(seconds=random_seconds)

        return random_dt.strftime(self.format) if self.format else random_dt


class DateField(DateTimeField):
    def process(self, *args, **kwargs):
        res = super(DateField, self).process(*args, **kwargs)
        return res.date() if isinstance(res, datetime) else res
