import shelve


class CacheSettings(object):
    enabled = True
    """
    Turns cache on and off

    :type: bool
    """

    storage = shelve.open('.okapi_cache.pickle')
    """
    Storage for saving cache.

    :type: dict
    """

    def get(self):
        return self.storage if self.enabled else {}
