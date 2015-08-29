from fields import *


class Sampler(object):
    def __init__(self, **kwargs):
        self._seed = False

        for k, v in kwargs.iteritems():
            if not isinstance(v, Field) and not isinstance(v, Sampler):
                # v = Field(v)
                getattr(self, k).value = v
            else:
                setattr(self, k, v)


    def seed(self, seed):
        self._seed = seed
        return self

    def generate(self, count=None):
        if self._seed:
            random.seed(self._seed)

        if count is None:
            return self.generate_one()
        else:
            return [self.generate_one() for i in range(count)]

    def generate_one(self):
        data = {}

        for name, obj in self.get_fields():
            if isinstance(obj, Field):
                data[name] = obj.get(context=data)
            elif isinstance(obj, Sampler):
                data[name] = obj.generate()
            
        return dict([(k, v) for k, v in data.iteritems() if not k.startswith('_')])
        
    def get_fields(self):
        for param_name in dir(self):
            param_obj = getattr(self, param_name)
            if isinstance(param_obj, Field) or isinstance(param_obj, Sampler):
                yield (param_name, param_obj)
