# -*- coding: utf-8 -*-
import cStringIO


def __validate(target_kernel):
    index2node = target_kernel.index2node

    if index2node is None:
        raise ValueError('Cannot serialize Kernel created from pre-computed file.')

    kernel = target_kernel.kernel
    labels = target_kernel.labels

    return kernel, labels, index2node


def __write(kernel, labels, index2node, output_stream):

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


def get_kernel_as_string(target_kernel):
    """
    Return a kernel as a big string object.
    """
    output_stream = cStringIO.StringIO()
    kernel, labels, index2node = __validate(target_kernel)
    __write(kernel, labels, index2node, output_stream)
    kernel_as_big_string = output_stream.getvalue()
    output_stream.close()

    return kernel_as_big_string


def write_kernel(target_kernel, output_file):
    """
    Serialize the kernel to the supplied output file
    """
    kernel, labels, index2node = __validate(target_kernel)
    output_stream = open(output_file, 'w')
    __write(kernel, labels, index2node, output_stream)
    output_stream.close()
