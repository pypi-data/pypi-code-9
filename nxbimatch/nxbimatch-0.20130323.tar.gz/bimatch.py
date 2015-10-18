"""
Bipartite Matching
"""

import networkx as nx


LICENSE = """
Copyright (c) 2012,2013, MATSUI Tetsushi <VED03370@nifty.ne.jp>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# bipartite graph (red + black, edges)
def bipartite_graph(red, black, edges):
    """
    Return a nx.Graph object
    """
    graph = nx.Graph()
    graph.add_nodes_from(red, bipartite=0)
    graph.add_nodes_from(black, bipartite=1)
    graph.add_edges_from(edges)
    return graph


# a maximum match
def maximum_match(bgraph):
    """
    Return a maximum match of given bipartite graph.

    Hopcroft-Karp algorithm.
    """
    matching_graph = nx.Graph()

    augmenting_paths = maximal_shortest_augmenting_paths(bgraph, matching_graph)
    while augmenting_paths:
        matching = align_part(bgraph, matching_graph.edges())
        augment_graph(bgraph, matching_graph, augmenting_paths)
        augmenting_paths = maximal_shortest_augmenting_paths(bgraph, matching_graph)
    return matching_graph.edges()


def maximal_shortest_augmenting_paths(bgraph, matching_graph):
    """
    Return a maximal set of vertex-disjoint shortest augmenting paths.

    Returned as a list of lists each of which contains tuples
    representing directed edges.
    """
    red = set(n for n, d in bgraph.nodes(data=True) if d['bipartite'] == 0)
    black = set(bgraph) - red
    free_red = red.difference(matching_graph)
    free_black = black.difference(matching_graph)
    if not free_red or not free_black:
        return []
    layers = construct_layered_dag(bgraph, matching_graph, free_red, free_black)

    # DFS on the dag to get augmenting paths
    paths = []
    while layers.out_edges("source"):
        path = []
        node = layers.out_edges("source")[0][1]
        next_node = None
        while layers.out_edges(node):
            next_node = layers.out_edges(node)[0][1]
            layers.remove_node(node)
            if next_node == "sink":
                break
            path.append((node, next_node))
            node = next_node
        if next_node != "sink":
            # no next node was found, i.e. no more path
            layers.remove_node(node)
            continue
        else:
            paths.append(path)
    return paths


def construct_layered_dag(bgraph, matching_graph, free_red, free_black):
    """
    Construct layered DAG to search augmenting paths in bgraph with
    respect to the matching (here, it is given as matching_graph).
    free_red (free_black resp.) is the free vertices with respect to
    the matching in red side vertices (black side resp.).
    """
    i, j = 0, 1
    layers = {0: free_red}
    layered_arcs = {}
    nodes = list(free_red)
    arcs = []
    while layers[i]:
        layers[j] = set()
        layered_arcs[i] = set()
        for vertex in layers[i]:
            for neighbor in bgraph.neighbors_iter(vertex):
                if neighbor not in nodes:
                    arc = (neighbor, vertex)
                    has_edge = matching_graph.has_edge(neighbor, vertex)
                    if j & 1 and not has_edge or i & 1 and has_edge:
                        layers[j].add(neighbor)
                        layered_arcs[i].add(arc)
        if j & 1 and layers[j].intersection(free_black):
            filtered = set(a for a in layered_arcs[i] if a[0] in free_black)
            layered_arcs[i] = filtered
            arcs.extend(layered_arcs[i])
            break
        else:
            nodes.extend(layers[j])
            arcs.extend(layered_arcs[i])
            i += 1
            j += 1

    layered_dag = nx.DiGraph()
    layered_dag.add_edges_from(arcs)
    layered_dag.add_edges_from((node, "sink") for node in layers[0])
    layered_dag.add_edges_from(("source", node) for node in layers[j])
    return layered_dag


def augment_graph(bgraph, matching_graph, augmenting_paths):
    """
    Update matching graph with given set of augmenting paths.
    """
    if len(augmenting_paths[0]) == 1:
        matching_graph.add_edges_from(path[0] for path in augmenting_paths)
    else:
        for path in augmenting_paths:
            matching_graph.remove_edges_from(path[1::2])
            matching_graph.add_edges_from(align_part(bgraph, path[0::2]))


def augment_single(matching, augmenting_path):
    """
    Update matching with given augmenting path.
    """
    if len(augmenting_path) == 1:
        matching.add(augmenting_path[0])
    else:
        if augmenting_path[0] in matching:
            matching.difference_update(augmenting_path[0::2])
            matching.update((v, u) for (u, v) in augmenting_path[1::2])
        else:
            matching.difference_update(augmenting_path[1::2])
            matching.update((v, u) for (u, v) in augmenting_path[0::2])


# generate maximum matching
def generate_maximum_matchings(bgraph):
    """
    Generate all maximum matchings of given bipartite graph.
    """
    initial = maximum_match(bgraph)
    initial = align_part(bgraph, initial)
    yield initial

    digraph = create_directed_bipartite(bgraph, initial)

    for matching in sub_generate_maximum_matching(digraph, initial):
        matching = align_part(digraph, matching)
        yield matching


def sub_generate_maximum_matching(digraph, matching):
    """
    Generate matchings for given directed bipartite graph & matching.
    """
    if digraph.size() != 0:
        cycle = find_a_cycle(digraph)
        if cycle:
            arc = matching_arc_in_cycle(cycle, matching)

            exchanged = matching.copy()
            augment_single(exchanged, cycle)
            yield exchanged

            # gminus (do not use arc)
            reverse_cycle(digraph, cycle)
            delete_edge(digraph, arc)
            for sub in sub_generate_maximum_matching(digraph, exchanged):
                yield sub

            # gplus (use arc)
            cycle.remove(arc) # name is "cycle" but content becomes a path
            reverse_cycle(digraph, [(v, u) for (u, v) in cycle]) # re-reverse
            removed_edges = digraph.edges(arc)
            delete_adjacent_edges(digraph, arc)
            for sub in sub_generate_maximum_matching(digraph, matching):
                yield sub
            # add back removed_edges
            digraph.add_edges_from(removed_edges)
            digraph.add_edge(*arc)

        else:
            for sub in path_generate_maximum_matching(digraph, matching):
                yield sub


def path_generate_maximum_matching(dbgraph, matching):
    """
    Generate maximum matching using acyclic bipartite dbgraph,
    by exchanging feasible paths.
    """
    # feasible path is a length two path starting from free vertex,
    # i.e. the first edge is not in matching.
    path = find_a_feasible_path(dbgraph, matching)
    if path:
        # arc is not in matching
        arc, match_arc = path
        assert match_arc in matching

        exchanged = matching.copy()
        augment_single(exchanged, path)
        assert all(i < j for i, j in exchanged)
        yield exchanged

        # gminus (arc does not remain in graph)
        delete_edge(dbgraph, arc)
        for sub in path_generate_maximum_matching(dbgraph, matching):
            yield sub
        dbgraph.add_edge(*arc)

        # gplus (arc remains in graph)
        removed_edges = dbgraph.edges(arc)
        delete_adjacent_edges(dbgraph, arc)
        for sub in path_generate_maximum_matching(dbgraph, exchanged):
            yield sub

        dbgraph.add_edges_from(removed_edges)
        assert dbgraph.has_edge(*arc)


def delete_adjacent_edges(graph, edge):
    """
    Delete specified edge and its adjacent edges from graph.

    The edge set is denoted as E^{+}(G) in Uno's paper.
    """
    graph.remove_edges_from(graph.edges(edge))


def delete_edge(graph, edge):
    """
    Delete specified edge from graph.

    The edge set is denoted as E^{-}(G) in Uno's paper.
    """
    if graph.has_edge(*edge):
        graph.remove_edge(*edge)
    else:
        graph.remove_edge(edge[1], edge[0])


def reverse_edge(digraph, edge):
    """
    Reverse the direction of given edge in the digraph.
    """
    digraph.remove_edge(*edge)
    digraph.add_edge(*edge[::-1])


def align_part(bgraph, matching):
    """
    Align edges in matching so that first vertex of each matching edge
    is with attribute bipartite=0.
    """
    aligned = set()
    for edge in matching:
        if bgraph.node[edge[0]]["bipartite"] == 0:
            aligned.add(edge)
        else:
            aligned.add(edge[::-1])
    return aligned


# generate perfect matching
def generate_perfect_matchings(bgraph):
    """
    Generate all perfect matchings of given bipartite graph.
    """
    assert len([v for (v, d) in bgraph.nodes(data=True) if d["bipartite"] == 0]) == len([v for (v, d) in bgraph.nodes(data=True) if d["bipartite"] != 0])

    initial = set(maximum_match(bgraph))

    if len(initial) != len(bgraph) // 2:
        raise StopIteration("there is no perfect matching")

    initial = align_part(bgraph, initial)
    yield initial

    digraph = create_directed_bipartite(bgraph, initial)

    for matching in sub_generate_perfect_matchings(digraph, initial):
        matching = align_part(bgraph, matching)
        yield matching

def sub_generate_perfect_matchings(digraph, matching):
    """
    Generate matchings for given directed bipartite graph & matching.
    """
    if digraph.size():
        cycle = find_a_cycle(digraph)
        if cycle:
            arc = matching_arc_in_cycle(cycle, matching)

            exchanged = matching.copy()
            augment_single(exchanged, cycle)
            yield exchanged

            # gminus (do not use arc)
            reverse_cycle(digraph, cycle)
            delete_edge(digraph, arc)
            for sub in sub_generate_perfect_matchings(digraph, exchanged):
                yield sub

            # gplus (use arc)
            cycle.remove(arc) # name is "cycle" but content becomes a path
            reverse_cycle(digraph, [(v, u) for (u, v) in cycle]) # re-reverse
            removed_edges = digraph.edges(arc)
            delete_adjacent_edges(digraph, arc)
            for sub in sub_generate_perfect_matchings(digraph, matching):
                yield sub
            # add back removed_edges
            digraph.add_edges_from(removed_edges)
            digraph.add_edge(*arc)


# digraph functions
def create_directed_bipartite(bgraph, matching):
    """
    Create a digraph with the same vertices with bgraph.
    The edges in matching are directed forward, otherwise backward.
    """
    aligned_match = align_part(bgraph, matching)
    directed = nx.DiGraph()
    directed.add_nodes_from((v for (v, d) in bgraph.nodes(data=True) if d["bipartite"] == 0), bipartite=0)
    directed.add_nodes_from((v for (v, d) in bgraph.nodes(data=True) if d["bipartite"] == 1), bipartite=1)
    for edge in align_part(bgraph, bgraph.edges()):
        if edge in aligned_match:
            directed.add_edge(*edge)
        else:
            directed.add_edge(*edge[::-1])
    return directed


def cycle_edges(nodes):
    """
    Convert a cycle as node list to a cycle as edge list.
    """
    if nodes[0] != nodes[-1]:
        nodes = nodes + [nodes[0]]
    size = len(nodes)
    return [tuple(nodes[i:i + 2]) for i in range(size - 1)]


def reverse_cycle(digraph, cycle):
    """
    Reverse the direction of arcs in cycle.

    cycle is a sequence of arcs.
    """
    assert digraph.has_edge(*cycle[0])
    digraph.remove_edges_from(cycle)
    digraph.add_edges_from([(v, u) for (u, v) in cycle])


def find_a_feasible_path(digraph, matching):
    """
    Return a length 2 feasible path.
    """
    free_vertices = set(digraph)
    for edge in matching:
        free_vertices.difference_update(edge)
    while free_vertices:
        hop0 = free_vertices.pop()
        for hop1 in digraph.neighbors(hop0):
            if hop1 in free_vertices:
                continue
            for hop2 in digraph.neighbors(hop1):
                return [(hop0, hop1), (hop1, hop2)]


def find_a_cycle(digraph):
    """
    Find a cycle in given digraph.

    If there is no cycle in the digraph, return None.
    """
    # DFS
    to_check = set(digraph)
    while to_check:
        cycle_nodes = [to_check.pop()]
        while cycle_nodes:
            for arc in digraph.out_edges_iter(cycle_nodes[-1:]):
                if arc[1] in to_check:
                    to_check.remove(arc[1])
                    cycle_nodes.append(arc[1])
                    break
                elif arc[1] in cycle_nodes:
                    del cycle_nodes[:cycle_nodes.index(arc[1])]
                    return cycle_edges(cycle_nodes)
            else:
                cycle_nodes.pop()


def matching_arc_in_cycle(cycle, matching):
    """
    Return an arc in cycle, which is also in matching.
    """
    return cycle[0] if cycle[0] in matching else cycle[1]


# maybe unnecessary
create_directed = create_directed_bipartite

def trim_unnecessary(dgraph):
    """
    Return a list of strongly connected components (unnecessary
    arcs are trimmed from digraph).
    """
    return [c for c in nx.strongly_connected_component_subgraphs(dgraph) if c.size()]

def cycle_containing_arc(dgraph, arc):
    """
    Return a cycle (as node list) in dgraph containing the arc
    """
    root = arc[0]
    vertex = arc[1]
    cycle = list(arc)
    cycle.extend(nx.shortest_path(dgraph, vertex, root)[1:-1])
    return cycle

def augment(matching, augmenting_paths):
    """
    Update matching with given set of augmenting paths.
    """
    if len(augmenting_paths[0]) == 1:
        matching.update(path[0] for path in augmenting_paths)
    else:
        for path in augmenting_paths:
            matching.difference_update(path[1::2])
            matching.update((v, u) for (u, v) in path[0::2])
