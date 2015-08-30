"""
.. pakage:: dataholder
    :synopsis: Trick for assignment in an if statement
"""
__version__ = '1.0.1'
__email__ = '@'.join(['petr.cons', 'gmail.com'])
__license__ = 'MIT'


class DataHolder(object):
    def __init__(self, value=None, attr_name='value'):
        self._attr_name = attr_name
        self.set(value)

    def __call__(self, value):
        return self.set(value)

    def set(self, value):
        setattr(self, self._attr_name, value)
        return value

    def get(self):
        return getattr(self, self._attr_name)
