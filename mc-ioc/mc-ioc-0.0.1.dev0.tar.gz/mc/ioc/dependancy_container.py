from mc.ioc.singleton import Singleton

import logging
import logging.config

logger = logging.getLogger(__name__)

# FIXME: seperate service injection from initiation so container wait
# till all dependancies are fullfiled

@Singleton
class DependencyContainer:
    """
    A Singleton container to implement IoC pattern and maintain
    Features initiation with thier deps
    Limitations: needs dependancies to be inserted in order

    """
    def __init__(self, allow_replace=False):
        self.services = {}
        self.allow_replace = allow_replace

    def inject(self, feature, service, *args, **kwargs):
        """
        Inject new service into container
        TODO: user kwargs to match with service param names so order don't matter
        """
        logger.info("Injecting %s with deps: %s", feature, args)
        if not self.allow_replace:
            assert not self.services.has_key(feature), "Duplicate service: %r" % feature
        if callable(service):
            deps = []
            for dep in args:
                assert self.services.has_key(dep), "Unfulfilled dependancy: %r" % dep
                deps.append(self.services[dep]())
            instance = service(*deps, **kwargs)
            def call(): return instance
        else:
            def call(): return service

        self.services[feature] = call

    def get_service(self, feature):
        assert self.services.has_key(feature), "Unknown service %r" % dep
        return self.services[dep]()

    def __getitem__(self, feature):
        try:
            service = self.services[feature]
        except KeyError:
            raise KeyError, "Unknown feature named %r" % feature
        return service()
