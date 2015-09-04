# =========================================================================
# Module:  sentence.py
# Author:  Aaron Hosford
# Created: 06/26/2011
#
# Copyright (c) Aaron Hosford 2011, all rights reserved.
# =========================================================================
#
# Description:
#   Provides sentence reading and construction functionality for
#   semantics2.py
#
# =========================================================================
#
# Contents:
#
#   class SentenceBuilder
#     Provides mechanisms for construction of new sentences.
#
#   class Sentence
#     Provides mechanisms for reading the structure of existing sentences.
#
# =========================================================================
#
# Modification History:
#
#   06/26/2011:
#     - Created this module.
#
# =========================================================================
# !/usr/bin/env python


import semantic_nets
import words


# TODO: Make this able to utilize a parser to construct a set of parse
#       trees that correspond to the sentence, and pick the one that has
#       the best score.
# TODO: Create Query class which represents the satisfaction set of a
#       sentence in terms of the actual logical structure, and which can
#       retrieve other queries or actual facts related to its meaning.
#       Then give this class a method that builds a Query instance
#       corresponding to it.
class Sentence:

    CONTAINS = semantic_nets.reserve_link_type(
        "SENTENCE CONTAINS",
        __name__
    )

    HEAD = semantic_nets.reserve_link_type("SENTENCE HEAD", __name__)
    SOURCE = semantic_nets.reserve_link_type("SENTENCE SOURCE", __name__)
    NEXT = semantic_nets.reserve_link_type("NEXT WORD USE", __name__)

    NODE_INDEX = semantic_nets.reserve_node_data_type(
        "WORD USE NODE INDEX",
        __name__
    )

    SYNTACTIC_CATEGORY = semantic_nets.reserve_node_data_type(
        "SENTENCE SYNTACTIC CATEGORY",
        __name__
    )

    def __init__(self, root_node):
        self._root_node = root_node

    @property
    def root_node(self):
        return self._root_node

    @property
    def category(self):
        return self.root_node.data[self.SYNTACTIC_CATEGORY]

    @property
    def source(self):
        return self.root_node.outgoing.get_unique_link(self.SOURCE).sink

    @property
    def head(self):
        return self.root_node.outgoing.get_unique_link(self.HEAD).sink

    def __str__(self):
        return self.to_str()

    def to_str(self, show_all=True):
        word_uses = self.sorted_word_uses()

        if not show_all:
            # Restrict nodes to those that are reachable from the head node
            # via forward paths inside the sentence.
            word_uses = [
                word_use
                for word_use in word_uses
                if self.has_path(
                    self.head,
                    word_use.root_node,
                    valid_nodes=lambda node: node in self,
                    forward_only=True
                )
            ]

        result = str(self.category) + ':'
        for word_use in word_uses:
            result += '\n  '
            if word_use.root_node == self.head:
                result += '*'
            result += str(word_use) + ':'
            inner_links = [
                link
                for link in word_use.root_node.outgoing.iter_links()
                if link.sink in self
            ]
            inner_links.sort(
                key=lambda l: (l.sink.data[self.NODE_INDEX], l.type)
            )
            for link in inner_links:
                result += (
                    '\n    ' + str(link.type) + ': ' +
                    str(words.WordUse(link.sink))
                )
        return result

    def __contains__(self, node):
        return bool(semantic_nets.Link(
            self.root_node,
            self.CONTAINS,
            node
        ))

    def __iter__(self):
        for node in self.root_node.outgoing.iter_nodes(self.CONTAINS):
            yield node

    def __len__(self):
        result = 0
        for _ in self:
            result += 1
        return result

    def iter_word_uses(self):
        for node in self:
            yield words.WordUse(node)

    def sorted_word_uses(self):
        return sorted(
            self.iter_word_uses(),
            key=lambda word_use: word_use.root_node.data[self.NODE_INDEX]
        )

    def iter_links(self):
        for node in self:
            for link in node.outgoing.iter_links():
                if link.sink in self:
                    yield link

    def _iter_paths(self, source, sink, valid_nodes, valid_links,
                    forward_only, covered_nodes):
        if source is sink:
            yield []
        else:
            covered_nodes = covered_nodes.copy()
            covered_nodes.add(source)
            for link in source.outgoing.iter_links():
                if (link.sink not in self or
                        link.sink in covered_nodes or
                        (valid_links is not None and
                         not valid_links(link)) or
                        (valid_nodes is not None and
                         not valid_nodes(link.sink))):
                    continue
                for tail in self._iter_paths(
                        link.sink,
                        sink,
                        valid_nodes,
                        valid_links,
                        forward_only,
                        covered_nodes):
                    yield [link] + tail
            if not forward_only:
                for link in source.incoming.iter_links():
                    if (link.source not in self or
                            link.source in covered_nodes or
                            (valid_links is not None and
                             not valid_links(link)) or
                            (valid_nodes is not None and
                             not valid_nodes(link.source))):
                        continue
                    for tail in self._iter_paths(
                            link.source,
                            sink,
                            valid_nodes,
                            valid_links,
                            forward_only,
                            covered_nodes):
                        yield [link] + tail

    def iter_paths(self, source, sink, valid_nodes=None, valid_links=None,
                   forward_only=True):
        return self._iter_paths(source, sink, valid_nodes, valid_links,
                                forward_only, set())

    def _has_path(self, source, sink, valid_nodes, valid_links,
                  forward_only, covered_nodes):
        if source is sink:
            return True
        covered_nodes = covered_nodes.copy()
        covered_nodes.add(source)
        for link in source.outgoing.iter_links():
            if (link.sink not in self or
                    link.sink in covered_nodes or
                    (valid_links is not None and
                     not valid_links(link)) or
                    (valid_nodes is not None and
                     not valid_nodes(link.sink))):
                continue
            if self._has_path(link.sink, sink, valid_nodes, valid_links,
                              forward_only, covered_nodes):
                return True
        if not forward_only:
            for link in source.incoming.iter_links():
                if (link.source not in self or
                        link.source in covered_nodes or
                        (valid_links is not None and
                         not valid_links(link)) or
                        (valid_nodes is not None and
                         not valid_nodes(link.source))):
                    continue
                if self._has_path(link.source, sink, valid_nodes,
                                  valid_links, forward_only,
                                  covered_nodes):
                    return True
        return False

    def has_path(self, source, sink, valid_nodes=None, valid_links=None,
                 forward_only=True):
        return self._has_path(source, sink, valid_nodes, valid_links,
                              forward_only, set())

    def has_linchpin(self, link):
        for node1 in self:
            for node2 in self:
                if node1 is node2:
                    continue
                if not self.has_path(
                        node1,
                        node2,
                        valid_links=lambda l: l is not link,
                        forward_only=False):
                    return True
        return False

    def iter_linchpins(self):
        for link in self.iter_links():
            if self.has_linchpin(link):
                yield link

    def get_depths(self):
        ranks = {}
        for node in self:
            ranks[node] = 0
            for link in node.incoming.iter_links():
                if link.source in self:
                    ranks[node] += 1
        depths = {}
        depth = 0
        while ranks:
            min_rank = min(ranks.values())
            found = set()
            for node in ranks:
                if ranks[node] == min_rank:
                    found.add(node)
            for node in found:
                del ranks[node]
                depths[node] = depth
                for link in node.outgoing.iter_links():
                    if link.sink in ranks:
                        ranks[link.sink] -= 1
            depth += 1
        return depths

    def sorted_by_depth(self):
        depths = self.get_depths()
        return sorted(self, key=depths.get)


