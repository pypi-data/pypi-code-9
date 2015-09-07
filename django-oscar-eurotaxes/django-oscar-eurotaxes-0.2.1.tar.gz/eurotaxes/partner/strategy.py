from oscar.apps.partner import strategy

from eurotaxes.partner.models import VATCountry


class Selector(object):
    """
    Custom selector to return a UK-specific strategy that charges VAT
    """

    def strategy(self, request=None, user=None, **kwargs):
        return Default(request=request, user=user)


class VATCountryStrategy(strategy.FixedRateTax):
    """
    Price policy to charge VAT on the base price
    """
    def __init__(self, request=None, user=None):
        super(VATCountryStrategy, self).__init__(request=request)
        if not self.user:
            self.user = user

    def get_country_using_request(self, request):
        """
        TODO
        """
        return None

    def get_country_using_user(self, user):
        """
        TODO
        """
        return None

    def get_rate(self, product, stockrecord):
        country = self.get_country_using_user(self.user)
        if not country:
            country = self.get_country_using_request(self.request)
        if not country:
            return VATCountry.objects.get_for_product(product).get_vat
        return VATCountry.objects.get_for_product_and_country(product, country).get_vat


class Default(strategy.UseFirstStockRecord, VATCountryStrategy,
              strategy.StockRequired, strategy.Structured):

    pass
