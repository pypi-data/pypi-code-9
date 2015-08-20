from paom.base import BaseResource


class Products(BaseResource):

    ABSOLUTE_URL = "/products/"

    def collections(self, slug):
        url = "%s%s" % ("/collections-in-product/", slug)
        return  self.request._call_api(url)
