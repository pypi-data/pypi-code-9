import collections

class NodeException(Exception):
    pass

class Node(object):

    def __init__(self, start_node = None):
        self.nodes = collections.defaultdict(set)
        self._node_start = start_node
        if start_node:
            self.nodes[start_node] = set()

    def __str__(self):
        return str(self.nodes)

    def add_vertex(self, vertex):
        if self.nodes.has_key(vertex):
            raise NodeException("vertex already exists")
        self.nodes[vertex] = set()

    def add_edge(self, edge):
        v1, v2 = edge
        self.nodes[v1].add(v2)
        self.nodes[v2].add(v1)

    @property
    def node_start(self):
        return self._node_start

Edge = collections.namedtuple('Edge', ['v1', 'v2'])
