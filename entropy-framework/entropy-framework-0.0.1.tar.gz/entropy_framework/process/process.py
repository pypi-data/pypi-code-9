class Process(object):
    def __init__(self, registry):
        """
        Setting registry
        """
        self.registry = registry

    def __call__(self, *args, **kwargs):
        """
        Calling _process method
        """
        return self._process(*args, **kwargs)

    def _process(self, *args, **kwargs):
        """
        Custom method, witch should be writen
        manually in client code
        """
        pass
