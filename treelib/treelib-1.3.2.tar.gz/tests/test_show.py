#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from treelib import Tree, Node

tree = Tree()
tree.create_node("Harry", "harry")
tree.create_node("Jane", "jane", parent="harry")
tree.create_node("Bill", "bill", parent="harry")
tree.create_node("Diane", "diane", parent="jane")
tree.create_node("George", "george", parent="bill")

print(tree)
tree.show()
tree.save2file("test_tree.txt")