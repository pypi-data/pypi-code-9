# Based on Michael Angeletti's MIT Licensed pycard
# https://github.com/orokusaki/pycard

import calendar
import datetime
import re

from .gateway import PaymentGateway

__all__ = ('Card',)

non_digit_regexp = re.compile(r'\D')


class Card(object):
    """
    A credit card that may be valid or invalid.
    """

    # A mapping from common credit card brands to their number regexps
    BRAND_VISA = 'visa'
    BRAND_MASTERCARD = 'mastercard'
    BRAND_AMEX = 'amex'
    BRAND_DISCOVER = 'discover'
    BRAND_UNKNOWN = u'unknown'

    BRANDS = {
        BRAND_VISA: re.compile(r'^4\d{12}(\d{3})?$'),
        BRAND_MASTERCARD: re.compile(r'^(5[1-5]\d{4}|677189)\d{10}$'),
        BRAND_AMEX: re.compile(r'^3[47]\d{13}$'),
        BRAND_DISCOVER: re.compile(r'^(6011|65\d{2})\d{12}$'),
    }

    def __init__(self, number, exp_month, exp_year, cvv2):
        """
        Attaches the provided card data and holder to the card after removing
        non-digits from the provided number.
        """
        self.number = non_digit_regexp.sub('', number)
        self.exp_date = ExpDate(exp_month, exp_year)
        self.cvv2 = cvv2

    def __repr__(self):
        """
        Returns a typical repr with a simple representation of the masked card
        number and the exp date.
        """
        return u'<Card brand={b} number={n}, exp_date={e}>'.format(
            b=self.brand,
            n=self.mask,
            e=self.exp_date.mmyyyy
        )

    @property
    def mask(self):
        """
        Returns the credit card number with each of the number's digits but the
        first six and the last four digits replaced by an X, formatted the way
        they appear on their respective brands' cards.
        """
        # If the card is invalid, return an "invalid" message
        if not self.is_luhn_valid:
            return u'invalid'

        # If the card is an Amex, it will have special formatting
        if self.brand == self.BRAND_AMEX:
            return u'XXXX-XXXXXX-X{0}'.format(self.number[11:15])

        # All other cards
        return u'XXXX-XXXX-XXXX-{0}'.format(self.number[12:16])

    @property
    def brand(self):
        """
        Returns the brand of the card, if applicable, else an "unknown" brand.
        """
        # Check if the card is of known type
        for brand, regexp in self.BRANDS.items():
            if regexp.match(self.number):
                return brand

        # Default to unknown brand
        return self.BRAND_UNKNOWN

    @property
    def is_expired(self):
        """
        Returns whether or not the card is expired.
        """
        return self.exp_date.is_expired

    @property
    def is_valid(self):
        """
        Returns whether or not the card is a valid card for making payments.
        """
        return not self.is_expired and self.is_luhn_valid

    @property
    def is_luhn_valid(self):
        """
        Returns whether or not the card's number validates against the luhn
        algorithm, automatically returning False on an empty value.
        """
        # Check for empty string
        if not self.number:
            return False

        r = [int(ch) for ch in str(self.number)][::-1]
        s = (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2]))
        return s % 10 == 0

    def authorize(self, amt_tran, **kwargs):
        assert self.is_valid  # CONSIDER: What should this raise?
        gateway = PaymentGateway()
        return gateway.authorize(
            card_number=self.number,
            exp_date=self.exp_date.mmyy,
            amt_tran=amt_tran,
            **kwargs
        )

    def verify(self, **kwargs):
        assert self.is_valid  # CONSIDER: What should this raise?
        gateway = PaymentGateway()
        return gateway.verify(
            card_number=self.number,
            exp_date=self.exp_date.mmyy,
            cvv2=self.cvv2,
            **kwargs
        )

    def sale(self, amt_tran, **kwargs):
        assert self.is_valid  # CONSIDER: What should this raise?
        gateway = PaymentGateway()
        return gateway.sale(
            card_number=self.number,
            exp_date=self.exp_date.mmyy,
            cvv2=self.cvv2,
            amt_tran=amt_tran,
            **kwargs
        )

    def tokenize(self, **kwargs):
        assert self.is_valid  # CONSIDER: What should this raise?
        gateway = PaymentGateway()
        return gateway.tokenize(
            card_number=self.number,
            exp_date=self.exp_date.mmyy,
            cvv2=self.cvv2,
            **kwargs
        )


class ExpDate(object):
    """
    An expiration date of a credit card.
    """
    def __init__(self, month, year):
        """
        Attaches the last possible datetime for the given month and year, as
        well as the raw month and year values.
        """
        # Attach month and year
        self.month = month
        self.year = year

        # Get the month's day count
        weekday, day_count = calendar.monthrange(year, month)

        # Attach the last possible datetime for the provided month and year
        self.expired_after = datetime.datetime(
            year,
            month,
            day_count,
            23,
            59,
            59,
            999999
        )

    def __repr__(self):
        """
        Returns a typical repr with a simple representation of the exp date.
        """
        return u'<ExpDate expired_after={d}>'.format(
            d=self.expired_after.strftime('%m/%Y')
        )

    @property
    def is_expired(self):
        """
        Returns whether or not the expiration date has passed in American Samoa
        (the last timezone).
        """
        # Get the current datetime in UTC
        utcnow = datetime.datetime.utcnow()

        # Get the datetime minus 11 hours (Samoa is UTC-11)
        samoa_now = utcnow - datetime.timedelta(hours=11)

        # Return whether the exipred after time has passed in American Samoa
        return samoa_now > self.expired_after

    @property
    def mmyyyy(self):
        """
        Returns the expiration date in MM/YYYY format.
        """
        return self.expired_after.strftime('%m/%Y')

    @property
    def mmyy(self):
        """
        Returns the expiration date in MMYY format.
        """
        return self.expired_after.strftime('%m%y')

    @property
    def mm(self):
        """
        Returns the expiration date in MM format.
        """
        return self.expired_after.strftime('%m')

    @property
    def yyyy(self):
        """
        Returns the expiration date in YYYY format.
        """
        return self.expired_after.strftime('%Y')