# TODO: Add timing information? Or would that be better to do in
#       Conversation?
class LanguageGraphBuilder:

    def __init__(self, knowledge_base, source=None):
        self._knowledge_base = knowledge_base
        self._source = source
        self._nodes = {}
        self._heads = []

    @property
    def knowledge_base(self):
        return self._knowledge_base

    @property
    def source(self):
        return self._source

    @property
    def heads(self):
        return tuple(self._heads)

    @property
    def is_ambiguous(self):
        return len(set(self._nodes.values())) < len(self._nodes)

    @property
    def is_empty(self):
        return not self._nodes

    def add_head(self, head, category):
        if not isinstance(head, semantic_nets.Node):
            raise TypeError(head, semantic_nets.Node)
        self._heads.append((head, category))

    # def add_word_use(self, category, spelling, index = None):
    def add_word_use(self, spelling, word_category, index=None):
        word_use = self.knowledge_base.get_word(word_category,
                                                spelling).new_use()
        word_use.root_node.data[Sentence.NODE_INDEX] = index
        word_use.root_node.data[Sentence.SYNTACTIC_CATEGORY] = \
            word_category
        self._nodes[word_use.root_node] = index
        return word_use.root_node

    def set_tree_category(self, node, tree_category):
        if node not in self._nodes:
            raise KeyError("Invalid node reference.")
        node.data[Sentence.SYNTACTIC_CATEGORY] = tree_category

    def set_index(self, node, index):
        if node not in self._nodes:
            raise KeyError("Invalid node reference.")
        self._nodes[node] = index
        node.data[Sentence.NODE_INDEX] = index

    def build(self):
        while self._heads:
            head, category = self._heads.pop(0)

            root_node = self.knowledge_base.new_sentence_node()
            root_node.data[Sentence.SYNTACTIC_CATEGORY] = category
            if self.source is not None:
                semantic_nets.Link(
                    root_node,
                    Sentence.SOURCE,
                    self.source
                ).connect()
            previous_nodes = ()
            for node in sorted(self._nodes, key=self._nodes.get):
                semantic_nets.Link(
                    root_node,
                    Sentence.CONTAINS,
                    node
                ).connect()
                for previous_node in previous_nodes:
                    semantic_nets.Link(
                        previous_node,
                        Sentence.NEXT,
                        node
                    ).connect()
            semantic_nets.Link(root_node, Sentence.HEAD, head).connect()
            yield Sentence(root_node)

    def clear(self):
        self._heads = []

    def reset(self):
        self._nodes = {}
        self._heads = []
