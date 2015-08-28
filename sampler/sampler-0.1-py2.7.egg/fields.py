import random
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
        if hasattr(self.value, '__call__'):
            return self.value()
        else:
            return self.value


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
