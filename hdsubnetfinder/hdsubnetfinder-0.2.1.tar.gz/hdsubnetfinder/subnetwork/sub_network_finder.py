import hdsubnetfinder.subnetwork.network_util as util


class SubNetworkFinder():
    """
    This service gets an annotated node network
    typically derived from an uploaded TSV
    and uses a reference network to find a
    relevant subnetwork.  The annotations are
    applied to the subnetwork and it is returned
    as CX network as the result of the job
    """

    def __init__(self, kernel, network):
        """
        Sub network finder is always associated with a network and pre-computed kernel.

        :param kernel:
        :param network: Network as triples
        :return:
        """
        if kernel is None:
            raise ValueError('Kernel is required.')
        if network is None:
            raise ValueError('Network is required.')

        self.__kernel = kernel
        self.__network = network

    def get_sub_network(self, identifiers):
        query_vector = util.query_vector(identifiers, self.__kernel.labels)
        diffused = self.__kernel.diffuse(query_vector)
        filtered = util.filter_sif(self.__network, diffused)

        # Return result in CX format.
        return util.sif2cx(filtered, scores=diffused)
