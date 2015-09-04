try:   # pragma: no cover
    from collections.abc import Mapping
except ImportError:   # pragma: no cover
    # python < 3.0
    from collections import Mapping
from copy import deepcopy


def merge_recursively(base, data):
    dest = deepcopy(base)
    for key, value in data.items():
        orig = base.get(key, None)
        if isinstance(orig, Mapping) and isinstance(value, Mapping):
            value = merge_recursively(orig, value)
        dest[key] = value
    return dest


class Overdub(Mapping):
    """Access mapping as a layer.

    When possible, keys will be accessed as attributes.

    For example:

    >>> overdub = Overdub({'foo': 1, 'bar': {'baz': 'qux'}})
    >>> overdub.foo
    1
    >>> overdub['foo']
    1
    """

    def __init__(self, data=None):
        self._ = data or {}

    def __getitem__(self, key):
        try:
            value = self._[key]
        except KeyError:
            raise KeyError('Key %r is not defined' % key)
        if isinstance(value, dict):
            value = self.__class__(value)
        return value

    def __iter__(self):
        return iter(self._)

    def __len__(self):
        return len(self._)

    def __getattr__(self, name):
        """
        Fallback to current data key if attr is not setted.
        """

        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError("%r object has no attribute %r" % (
                self.__class__.__name__, name
            ))


class MutableOverdub(Overdub):
    """A Overdub with mutability abilities.
    """

    def update(self, data):
        """Update data

        Parameters:
            data (dict): data to be updated
        """
        return self._.update(data)

    def merge(self, data):
        """Merge data

        Parameters:
            data (dict): data to be merged
        """
        data = merge_recursively(self._, data)
        return self._.update(data)

    def rebase(self, data):
        """Rebase data

        Parameters:
            data (dict): data to be rebase
        """
        data = merge_recursively(data, self._)
        return self._.update(data)

    def frozen(self):
        """froze data

        Returns:
            Overdub: the frozen data
        """
        return Overdub(self._)
