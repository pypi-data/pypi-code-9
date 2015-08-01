import math

__all__ = ['Concurrency']


class Concurrency:

    def __init__(self, *, size=None, part=None):
        if size and part:
            raise ValueError('size and part are mutually exclusive')

        self.size = size
        self.part = part

    def batch(self, collection):
        if self.size:
            return self.size
        if self.part:
            return math.ceil(len(collection) / 100 * self.part)
        return len(collection)

    def __repr__(self):
        if self.size:
            return '<Concurrency(size=%r)>' % self.size
        if self.part:
            return '<Concurrency(part=%r)>' % self.part

        return '<Concurrency>'
