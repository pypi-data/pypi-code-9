import functools
from .requestor import APIRequestor

__all__ = ('PaymentGateway', 'authorize', 'verify', 'capture', 'sale', 'void',
    'refund', 'credit', 'force', 'tokenize')


class PaymentGateway(object):
    def __init__(self, merchant_id=None, security_key=None, base_endpoint=None):
        import qualpay
        self.merchant_id = merchant_id or qualpay.merchant_id
        self.security_key = security_key or qualpay.security_key
        self.base_endpoint = base_endpoint or qualpay.base_endpoint

    def get_requestor(self):
        requestor = APIRequestor(
            merchant_id=self.merchant_id,
            security_key=self.security_key,
            base_endpoint=self.base_endpoint
        )
        return requestor

    def request(self, endpoint, **data):
        requestor = self.get_requestor()
        response = requestor.request(endpoint, data)
        return response

    def authorize(self, **kwargs):
        """
        An authorization message is used to send cardholder data to the issuing bank for
        approval. An approved transaction will continue to be open until it expires or a
        capture message is received. Authorizations are automatically voided if they are not
        captured within 28 days, although most issuing banks will release the hold after 24
        hours in retail environments or 7 days in card not present environments.
        """
        response = self.request('pg/auth', **kwargs)
        return response

    def verify(self, **kwargs):
        """
        A verify message is used to send cardholder data to the issuing bank for validation. A
        verify message will return success if the cardholder information was verified by the
        issuer. If the AVS or CVV2 field is included in the message, then the AVS or CVV2
        result code will be returned in the response message.
        """
        response = self.request('pg/verify', **kwargs)
        return response

    def capture(self, pg_id, **kwargs):
        """
        A capture message is used to capture a previously authorized transaction using the
        payment gateway identifier returned by the authorization message. A capture may
        be completed for any amount up to the authorized amount.
        """
        response = self.request('pg/capture/{0}'.format(pg_id), **kwargs)
        return response

    def sale(self, **kwargs):
        """
        A sale message is used to perform the function of an authorization and a capture in a
        single message. This message is used in retail and card not present environments
        where no physical goods are being shipped.
        """
        response = self.request('pg/sale', **kwargs)
        return response

    def void(self, pg_id, **kwargs):
        """
        A void message is used to void a previously authorized transaction. Authorizations
        can be voided at any time. Captured transactions can be voided until the batch is
        closed. The batch close time is configurable and by default is 11 PM Eastern Time.
        """
        response = self.request('pg/void/{0}'.format(pg_id), **kwargs)
        return response

    def refund(self, pg_id, **kwargs):
        """
        A refund message is used to issue a partial or full refund of a previously captured
        transaction using the payment gateway identifier. Multiple refunds are allowed per
        captured transaction provided that the sum of all refunds does not exceed the
        original captured transaction amount.

        Authorizations that have not been captured are not eligible for refund.
        """
        response = self.request('pg/refund/{0}'.format(pg_id), **kwargs)
        return response

    def credit(self, **kwargs):
        """
        A credit message is used to issue a non-referenced credit to a cardholder. A nonreferenced
        credit requires the cardholder data be provided in the message. The
        credit message is enabled during the first 30 days of production activity.

        After 30 days, the credit message is disabled to prevent fraudulent use of the
        message. If a credit is necessary after 30 days, it is recommended that the merchant
        make use of the Qualpay web based business platform to issue the credit. If the
        merchant requires non-referenced credits to be enabled on the payment gateway
        beyond 30 days they can request this by contacting Qualpay.
        """
        response = self.request('pg/credit', **kwargs)
        return response

    def force(self, **kwargs):
        """
        A force message is used to force a declined transaction into the system. This would
        occur when the online authorization was declined and the merchant received an
        authorization from a voice or automated response (ARU) system. The required fields
        are the same as a sale or authorization message with the following exceptions: the
        cardholder expiration date (exp_date) is not required, and the 6-character
        authorization code received from the issuer (auth_code) is required.
        """
        response = self.request('pg/force', **kwargs)
        return response

    def tokenize(self, **kwargs):
        """
        A tokenization message is used to securely store cardholder data on the Qualpay
        system. Once stored, a unique card identifier is returned for use in future
        transactions. Optionally, tokenization can be requested in an authorization,
        verification or sale message by sending the tokenize field set to "true".
        """
        response = self.request('pg/tokenize', **kwargs)
        return response


def gateway_method(method):
    @functools.wraps(getattr(PaymentGateway, method))
    def wrapper(**kwargs):
        gateway = PaymentGateway()
        return getattr(gateway, method)(*args, **kwargs)
    return wrapper

authorize = gateway_method('authorize')
verify = gateway_method('verify')
capture = gateway_method('capture')
sale = gateway_method('sale')
void = gateway_method('void')
refund = gateway_method('refund')
credit = gateway_method('credit')
force = gateway_method('force')
tokenize = gateway_method('tokenize')
