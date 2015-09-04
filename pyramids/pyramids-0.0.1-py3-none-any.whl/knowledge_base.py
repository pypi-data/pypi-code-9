# =========================================================================
# Module:  knowledge_bases.py
# Author:  Aaron Hosford
# Created: 06/27/2011
#
# Copyright (c) Aaron Hosford 2011, all rights reserved.
# =========================================================================
#
# Description:
#   Provides knowledge reflection & storage functionality for 
#   semantics2.py.
#
# =========================================================================
#
# Contents:
#
#   class KnowledgeBase
#     Reflects (and stores) the structures used by the various component
#     classes of semantics2.py as subgraphs of a semantic net. Can be 
#     thought of as a blackboard of sorts.
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
import words


class KnowledgeBase:
    
    WORD = semantic_nets.reserve_link_type("WORD NODE", __name__)
    WORD_USE = semantic_nets.reserve_link_type("WORD USE NODE", __name__)
    SENTENCE = semantic_nets.reserve_link_type("SENTENCE NODE", __name__)

    PERSON = semantic_nets.reserve_link_type("PERSON NODE", __name__)

    def __init__(self, net=None, root_node=None):
        self._net = net if net else semantic_nets.Net()
        self._root_node = root_node if root_node else self._net.add_node()
        self._word_nodes = {}

    @property
    def net(self):
        return self._net

    @property
    def root_node(self):
        return self._root_node

    def _new_node(self, node_type):
        node = self.net.add_node()
        semantic_nets.Link(self.root_node, node_type, node).connect()
        return node

    def new_word_use_node(self):
        return self._new_node(self.WORD_USE)

    def new_sentence_node(self):
        return self._new_node(self.SENTENCE)

    def get_word(self, category, spelling):
        if not isinstance(spelling, str) and spelling is not None:
            raise TypeError(
                "Expected string value or None for word spelling. (" + 
                repr(spelling) + ")"
            )
        
        if (category, spelling) not in self._word_nodes:
            word_node = self._new_node(self.WORD)
            
            # What is the spelling of the word?
            word_node.data[words.Word.SPELLING] = spelling
            
            # How many uses of the word have been created?
            word_node.data[words.Word.USE_COUNT] = 0
            
            # What other words are associated with this one through use, 
            # and how often are they used together?
            word_node.data[words.Word.ASSOCIATIONS] = {}
            
            # The syntactic category of the word.
            word_node.data[words.Word.CATEGORY] = category
            
            self._word_nodes[category, spelling] = word_node
            
        return words.Word(self._word_nodes[category, spelling], self)

    def new_person_node(self):
        person_node = self._new_node(self.PERSON)
        # TODO: Right now this is a hack to get things up & going.
        #       There needs to be a kind node for people, and this should 
        #       be an instance of it.
        return person_node
