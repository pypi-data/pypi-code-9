class Stack(object):
    def __init__(self, name):
        self.name = name

    def outputs(self, conn):
        stacks = conn.describe_stacks(self.name)
        if len(stacks) == 0:
            raise Exception('No such stack: {}'.format(self.name))

        return {o.key: o.value for o in stacks[0].outputs}


class Resolver(object):
    def __init__(self, outputs):
        self.outputs = outputs

    def __call__(self, stack, key):
        try:
            return self.outputs[stack][key]
        except KeyError as e:
            raise ResolutionError(stack, key, e)


class ResolutionError(Exception):
    def __init__(self, stack, key, exc):
        self.stack = stack
        self.key = key
        self.exc = exc

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return (
            'Could not resolve output from stack: '
            'stack={} '
            'key={} '
            'exc={}'
            .format(self.stack, self.key, str(self.exc))
        )
