#!/bin/python2

from sys import argv
from astparser import AstParser
from graphviz import Digraph

def handle_node(node, graph, parent=None):
	name = str(id(node.name))
	graph.node(name, node.name)
	if parent:
		graph.edge(parent, name)
	for child in node.children:
		handle_node(child, graph, parent=name)

def visualize(content, target):
		parser = AstParser()
		ast = parser.parse(content, rule_name='node')
		graph = Digraph(comment=argv[1])
		handle_node(ast, graph)
		graph.render(target, view=False)

def main():
    if len(argv) > 1:
        target = "output.gv"
        if len(argv) > 2:
            target = argv[2]

        with open(argv[1], "r") as f:
            content = f.read()
            visualize(content, target)

    else:
        print "No input file specified."
