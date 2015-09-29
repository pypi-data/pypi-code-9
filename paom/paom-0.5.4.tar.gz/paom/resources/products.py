from paom.base import BaseResource


class Products(BaseResource):

    ABSOLUTE_URL = "/products/"
    REQUEST_TYPES = ["GET", "POST", "ALL", "PATCH", "DELETE"]

    def collections(self, slug):
        url = "%s%s" % ("/collections-in-product/", slug)
        return  self.request._call_api(url)


class Collections(BaseResource):

    ABSOLUTE_URL = "/collections/"
    REQUEST_TYPES = ["GET", "POST", "ALL", "PATCH", "DELETE"]

    def products(self, slug):
        url = "%s%s" % ("/products-in-collection/", slug)
        return  self.request._call_api(url)

    def remove_product(self, data):
        """
        This method will remove a product from a collection. 'data' parameter
        should contain:
            'product': serialized product
            'paom_collection': serialized collection
        """
        url = "/product-collections-delete/"
        return  self.request._call_api(url, data=data,  method="DELETE")


class Designs(BaseResource):

    ABSOLUTE_URL = "/designs/"
    REQUEST_TYPES = ["GET", "POST", "ALL", "PATCH", "DELETE"]


class Categories(BaseResource):

    def products(self, slug):
        url = "%s%s" % ("/category/", slug)
        return  self.request._call_api(url)
