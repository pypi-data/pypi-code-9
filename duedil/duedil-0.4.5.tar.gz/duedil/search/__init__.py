

class SearchResource(object):
    attribute_names = None
    locale = 'uk'
    rid = None
    path = None

    def __init__(self, client, rid=None, locale='uk', **kwargs):
        if not self.attribute_names:
            raise NotImplementedError(
                "Resources must include a list of allowed attributes")

        self.rid = rid
        assert(locale in ['uk', 'roi'])
        self.locale = locale
        self.client = client

        if kwargs:
            self._set_attributes(**kwargs)

    def _set_attributes(self, missing=False, **kwargs):
        for k, v in kwargs.items():
            if k in self.attribute_names:
                self.__setattr__(k, v)

        if missing is True:
            for allowed in self.attribute_names:
                if allowed not in kwargs:
                    self.__setattr__(allowed, None)

    def load(self):
        result = self.client.get(self.endpoint)
        self._set_attributes(**result)

    def __getattr__(self, name):
        """
        lazily return attributes, only contact duedil if necessary
        """
        try:
            return super(SearchResource, self).__getattribute__(name)
        except AttributeError:
            if name in self.attribute_names:
                self.load()
                return super(SearchResource, self).__getattribute__(name)
            else:
                raise
