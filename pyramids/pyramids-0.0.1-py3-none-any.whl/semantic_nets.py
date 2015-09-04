# =========================================================================
# semantic_nets.py
# by Aaron Hosford
# 3/11/2011
# =========================================================================
#
# Description:
#   This module implements the underlying semantic net-related data
#   structures used by semantics.py and its relatives.
#
# =========================================================================
#
# Contents:
#
#   class LinkSet
#     Tracks links entering or leaving a Node in a semantic net, and the
#     data values associated with them.
#
#   class Link
#     A simple directed edge between Nodes in a semantic net, labeled with
#     a type to indicate its purpose/meaning and arbitrary additional data
#     determined by client usage.
#
#   class Node
#     A vertex in a semantic net, labeled with arbitrary data determined by
#     client usage.
#
#   class Net
#     A collection of interconnected Nodes, serving as a semantic net.
#
#   class Mapping
#     Allows node mappings to be analyzed in terms of preservation of
#     structure, i.e. homo- and isomorphisms. (This class is not currently
#     integrated with other components in the module.)
#
#   class TypeID
#     Base class for the three reservable types: LinkType, LinkDataType,
#     and NodeDataType.
#
#   class LinkType
#     A named kind of link.
#
#   class LinkDataType
#     A named key for link data.
#
#   class NodeDataType
#     A named key for node data.
#
#   def reserve_link_type
#     Reserve a new LinkType instance by name.
#
#   def get_link_type
#     Retrieve an existing LinkType instance by name.
#
#   def reserve_link_data_type
#     Reserve a new LinkDataType instance by name.
#
#   def get_link_data_type
#     Retrieve an existing LinkDataType instance by name.
#
#   def reserve_node_data_type
#     Reserve a new NodeDataType instance by name.
#
#   def get_node_data_type
#     Retrieve an existing NodeDataType instance by name.
#
# =========================================================================
#
# Modification History:
#
#   6/26/2011:
#     - Created this file and migrated the LinkSet, Link, Node, Net, and
#       Mapping classes to it from semantics2.py.
#
#   6/27/2011:
#     - Added TypeID and its subclasses, together with convenience methods
#       for reserving them by name.
#     - Renamed Node.outgoing_links to outgoing and Node.incoming_links to
#       incoming.
#     - Added the get_unique_link method to the LinkSet class.
#     - Added the iter_nodes method to the LinkSet class.
#
# =========================================================================


from sys import intern

import constants


# Serves to group links together by their types.
class LinkSet:

    def __init__(self, outgoing):
        self._links = {}
        self._outgoing = bool(outgoing)

    def types(self):
        return tuple(self._links)

    def iter_types(self):
        return iter(self._links)

    def count_types(self):
        return len(self._links)

    def add_type(self, link_type):
        if link_type not in self._links:
            if self._outgoing:
                self._links[link_type] = {}
            else:
                self._links[link_type] = set()

    def remove_type(self, link_type):
        if link_type in self._links:
            del self._links[link_type]

    def has_type(self, link_type):
        return link_type in self._links

    def links(self, link_type=None):
        if link_type is None:
            return sum(
                [tuple(self._links[link_type])
                 for link_type in self._links],
                ()
            )
        else:
            return tuple(self._links.get(link_type, ()))

    def iter_links(self, link_type=None):
        if link_type is None:
            for link_type in self._links:
                for link in self._links[link_type]:
                    yield link
        else:
            for link in self._links.get(link_type, ()):
                yield link

    def count_links(self, link_type=None):
        if link_type is None:
            return sum([len(self._links[link_type])
                        for link_type in self._links])
        else:
            return len(self._links.get(link_type, ()))

    def add_link(self, link):
        self.add_type(link.type)
        if self._outgoing:
            self._links[link.type][link] = {}
        else:
            self._links[link.type].add(link)

    def remove_link(self, link):
        if self.has_type(link.type) and link in self._links[link.type]:
            if self._outgoing:
                self._links[link.type].pop(link)
            else:
                self._links[link.type].remove(link)
            if not self._links[link.type]:
                self.remove_type(link.type)

    def has_link(self, link):
        return self.has_type(link.type) and link in self._links[link.type]

    def has_unique_link(self, link_type):
        return (
            link_type in self._links and
            len(self._links[link_type]) == 1
        )

    def get_unique_link(self, link_type):
        if link_type not in self._links:
            raise KeyError("No link of this type exists.")
        if len(self._links[link_type]) > 1:
            raise KeyError("Multiple links of this type exist.")
        for link in self._links[link_type]:
            return link

    def get_unique_node(self, link_type):
        if self._outgoing:
            return self.get_unique_link(link_type).sink
        else:
            return self.get_unique_link(link_type).source

    def iter_nodes(self, link_type=None):
        if self._outgoing:
            for link in self.iter_links(link_type):
                yield link.sink
        else:
            for link in self.iter_links(link_type):
                yield link.source

    def data(self, link):
        if not self._outgoing:
            raise TypeError("Data is only stored with outgoing links.")
        if self.has_type(link.type):
            return self._links[link.type][link]
        else:
            return None


