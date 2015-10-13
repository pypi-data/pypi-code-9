#!/usr/bin/env python
# Example usage of treelib
#
# Author: chenxm
#
__author__ = 'chenxm'

from treelib import Tree, Node

def create_family_tree():
    ## Create the family tree
    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")
    return tree

def example(desp):
    sep = "-"*20 + '\n'
    print(sep + desp)

if __name__ == '__main__':
    tree = create_family_tree()

    example("Tree of the whole family:")
    tree.show(key=lambda x: x.tag, reverse=True, line_type='ascii-em')

    example("All family members in DEPTH mode:")
    print(','.join([tree[node].tag for node in tree.expand_tree()]))
