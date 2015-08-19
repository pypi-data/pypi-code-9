class BaseResource(object):

    def __init__(self, request):
        self.request = request

    def all(self):
        url = self.ABSOLUTE_URL
        return self.request._call_api(url)

    def create(self, data):
        url = self.ABSOLUTE_URL
        return self.request._call_api(url, data, method="POST")

    def update(self, data):
        url = "%s%s" % (self.ABSOLUTE_URL, data["slug"])
        return self.request._call_api(url, data, method="PATCH")

    def delete(self, data):
        url = "%s%s" % (self.ABSOLUTE_URL, data["slug"])
        return self.request._call_api(url, data, method="DELETE")

    def get(self, lookup):
        """
        param 'lookup' should either be 'slug' or 'id' of the
        object being retrieved.
        """
        url = "%s%s" % (self.ABSOLUTE_URL, lookup)
        return self.request._call_api(url)
