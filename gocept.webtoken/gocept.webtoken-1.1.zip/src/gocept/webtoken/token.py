from .interfaces import ICryptographicKeys
import datetime
import jwt
import zope.component


def create_web_token(
        key_name, issuer, subject, expires_in, data, algorithm='RS256'):
    """Create a signed web token.

    key_name ... name of the cryptographic key (should end in '-private')
    issuer ... string
    subject ... string
    expires_in ... number of seconds the token expires in or None for no expiry
    data ... dict of payload
    algorithm ... the encryption algorithm (default: RS256)

    Returns a dict containing token and the content of the token, so one can
    access the tokens content for debugging without the need to decode the
    token itself.
    """
    keys = zope.component.getUtility(ICryptographicKeys)
    now = datetime.datetime.utcnow()
    args = {'iss': issuer,
            'sub': subject,
            'iat': now,
            'nbf': now,
            'data': data}
    if expires_in is not None:
        args['exp'] = now + datetime.timedelta(seconds=expires_in)
    return {'token': jwt.encode(args, keys[key_name], algorithm=algorithm),
            'data': args}


def decode_web_token(token, key_name, subject, algorithms=['RS256']):
    """Decode a signed web token.

    token ... encoded token string
    key_name ... name of the cryptographic key (should end in '-public')
    subject ... require this subject ('sub') to be set in the token
    algorithm ... list of possible encryption algorithms (default: RS256)

    Raises ValueError on an invalid token.
    Returns decoded token.

    """
    keys = zope.component.getUtility(ICryptographicKeys)
    try:
        token_content = jwt.decode(
            token, keys[key_name], algorithms=algorithms)
    except Exception as e:
        raise ValueError(e)
    if token_content.get('sub') != subject:
        raise ValueError("Subject mismatch '%s' != '%s'" % (
            subject, token_content.get('sub')))
    return token_content
