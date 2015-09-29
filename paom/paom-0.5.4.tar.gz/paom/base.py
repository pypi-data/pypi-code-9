class BaseResource(object):

    REQUEST_TYPES = []

    def __init__(self, request):
        self.request = request

    def _get_lookup(self, data):
        lookup = "id"
        if "username" in data:
            lookup = "username"
        elif "slug" in data:
            lookup = "slug"
        return lookup

    def all(self):
        if "ALL" in self.REQUEST_TYPES:
            url = self.ABSOLUTE_URL
            return self.request._call_api(url)
        else:
            raise AttributeError("Attribute not allowed for this resource.")

    def create(self, data):
        if "POST" in self.REQUEST_TYPES:
            url = self.ABSOLUTE_URL
            return self.request._call_api(url, data, method="POST")
        else:
            raise AttributeError("Attribute not allowed for this resource.")

    def update(self, data):
        if "PATCH" in self.REQUEST_TYPES:
            lookup = self._get_lookup(data)
            url = "%s%s" % (self.ABSOLUTE_URL, lookup)
            return self.request._call_api(url, data, method="PATCH")
        else:
            raise AttributeError("Attribute not allowed for this resource.")

    def delete(self, data):
        if "DELETE" in self.REQUEST_TYPES:
            lookup = self._get_lookup(data)
            url = "%s%s" % (self.ABSOLUTE_URL, lookup)
            return self.request._call_api(url, data, method="DELETE")
        else:
            raise AttributeError("Attribute not allowed for this resource.")

    def get(self, lookup):
        """
        param 'lookup' should either be 'slug' or 'id' of the
        object being retrieved.
        """
        if "GET" in self.REQUEST_TYPES:
            url = "%s%s" % (self.ABSOLUTE_URL, lookup)
            return self.request._call_api(url)
        else:
            raise AttributeError("Attribute not allowed for this resource.")
