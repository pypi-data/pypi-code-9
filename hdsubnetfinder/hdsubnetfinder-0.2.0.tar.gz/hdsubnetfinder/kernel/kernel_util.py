# -*- coding: utf-8 -*-


def write_kernel(target_kernel, output_file):
    """
    Serialize the kernel to the supplied output file
    """
    index2node = target_kernel.index2node

    if index2node is None:
        raise ValueError('Cannot serialize Kernel created from pre-computed file.')

    kernel = target_kernel.kernel
    labels = target_kernel.labels

    output_stream = open(output_file, 'w')

    cx = kernel.tocoo()
    edges = {}
    for i, j, v in zip(cx.row, cx.col, cx.data):
        a = index2node[i]
        b = index2node[j]
        edges[(a, b)] = str(v)

    # iterate through rows
    # sort labels in alphabetical order

    output_stream.write("Key\t" + "\t".join(sorted(labels)) + "\n")

    for nodeA in sorted(labels):
        printstr = nodeA
        # through columns
        for nodeB in sorted(labels):
            if (nodeA, nodeB) in edges:
                printstr += "\t" + edges[(nodeA, nodeB)]
            else:
                printstr += "\t0"

        output_stream.write(printstr + "\n")

    output_stream.close()
