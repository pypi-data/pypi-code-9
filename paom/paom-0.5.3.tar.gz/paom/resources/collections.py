from paom.base import BaseResource


class Collections(BaseResource):

    ABSOLUTE_URL = "/collections/"

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
