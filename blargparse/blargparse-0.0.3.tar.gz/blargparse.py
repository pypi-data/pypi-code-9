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

        subparser_id = getattr(self, '_blarg_subparser_dest', None)
        self._aggregates.append((subparser_id, g))

    def add_subparsers(self, dest = 'subparser'):
        out = super(BlargParser, self).add_subparsers(dest = dest)
        self._blarg_subparser_dest = dest
        self._blarg_children = out
        return out

    def parse_args(self, *args, **kwargs):
        namespace = super(BlargParser, self).parse_args(*args, **kwargs)
        self._aggregate(namespace)
        return namespace

    def _aggregate(self, namespace):
        for subparser_id, func in self._aggregates:
            if subparser_id == None or subparser_id == self._blarg_subparser_dest:
                func(namespace)

        if hasattr(self, '_blarg_children'):
            for key, value in dict(self._blarg_children._get_kwargs())['choices'].items():
                if key == getattr(namespace, self._blarg_subparser_dest):
                    value._aggregate(namespace)
