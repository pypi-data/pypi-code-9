import os
from six import iteritems

from whaleapi import api


def initialize(api_token=None, api_host=None, **kwargs):
    api.api_token = api_token if api_token is not None else os.environ.get('WHALE_API_TOKEN')
    api.api_host = api_host if api_host is not None else os.environ.get('WHALE_HOST',
                                                                        'https://app.whale.io')

    # HTTP client and API options
    for key, value in iteritems(kwargs):
        setattr(api, key, value)
