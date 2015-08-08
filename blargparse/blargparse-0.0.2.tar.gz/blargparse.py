import argparse

class BlargParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(BlargParser, self).__init__(*args, **kwargs)
        self._aggregates = []
        self._aggregate_dests = set()

    def add_aggregate(self, dest = None, func = lambda args:None):
        if dest:
            if dest in self._aggregate_dests:
                raise AttributeError('Aggregate named %s already exists' % dest)
            elif not isinstance(dest, str):
                raise TypeError('Aggregate dest must be str type.')
            else:
                self._aggregate_dests.add(dest)
                def g(args):
                    setattr(args, dest, func(args))
        else:
            g = func

        self._aggregates.append(g)

    def add_subparsers(self, **kwargs):
        out = super(BlargParser, self).add_subparsers(**kwargs)
        self._blarg_children = out
        return out

    def parse_args(self, *args, **kwargs):
        namespace = super(BlargParser, self).parse_args(*args, **kwargs)

        for descendant in self._blarg_descendants():
            for func in descendant._aggregates:
                func(namespace)

        return namespace

    def _blarg_descendants(self):
        yield self
        if hasattr(self, '_blarg_children'):
            for child in dict(self._blarg_children._get_kwargs())['choices'].values():
                yield from child._blarg_descendants()
