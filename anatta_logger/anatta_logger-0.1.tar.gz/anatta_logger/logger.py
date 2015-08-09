class AnattaLogger(object):
    """
    Output data into anatta format
    """

    def __init__(self, conf):
        """
        Args
            conf Hash
                root String: where is project root directory
                    - will publish logs into <root>/logs/
        """
        self.root = conf['root']
        pass

    def log(self, measurements):
        """
        Log one datapoint
        """
        pass
