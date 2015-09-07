# coding=utf-8
__copyright__ = 'Copyright 2015, Abalt'


from oscar.apps.dashboard.catalogue.forms import *
from oscar.apps.dashboard.catalogue.forms import ProductForm as BaseProductForm


class ProductForm(BaseProductForm):
    class Meta:
        model = Product
        fields = [
            'title', 'upc', 'description', 'is_discountable', 'vat_type', 'structure']
        widgets = {
            'structure': forms.HiddenInput()
        }