# Represents a relationship or connection between concepts as an edge/link
# in the semantic network
class Link:

    def __init__(self, source, link_type, sink):
        self._type = link_type
        self._source = source
        self._sink = sink
        if not isinstance(source, Node):
            raise TypeError(source, Node)
        if not isinstance(sink, Node):
            raise TypeError(sink, Node)

    def __hash__(self):
        return hash(self.type) ^ hash(self.source) ^ hash(self.sink)

    def __eq__(self, other):
        if not isinstance(other, Link):
            return NotImplemented
        return (
            self.type == other.type and
            self.source == other.source and
            self.sink == other.sink
        )

    def __ne__(self, other):
        if not isinstance(other, Link):
            return NotImplemented
        return not (
            self.type == other.type and
            self.source == other.source and
            self.sink == other.sink
        )

    def __lt__(self, other):
        if not isinstance(other, Link):
            return NotImplemented
        if self.type != other.type:
            return self.type < other.type
        if self.source != other.source:
            return self.source < other.source
        return self.sink < other.sink

    def __le__(self, other):
        if not isinstance(other, Link):
            return NotImplemented
        if self.type != other.type:
            return self.type < other.type
        if self.source != other.source:
            return self.source < other.source
        return self.sink <= other.sink

    def __gt__(self, other):
        if not isinstance(other, Link):
            return NotImplemented
        if self.type != other.type:
            return self.type > other.type
        if self.source != other.source:
            return self.source > other.source
        return self.sink > other.sink

    def __ge__(self, other):
        if not isinstance(other, Link):
            return NotImplemented
        if self.type != other.type:
            return self.type > other.type
        if self.source != other.source:
            return self.source > other.source
        return self.sink >= other.sink

    @property
    def type(self):
        return self._type

    @property
    def source(self):
        return self._source

    @property
    def sink(self):
        return self._sink

    @property
    def data(self):
        return self.source.outgoing.data(self)

    def __bool__(self):
        return self.is_connected()

    def is_connected(self):
        return self.source.outgoing.has_link(self)

    def connect(self):
        self.source.outgoing.add_link(self)
        self.sink.incoming.add_link(self)

    def disconnect(self):
        self.source.outgoing.remove_link(self)
        self.sink.incoming.remove_link(self)


# Represents a concept as a node/vertex in the semantic network
class Node:

    def __init__(self, net):
        self._net = net
        self._outgoing = LinkSet(True)
        self._incoming = LinkSet(False)
        self._data = {}

    @property
    def net(self):
        return self._net

    @property
    def data(self):
        return self._data

    @property
    def outgoing(self):
        return self._outgoing

    @property
    def incoming(self):
        return self._incoming

    def disconnect(self):
        for link in self._outgoing.links():
            link.disconnect()
        for link in self._incoming.links():
            link.disconnect()

    def has_path(self, end, link_types):
        finished = set()
        started = {self}
        while started and end not in started:
            finished |= started
            new = set()
            for node in started:
                for link_type, direction in link_types:
                    if direction is None or direction:
                        for link in node.outgoing.iter_links(link_type):
                            new.add(link.sink)
                    if direction is None or not direction:
                        for link in node.incoming.iter_links(link_type):
                            new.add(link.source)
            started = new - finished
        return end in started


# Represents a semantic net as a collection of nodes and links forming a
# graph
class Net:

    def __init__(self):
        self._nodes = set()

    def add_node(self):
        node = Node(self)
        self._nodes.add(node)
        return node

    def remove_node(self, node):
        node.disconnect()
        self._nodes.discard(node)

    def nodes(self):
        return self._nodes.copy()

    def iter_nodes(self):
        return iter(self._nodes)

    def count_nodes(self):
        return len(self._nodes)


class TypeID:

    def __init__(self, name):
        self._name = intern(name)

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name

    def __repr__(self):
        return type(self).__name__ + "(" + repr(self._name) + ")"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name is other.name

    def __ne__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._name is not other.name

    def __hash__(self):
        return id(self._name)


class LinkType(TypeID):
    pass  # Subclassing makes == and != work properly.


class LinkDataType(TypeID):
    pass  # Subclassing makes == and != work properly.


class NodeDataType(TypeID):
    pass  # Subclassing makes == and != work properly.


_link_types = constants.Constants()
_link_data_types = constants.Constants()
_node_data_types = constants.Constants()


def reserve_link_type(name, owner):
    _link_types.reserve(name, LinkType(name), owner)
    return _link_types.get_value(name)


def get_link_type(name):
    _link_types.get_value(name)


def reserve_link_data_type(name, owner):
    _link_data_types.reserve(name, LinkDataType(name), owner)
    return _link_data_types.get_value(name)


def get_link_data_type(name):
    return _link_data_types.get_value(name)


def reserve_node_data_type(name, owner):
    _node_data_types.reserve(name, NodeDataType(name), owner)
    return _node_data_types.get_value(name)


def get_node_data_type(name):
    return _node_data_types.get_value(name)
