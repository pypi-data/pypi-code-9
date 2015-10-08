

class BasePersistenceStrategy(object):
    """
    A persistence strategy is responsible for persisting a given event
    somewhere (i.e. directly to Shushuo, a local cache, a Redis queue, etc.)
    """

    def persist(self, event):
        """Persists the given event somewhere.

        :param event: the event to persist
        """
        raise NotImplementedError()


class DirectPersistenceStrategy(BasePersistenceStrategy):
    """
    A persistence strategy that saves directly to Shushuo and bypasses any local
    cache.
    """

    def __init__(self, api):
        """ Initializer for DirectPersistenceStrategy.

        :param api: the Shushuo Api object used to communicate with the Shushuo API
        """
        super(DirectPersistenceStrategy, self).__init__()
        self.api = api

    def persist(self, event):
        """ Posts the given event directly to the Shushuo API.

        :param event: an Event to persist
        """
        self.api.post_event(event)

    def batch_persist(self, events):
        """ Posts the given events directly to the Shushuo API.

        :param events: a batch of events to persist
        """
        self.api.post_events(events)


class RedisPersistenceStrategy(BasePersistenceStrategy):
    """
    A persistence strategy that persists events to Redis for later processing.

    Not yet implemented.
    """
    pass


class FilePersistenceStrategy(BasePersistenceStrategy):
    """
    A persistence strategy that persists events to the local file system for
    later processing.

    Not yet implemented.
    """
    pass
