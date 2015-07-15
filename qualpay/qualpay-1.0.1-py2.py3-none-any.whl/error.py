
GATEWAY_ERROR_CODES = {
    '000': 'Success',
    '100': 'Bad request',
    '101': 'Invalid credentials',
    '102': 'Invalid pg_id',
    '103': 'Missing cardholder data',
    '104': 'Invalid transaction amount',
    '105': 'Missing auth_code',
    '106': 'Invalid AVS data',
    '107': 'Invalid expiration date',
    '108': 'Invalid card number',
    '109': 'Field length validation failed',
    '110': 'Dynamic DBA not allowed',
    '111': 'Credits not allowed',
    '401': 'Void failed',
    '402': 'Refund failed',
    '403': 'Capture failed',
    '404': 'Batch close failed',
    '405': 'Tokenization failed',
    '998': 'Timeout',
    '999': 'Internal error',
}

HTTP_ERROR_CODES = {
    '200': 'OK',
    '400': 'Bad Request',
    '401': 'Unauthorized',
    '402': 'Declined',
    '409': 'Conflict',
    '500': 'Internal Server Error',
    '504': 'Timeout',
}


class APIError(Exception):
    """
    Base exception from which all other Qualpay exceptions inherit.
    """
    pass


class GatewayError(APIError):
    """
    Raised when the payment gateway returns a non-success code.
    """
    def __init__(self, code, response):
        self.code = code
        self.response = response
        message = GATEWAY_ERROR_CODES.get(str(code), 'Unknown Error')
        super(GatewayError, self).__init__(message)


class HttpError(APIError):
    """
    Raised when the payment gateway returns a non-200 response.
    """
    def __init__(self, code, response):
        self.code = code
        self.response = response
        message = HTTP_ERROR_CODES.get(str(code), 'Unknown Error')
        super(HttpError, self).__init__(message)
