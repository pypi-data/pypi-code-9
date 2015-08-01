from itertools import cycle

__all__ = ['Mode', 'AllMode', 'DistibuteMode']


class Mode:

    name = None

    def __init__(self, nodes, commands):
        self.nodes = nodes
        self.commands = commands

    def __iter__(self):
        raise NotImplemented

    def __len__(self):
        raise NotImplemented


class AllMode(Mode):

    name = 'all'

    def __init__(self, nodes, commands):
        self.nodes = nodes
        self.commands = commands

    def __iter__(self):
        for command in self.commands:
            for node in self.nodes:
                yield node, command

    def __len__(self):
        return len(self.commands) * len(self.nodes)


class DistibuteMode(Mode):

    name = 'distribute'

    def __init__(self, nodes, commands):
        self.nodes = nodes
        self.commands = commands

    def __iter__(self):
        nodes = cycle(self.nodes)
        for command in self.commands:
            node = next(nodes)
            yield node, command

    def __len__(self):
        return len(self.commands)
