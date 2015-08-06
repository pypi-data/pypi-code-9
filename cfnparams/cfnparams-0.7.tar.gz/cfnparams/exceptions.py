
class ResolutionError(Exception):
    def __init__(self, stack, output):
        self.stack = stack
        self.output = output

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return (
            'Could not resolve output "{}" from stack "{}"'
            .format(self.output, self.stack)
        )
