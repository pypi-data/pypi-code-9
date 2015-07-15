__author__ = 'Derek Payton <derek.payton@gmail.com>'
__copyright__ = 'Copyright (c) Derek Payton'
__description__ = 'Python bindings for Qualpay'
__version__ = '1.0.1'
__license__ = 'MIT License'

merchant_id = None
secret_key = None
base_endpoint = 'https://api.qualpay.com'

from .card import Card
from .error import APIError, GatewayError, HttpError
from .gateway import (PaymentGateway, authorize, verify, capture, sale, void,
    refund, credit, force, tokenize)
