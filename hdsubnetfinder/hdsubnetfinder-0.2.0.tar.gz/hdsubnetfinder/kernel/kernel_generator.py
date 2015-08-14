from array import array
import time
import urllib2
import logging
import csv
import numpy as np

from scipy.sparse import coo_matrix, csc_matrix
from scipy.sparse.linalg import expm

from kernel import Kernel

logging.basicConfig(level=logging.DEBUG)


class KernelGenerator:

    def create_kernel_from_file(self, pre_computed_kernel_url):
        """
        Input:
            pre_computed_kernel_file - filename of tab delemited kernel file,
                                        as made by KernelGenerator
        """
        ker = []
        start = True
        labels = list()

        for line in csv.reader(urllib2.urlopen(pre_computed_kernel_url), delimiter='\t'):
            if start:
                labels = line[1:]
                start = False
            else:
                ker.append([float(x) for x in line[1:]])

        kernel = csc_matrix(np.asarray(ker))
        return Kernel(kernel=kernel, labels=labels, index2node=None)

    def create_kernel(self, network_url, time_t=0.1):
        start = time.clock()

        edges, nodes, node_out_degrees = self.__parse_net(network_url)

        num_nodes = len(nodes)
        node_order = list(nodes)

        index2node = {}
        node2index = {}

        logging.debug('Network source: ' + str(network_url))
        logging.debug('# of Nodes: ' + str(num_nodes))
        logging.debug('# of Edges: ' + str(len(edges)))

        for i in range(0, num_nodes):
            index2node[i] = node_order[i]
            node2index[node_order[i]] = i

        # construct the diagonals
        # SCIPY uses row and column indexes to build the matrix
        # row and columns are just indexes: the data column stores 
        # the actual entries of the matrix
        row = array('i')
        col = array('i')
        data = array('f')

        # build the diagonals, including the out-degree 
        for i in range(0, num_nodes):
            # diag entries: out degree
            degree = 0
            if index2node[i] in node_out_degrees:
                degree = node_out_degrees[index2node[i]]
                # append to the end
            # array object: first argument is the index, the second is the data value
            # append the out-degree to the data array
            data.insert(len(data), degree)
            # build the diagonals
            row.insert(len(row), i)
            col.insert(len(col), i)

            # add off-diagonal edges
        for i in range(0, num_nodes):
            for j in range(0, num_nodes):
                if i == j:
                    continue
                if (index2node[i], index2node[j]) not in edges:
                    continue
                # append index to i-th row, j-th column
                row.insert(len(row), i)
                col.insert(len(col), j)
                # -1 for laplacian: i.e. the negative of the adjacency matrix 
                data.insert(len(data), -1)

        # Build the graph laplacian: the CSC matrix provides a sparse matrix format
        # that can be exponentiated efficiently
        l = coo_matrix((data, (row, col)), shape=(num_nodes, num_nodes)).tocsc()

        end = time.clock()
        logging.debug('Data preparation done in ' + str(end - start) + ' sec.')

        # this is the matrix exponentiation calculation.
        # Uses the Pade approximiation for accurate approximation.
        # Computationally expensive.
        # O(n^2), n= # of features, in memory as well. 
        start = time.clock()
        kernel = expm(-time_t * l)
        end = time.clock()

        logging.debug('expm done in ' + str(end - start) + ' sec.')

        return Kernel(kernel=kernel, labels=node_order, index2node=index2node)

    def __parse_net(self, network_url):
        """
        Parse .sif network, using just the first and third columns
        to build an undirected graph. Store the node out-degrees
        in an index while we're at it. 
        """
        edges = set()
        nodes = set()
        degrees = {}

        for line in urllib2.urlopen(network_url):
            parts = line.rstrip().split()
            source = parts[0]
            target = parts[2]

            # if inputting a multi-graph, skip this
            if (source, target) in edges:
                continue

            # Remove self-loop
            if source == target:
                continue

            edges.add((source, target))
            edges.add((target, source))

            nodes.add(source)
            nodes.add(target)

            if source not in degrees:
                degrees[source] = 0
            if target not in degrees:
                degrees[target] = 0

            degrees[source] += 1
            degrees[target] += 1

        return edges, nodes, degrees
