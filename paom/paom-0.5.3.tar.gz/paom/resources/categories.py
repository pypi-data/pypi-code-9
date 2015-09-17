from paom.base import BaseResource


class Categories(BaseResource):

    def products(self, slug):
        url = "%s%s" % ("/category/", slug)
        return  self.request._call_api(url)
