import time
import urlparse
import hmac
import string
import random
from hashlib import sha1

from swiftclient import client

def get_temp_key(connection):
    """ Tries to get meta-temp-url key from account.
    If not set, generate tempurl and save it to acocunt.
    This requires at least account owner rights. """

    try:
        account = connection.get_account()
    except client.ClientException:
        return None

    key = account[0].get('x-account-meta-temp-url-key')

    if not key:
        chars = string.ascii_lowercase + string.digits
        key = ''.join(random.choice(chars) for x in range(32))
        headers = {'x-account-meta-temp-url-key': key}
        try:
            client.post_account(storage_url, auth_token, headers)
        except client.ClientException:
            return None
    return key


def get_temp_url(connection, filename, container, expires=600):
    key = get_temp_key(connection)
    if not key:
        return None

    expires += int(time.time())
    url_parts = urlparse.urlparse(connection.url)
    path = "%s/%s/%s" % (url_parts.path, container, filename)
    base = "%s://%s" % (url_parts.scheme, url_parts.netloc)
    hmac_body = 'GET\n%s\n%s' % (expires, path)
    sig = hmac.new(key, hmac_body.encode("utf-8"), sha1).hexdigest()
    url = '%s%s?temp_url_sig=%s&temp_url_expires=%s' % (
        base, path, sig, expires)
    return url
