class BaseResource(object):

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
        url = self.ABSOLUTE_URL
        return self.request._call_api(url)

    def create(self, data):
        url = self.ABSOLUTE_URL
        return self.request._call_api(url, data, method="POST")

    def update(self, data):
        lookup = self._get_lookup(data)
        url = "%s%s" % (self.ABSOLUTE_URL, lookup)
        return self.request._call_api(url, data, method="PATCH")

    def delete(self, data):
        lookup = self._get_lookup(data)
        url = "%s%s" % (self.ABSOLUTE_URL, lookup)
        return self.request._call_api(url, data, method="DELETE")

    def get(self, lookup):
        """
        param 'lookup' should either be 'slug' or 'id' of the
        object being retrieved.
        """
        url = "%s%s" % (self.ABSOLUTE_URL, lookup)
        return self.request._call_api(url)
