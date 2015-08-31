def extract_relevant(formula, facts_only=False):
    """Determine the relevant part of the formula, that is, all nodes that are part of the ground
        program of a query or an evidence node.

    :param formula: formula
    :param facts_only: extract only facts
    :return: set of relevant node identifiers
    """
    current_nodes = set(abs(x) for _, x, _ in formula.evidence_all() if formula.is_probabilistic(x))
    current_nodes |= set(abs(x) for _, x in formula.queries() if formula.is_probabilistic(x))

    relevant = set()
    next_nodes = set()
    while current_nodes:
        index = current_nodes.pop()
        node = formula.get_node(index)
        nodetype = type(node).__name__
        if nodetype != 'atom':
            children = set(abs(c) for c in node.children)
            next_nodes |= (children - relevant)
            if not facts_only:
                relevant.add(index)
        else:
            relevant.add(index)
        current_nodes = next_nodes
    return relevant


def break_alternative(source, target, **kwargs):
    """

    :param source:
    :type source: LogicFormula
    :param target:
    :type target: LogicDAG
    :param kwargs:
    :return:
    """
    translation = {}

    def lookup(x):
        v = translation.get(abs(x))
        if v is None or x > 0:
            return v
        elif x < 0:
            return -v

    # Step 1: determine relevant facts
    relevant_nodes = extract_relevant(source)

    # Step 2: copy relevant facts to destination
    for index in relevant_nodes:
        node = source.get_node(index)
        if type(node).__name__ == 'atom':
            new_index = target.add_atom(*node)
            translation[index] = new_index

    # Step 3: do a forward pass, adding nodes that are fully defined
    #  The non-cyclic parts of the formula should only depend on earlier defined atoms.
    for index in relevant_nodes:
        node = source.get_node(index)
        ntype = type(node).__name__
        if index not in translation:
            # We know that node is not an atom.
            # Find the translated children
            children = [lookup(c) for c in node.children]
            if None not in children:
                # All children are known, so add the node to target.
                if ntype == 'conj':
                    new_index = target.add_and(children, name=node.name)
                else:
                    new_index = target.add_or(children, name=node.name)
                translation[index] = new_index
    cyclic_nodes = relevant_nodes - set(translation.keys())

    # Extract cyclic and non-cyclic parts
    cyclic_discard = set()
    cyclic_struct = {}
    # Step 4:
    for index in reversed(sorted(cyclic_nodes)):
        # if index not in cyclic_discard:       # TODO can only discard if only 1 parent
            node = source.get_node(index)
            ntype = type(node).__name__
            if ntype == 'conj':
                content, discard = expand_conj(source, index, cyclic_nodes)
                # extract the cyclic and non-cyclic content
                nc_nodes = []
                c_nodes = []
                for c in content:
                    if abs(c) in cyclic_nodes:
                        c_nodes.append(c)
                    else:
                        nc_nodes.append(c)
                # add the non-cyclic part and replace it
                if nc_nodes:
                    nc_part = target.add_and(nc_nodes)
                else:
                    nc_part = target.TRUE
                cyclic_struct[index] = ('conj', nc_part, c_nodes)
                cyclic_discard |= discard
            elif ntype == 'disj':
                content = set(map(abs, node.children))
                nc_nodes = []
                c_nodes = []
                for c in content:
                    if abs(c) in cyclic_nodes:
                        c_nodes.append(c)
                    else:
                        nc_nodes.append(c)
                if nc_nodes:
                    nc_part = target.add_or(nc_nodes)
                else:
                    nc_part = target.FALSE
                cyclic_struct[index] = ('disj', nc_part, c_nodes)

    # Extract nodes of interest:
    #  each cycle has to pass through a node that is larger than its parent
    nodes_of_interest = []
    for p in cyclic_struct:
        for c in cyclic_struct[p][2]:
            if c > p:
                nodes_of_interest.append((c, p))


    # # Other stuff below
    # # Step 4: add atoms for cyclic nodes
    # for index in cyclic_nodes:
    #     new_index = target.add_atom(('c', index), True, None, source.get_node(index).name)
    #     translation[index] = new_index
    #
    # counts = defaultdict(int)
    #
    # # Step 5: replace atoms by actual content
    # for index in cyclic_nodes:
    #     node = source.get_node(index)
    #     ntype = type(node).__name__
    #     children = [lookup(c) for c in node.children]
    #     new_index = lookup(index)
    #     if new_index not in counts:
    #         counts[new_index] = 0
    #
    #     if ntype == 'conj':
    #         target._update(new_index, target._create_conj(children, node.name))
    #     else:
    #         target._update(new_index, target._create_disj(children, node.name))
    #     for c in children:
    #         counts[abs(c)] += 1

    cyclic_struct_map = {}
    for index in sorted(cyclic_struct):
        ctype, nc, children = cyclic_struct[index]
        if ctype == 'disj':
            cyclic_struct_map[index] = index
        else:
            assert len(children) == 1
            cyclic_struct_map[index] = cyclic_struct_map[children[0]]

    cyclic_struct_redux = {}
    for index, content in cyclic_struct.items():
        ctype, nc, children = content
        if ctype == 'disj':
            new_children = [cyclic_struct_map[c] for c in children]
            cyclic_struct_redux[index] = ctype, nc, new_children

    # print (counts)
    # target is now a compact version of the original formula (no cycles were removed)
    return target, cyclic_struct, nodes_of_interest, cyclic_struct_redux


def find_cycles(adj, index, anc=(), maxl=None):
    if anc and index == anc[0]:
        yield anc
    elif index in anc:
        return
    elif maxl is not None and len(anc) == maxl:
        return
    else:
        for n in adj[index][2]:
            if not anc and n < index:
                continue
            elif anc and n < anc[0]:
                continue
            else:
                for cyc in find_cycles(adj, n, anc + (index,), maxl):
                    yield cyc


def expand_conj(formula, index, scope):
    discard = set()
    content = set()
    child1 = None
    node = formula.get_node(index)
    ntype = type(node).__name__
    while ntype == 'conj' and index in scope and node.name is None:
        discard.add(index)
        child0, child1 = node.children
        content.add(child0)
        index = abs(child1)
        node = formula.get_node(index)
        ntype = type(node).__name__
    if child1 is not None:
        content.add(child1)
    return content, discard
