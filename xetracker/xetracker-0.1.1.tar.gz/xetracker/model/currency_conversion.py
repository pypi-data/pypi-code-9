
class CurrencyConversion:
  def __init__(self, provider, currency_from, currency_to, provider_selling_rate, provider_buying_rate, conversion_time):
    self.provider = provider
    self.currency_from = currency_from
    self.currency_to = currency_to
    self.provider_selling_rate = provider_selling_rate
    self.provider_buying_rate = provider_buying_rate
    self.conversion_time = conversion_time

  def __str__(self):
    return ('CurrencyConversion[provider={}, currency_from={}, currency_to={}, provider_selling_rate={}, provider_buying_rate={}, conversion_time={}]'.format(
            self.provider,
            self.currency_from,
            self.currency_to,
            self.provider_selling_rate,
            self.provider_buying_rate,
            self.conversion_time)
        )

  def __eq__(self, other):
    return (
            self.provider == other.provider
        and self.currency_from == other.currency_from
        and self.currency_to == other.currency_to
        and self.provider_selling_rate == other.provider_selling_rate
        and self.provider_buying_rate == other.provider_buying_rate
        and self.conversion_time == other.conversion_time
        )
