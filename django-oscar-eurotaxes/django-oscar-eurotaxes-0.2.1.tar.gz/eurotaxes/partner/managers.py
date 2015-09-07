# coding=utf-8
__copyright__ = 'Copyright 2015, Abalt'

from django.db.models import Manager


class VATCountryManager(Manager):
    def get_default(self):
        return self.get(default=True)

    def get_for_country(self, country):
        return self.get(country=country, vat_type__default=True)

    def get_for_product(self, product):
        return self.get_for_product_and_country(product, self.get_default().country)

    def get_for_product_and_country(self, product, country):
        return self.get(country=country, vat_type=product.vat_type)
