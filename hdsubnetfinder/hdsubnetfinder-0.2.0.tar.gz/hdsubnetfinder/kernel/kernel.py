# -*- coding: utf-8 -*-


class Kernel:

    def __init__(self, kernel=None, labels=None, index2node=None):
        if labels is None:
            raise ValueError('labels are required.')

        if kernel is None:
            raise ValueError('Kernel is required.')

        self.labels = labels
        self.kernel = kernel
        self.index2node = index2node

    def kernel_multiply_one(self, vector):
        """
            Multiply the specified kernel by the supplied input heat vector.

            Input:
                vector: A hash mapping gene labels to floating point values
                kernel: a single index for a specific kernel

            Returns:
                A hash of diffused heats, indexed by the same names as the
                input vector
        """

        # Have to convert to ordered array format for the input vector
        array = []
        for label in self.labels:
            # Input heats may not actually be in the network.
            # Check and initialize to zero if not
            if label in vector:
                array.append(vector[label])
            else:
                array.append(0)

        # take the dot product
        value = self.kernel * array

        # Convert back to a hash and return diffused heats
        return_vec = {}
        idx = 0
        for label in self.labels:
            return_vec[label] = float(value[idx])
            idx += 1

        return return_vec

    def diffuse(self, vector, reverse=False):
        """
        Diffuse input heats over the set of kernels, add to this object

        Input:
            {
                'gene1': float(heat1)
                'gene2' : float(heat2)
                ...
            }

        Returns:
            Diffused heat vector
        """

        return self.kernel_multiply_one(vector)
