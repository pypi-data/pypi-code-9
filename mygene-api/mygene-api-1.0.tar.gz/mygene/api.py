""" A basic wrapper of the MyGene API. """

import requests


""" A dictionary of the various endpoints in the MyGene API.
Applications should not have to see or know the values of this
dict since the mygene package abstracts it all.
"""
endpoints = {
        # Metadata API
        'get-metadata': 'mygene.info/v2/metadata',
        # gene API
        'get-gene': 'mygene.info/v2/gene/{gene_id}',
        'post-gene': 'mygene.info/v2/gene',
        # Query API
        'get-query': 'mygene.info/v2/query',
        'post-query': 'mygene.info/v2/query'
    }


class ApiError(Exception):
    pass


def get(endpoint, method='http', params={}):
    """ Performs get requests to the appropriate API.
    :param endpoint: The API endpoint (from endpoints).
    :param method: 'http' or 'https'.
    :param params: Any additional key-value pairs to send
    to the server in the request.
    :returns data: a json dictionary of the data returned
    by the API.
    :raises ValueError:
    """
    method = method.lower()
    if not (method == 'http' or method == 'https'):
        raise ValueError('Method must be either http or https, not {}.'.format(method))
    if type(params) != dict:
        raise ValueError('Params must be a dictionary.')

    endpoint = '{method}://{endpoint}'.format(method=method, endpoint=endpoint)

    r = requests.get(endpoint, params=params)

    if r.status_code == 301:
        raise ApiError('API attempted redirect. Endpoints may be outdated.')
    elif r.status_code == 404:
        raise ApiError('Endpoint not found. Endpoints may be outdated.')
    elif r.status_code == 500:
        raise ApiError('Internal Server Error. Data Could not be retrieved.')
    elif r.status_code != 200:
        raise ApiError('An error has occurred. Data Could not be retrieved. \nError Code: {}'
                .format(r.status_code))

    return r.json()


def post(endpoint, method='http', params={}):
    """ Performs post requests to the appropriate API.
    :param endpoint: The API endpoint (from endpoints).
    :param method: 'http' or 'https'.
    :param params: Any additional key-value pairs to send
    to the server in the request.
    :returns data: a json dictionary of the data returned
    by the API.
    :raises ValueError:
    """
    method = method.lower()
    if not (method == 'http' or method == 'https'):
        raise ValueError('Method must be either http or https, not {}.'.format(method))
    if type(params) != dict:
        raise ValueError('Params must be a dictionary.')

    endpoint = '{method}://{endpoint}'.format(method=method, endpoint=endpoint)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    r = requests.post(endpoint, params=params, headers=headers)

    if r.status_code == 301:
        raise ApiError('API attempted redirect. Endpoints may be outdated.')
    elif r.status_code == 404:
        raise ApiError('Endpoint not found. Endpoints may be outdated.')
    elif r.status_code == 500:
        raise ApiError('Internal Server Error. Data Could not be retrieved.')
    elif r.status_code != 200:
        raise ApiError('An error has occurred. Data Could not be retrieved. \nError Code: {}'
                .format(r.status_code))

    return r.json()


