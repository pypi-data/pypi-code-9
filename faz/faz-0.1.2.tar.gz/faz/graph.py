# -*- coding: utf-8 -*-
from __future__ import print_function


import networkx as nx


class CircularDependencyException(Exception):
    pass


class DependencyGraph(object):

    def __init__(self, tasks):
        super(DependencyGraph, self).__init__()
        self.tasks = tasks
        self._graph = nx.MultiDiGraph()
        self._build_graph()

    def _build_graph(self):
        """ Produce a dependency graph based on a list
            of tasks produced by the parser.
        """
        self._graph.add_nodes_from(self.tasks)
        for node1 in self._graph.nodes():
            for node2 in self._graph.nodes():
                for input_file in node1.inputs:
                    for output_file in node2.outputs:
                        if output_file == input_file:
                            self._graph.add_edge(node2, node1)
        cycles = [cycle for cycle in nx.simple_cycles(self._graph)]
        if len(cycles) > 0:
            print("Found a circular dependency for tasks:")
            for cycle in cycles:
                for task in cycle:
                    print("{}".format(task))
                print()
            raise CircularDependencyException("Circular dependency found.")
        for order, task in enumerate(nx.topological_sort(self._graph)):
            task.predecessors = self._graph.predecessors(task)
            task.order = order

    def show_tasks(self):
        for task in nx.topological_sort(self._graph):
            print("Task {0}  ******************************".format(task.order))
            print("Predecessors: {0}".format(task.predecessors))
            print("options: {0}".format(task.options))
            print("Interpreter: {0}".format(task.interpreter))
            print("Environment: {0}".format(task.environment))
            print("Inputs: {0}".format(task.inputs))
            print("Outputs: {0}".format(task.outputs))
            print("Code:")
            for line in task.code:
                print("{0}".format(line))
        print("**************************************")

    def execute(self):
        """
        Execute tasks in the graph (already in order).
        """
        for task in self.tasks:
            print(80 * "*")
            task()
            print(80 * "*")
