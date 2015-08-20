import arrow
import hashlib
import random
import json
from urllib.request import Request, urlopen
from sparweltbitool.logger import Logger
from etl_generic.etl import GenericException
import urllib
from base64 import b64encode


class ClientEmarsys(object):
    """
    Emarsys REST API wrapper.
    """

    def __init__(self,
                 username,
                 secret_token,
                 base_uri=u"https://www1.emarsys.net/api/v2/",
                 tzinfo_obj=None):
        """
        Initialises the Emarsys API wrapper object.
        """
        self._username = username
        self._secret_token = secret_token
        self._base_uri = base_uri
        self._tzinfo_obj = tzinfo_obj

    def __unicode__(self):
        return u"Emarsys({base_uri})".format(base_uri=self._base_uri)

    def __repr__(self):
        return unicode(self).encode("utf8")

    def call(self, uri, method, params=None):
        """
        Send the API call request to the Emarsys server.
        uri: API method URI
        method: HTTP method
        params: parameters to construct payload when API calls are made with
                POST or PUT HTTP methods.
        """
        uri = self._base_uri + uri
        if params:
            params = json.dumps(params).encode("utf-8")

        req = Request(uri, params)

        header_value = self._authentication_header_value()
        logger = Logger()
        logger.info(header_value)

        req.add_header("X-WSSE", header_value)
        req.add_header("Content-Type", "application/json")

        timeout = 600

        try:
            response = json.loads(urlopen(req, timeout=timeout).read().decode("utf-8"))

        except urllib.error.HTTPError as ex:
            message = "urllib.error.HTTPError on fetching for data from remote endpoint: '{}'. Code: {}, Reason: '{}'.".format(uri, ex.code, ex.reason)
            raise GenericException(message)
        except urllib.error.URLError as ex:
            message = "urllib.error.URLError on fetching for data from remote endpoint: '{}'. Reason: '{}'.".format(uri, ex.reason)
            raise GenericException(message)
        except UnicodeEncodeError as ex:
            raise GenericException(ex)
        except ValueError as ex:
            raise GenericException(ex)

        if response['replyText'] != 'OK' and response['replyCode'] != 0 and "data" in response:
            message='HTTP {reply_text}: {reply_code} [{uri}]'.format(
                reply_text=response['replyText'],
                reply_code=response['replyCode'],
                uri=uri,
            ),

            raise GenericException(message)

        return response["data"]

    def _authentication_header_value(self):
        created = arrow.utcnow().to('local').format('YYYY-MM-DDTHH:mm:ssZZ')
        nonce = hashlib.md5(str(random.getrandbits(128)).encode("utf-8")).hexdigest()
        password = "".join((nonce, created, self._secret_token))
        password_encoded_and_hashed = hashlib.sha1(password.encode("utf-8")).hexdigest()
        password_digest = b64encode(password_encoded_and_hashed.encode("utf-8")).decode("ascii")

        return ('UsernameToken Username="{username}", '
                'PasswordDigest="{password_digest}", Nonce="{nonce}", '
                'Created="{created}"').format(username=self._username,
                                              password_digest=password_digest,
                                              nonce=nonce,
                                              created=created)
