def create_authorization_header(token_or_dict):
    """Create a Bearer Authorization header from token.

    Takes either a token_dict as returned by create_web_token or a token
    directly.
    """
    if isinstance(token_or_dict, dict):
        token = token_or_dict['token']
    else:
        token = token_or_dict
    return ('Authorization', 'Bearer {}'.format(token.decode('ascii')))


def extract_token(request_headers_or_authorization_header):
    """Extract the encoded JWT token from the Authorization header.

    Expects that the value of this header starts with "Bearer ".

    Takes a dict containing the key `Authorization` or
    the value of the HTTP `Authorization` header.

    """
    if isinstance(request_headers_or_authorization_header, dict):
        header_value = request_headers_or_authorization_header.get(
            'Authorization')
    else:
        header_value = request_headers_or_authorization_header
    if header_value is None:
        raise ValueError('Missing Authorization header')
    schema, _, encoded_token = header_value.partition(' ')
    if schema.lower() != 'bearer':
        raise ValueError('Authorization scheme is not Bearer')
    return encoded_token.encode('ascii')
