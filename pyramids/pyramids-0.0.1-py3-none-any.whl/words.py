# =========================================================================
# Module:  word.py
# Author:  Aaron Hosford
# Created: 06/27/2011
#
# Copyright (c) Aaron Hosford 2011, all rights reserved.
# =========================================================================
#
# Description:
#   Manages words and word uses.
#
# =========================================================================
#
# Contents:
#
#   class WordManager
#     Manages words and word uses on behalf of a knowledge base.
#
# =========================================================================
#
# Modification History:
#
#   06/27/2011:
#     - Created this module.
#
# =========================================================================
# !/usr/bin/env python

import semantic_nets


class WordUse:

    USE_OF = semantic_nets.reserve_link_type(
        "USE OF WORD",
        __name__
    )

    ROLES = semantic_nets.reserve_node_data_type(
        "SYNTACTIC ROLES",
        __name__
    )

    def __init__(self, root_node):
        self._root_node = root_node

    def __hash__(self):
        return hash(self._root_node)

    def __eq__(self, other):
        if isinstance(other, WordUse):
            return self._root_node == other._root_node
        elif isinstance(other, semantic_nets.Node):
            return self._root_node == other
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, WordUse):
            return self._root_node != other._root_node
        elif isinstance(other, semantic_nets.Node):
            return self._root_node != other
        else:
            return NotImplemented

    @property
    def root_node(self):
        return self._root_node

    @property
    def word_node(self):
        return self.root_node.outgoing.get_unique_node(self.USE_OF)

    @property
    def spelling(self):
        return self.word_node.data[Word.SPELLING]

    @property
    def category(self):
        return self.word_node.data[Word.CATEGORY]

    @property
    def roles(self):
        return self.root_node.data[self.ROLES]

    def __str__(self):
        return (
            self.word_node.data[Word.SPELLING]
            if self.word_node.data[Word.SPELLING]
            else '[omitted ' + self.category + ']'
        )


class Word:

    SPELLING = semantic_nets.reserve_node_data_type(
        "WORD SPELLING",
        __name__
    )

    USE_COUNT = semantic_nets.reserve_node_data_type(
        "WORD USE COUNT",
        __name__
    )

    ASSOCIATIONS = semantic_nets.reserve_node_data_type(
        "WORD ASSOCIATIONS",
        __name__
    )

    CATEGORY = semantic_nets.reserve_node_data_type(
        "SYNTACTIC CATEGORY",
        __name__
    )

    def __init__(self, root_node, knowledge_base):
        self._root_node = root_node
        self._knowledge_base = knowledge_base

    @property
    def root_node(self):
        return self._root_node

    @property
    def knowledge_base(self):
        return self._knowledge_base

    @property
    def spelling(self):
        return self.root_node[self.SPELLING]

    @property
    def use_count(self):
        return self.root_node[self.USE_COUNT]

    @property
    def category(self):
        return self.root_node.data[self.CATEGORY]

    def new_use(self):
        word_use_node = self.knowledge_base.new_word_use_node()
        word_use_node.data[WordUse.ROLES] = [self.category]
        semantic_nets.Link(
            word_use_node,
            WordUse.USE_OF,
            self.root_node
        ).connect()
        self.root_node.data[self.USE_COUNT] += 1
        return WordUse(word_use_node)

    def iter_associations(self):
        return iter(self.root_node[self.ASSOCIATIONS])

    def get_association(self, other):
        return self.root_node[self.ASSOCIATIONS][other]

    def associate(self, other):
        self.root_node[self.ASSOCIATIONS][other] = \
            self.root_node[self.ASSOCIATIONS].get(other, 0) + 1
