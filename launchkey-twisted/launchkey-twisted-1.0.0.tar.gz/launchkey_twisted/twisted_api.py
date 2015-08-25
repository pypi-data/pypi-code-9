import json, six

from six.moves.urllib.parse import urlencode

from twisted.internet.protocol import Protocol
from twisted.web.http_headers import Headers
from twisted.internet import defer
import launchkey


class TwistedAPI(launchkey.API):
    def __init__(self, agent, app_key, app_secret, private_key, version="v1", api_host="https://api.launchkey.com",
                 test=False):
        """

        :param agent: Twisted web client agent
        :type agent: twisted.web.client.Agent
        :param app_key:
        :param app_secret:
        :param private_key:
        :param version:
        :param api_host:
        :param test:
        """
        self._agent = agent
        super(TwistedAPI, self).__init__(app_key, app_secret, private_key, version, api_host, test)

    def get_user_hash(self):
        super(TwistedAPI, self).get_user_hash()

    def ping(self, force=False):
        """
        Used to retrieve the API's public key and server time
        The key is used to encrypt data being sent to the API and the server time is used
        to ensure the data being sent is recent and relevant.
        Instead of doing a ping each time to the server, it keeps the key and server_time
        stored and does a comparison from the local time to appropriately adjust the value
        :param success_callback: Callable to be called when the ping request succeeds
        :param error_callback: Callable to be called when the ping request fails
        :param force: Boolean. True will override the cached variables and ping LaunchKey
        :rtype: twisted.internet.defer.Deferred
        """
        import datetime
        if force or self.api_pub_key is None or self.ping_time is None:
            def cache_response(response):
                self.api_pub_key = response['key']
                self.ping_time = datetime.datetime.strptime(response['launchkey_time'], "%Y-%m-%d %H:%M:%S")
                self.ping_difference = datetime.datetime.now()
                return response

            d = self._send_request(None, 'GET', 'ping')
            d.addCallback(cache_response)
        else:
            self.ping_time = datetime.datetime.now() - self.ping_difference + self.ping_time
            d = defer.succeed({"launchkey_time": str(self.ping_time)[:-7], "key": self.api_pub_key})

        return d

    def authorize(self, username, session=True, user_push_id=False):
        def process_response(response):
            if 'auth_request' not in response:
                return defer.fail(RequestError(0, 'Invalid Response - No auth_request value in response'))

            return response['auth_request']

        d = self._prepare_data({'username': username, 'session': session, 'user_push_id': user_push_id})
        d.addCallback(self._send_request, 'POST', 'auths')
        d.addCallback(process_response)
        return d

    def poll_request(self, auth_request):
        def handle_request_error(failure, failed_auth_request):
            failure.trap(RequestError)
            if 70403 == failure.value.code:
                return defer.fail(PendingResponse(failed_auth_request))

            return failure

        d = self._prepare_data({'auth_request': auth_request})
        d.addCallback(self._send_request, 'GET', 'poll')
        d.addErrback(handle_request_error, auth_request)
        return d

    def create_whitelabel_user(self, identifier):
        def process_response(response):
            cipher = launchkey.decrypt_RSA(self.private_key, response['response']['cipher'])
            data = launchkey.decrypt_AES(cipher[:-16], response['response']['data'], cipher[-16:])
            return json.loads(data)

        d = self._prepare_data({'identifier': identifier})
        d.addCallback(self._send_request, 'POST', 'users', False)
        d.addCallback(process_response)
        return d

    def _notify(self, action, status, auth_request):
        def process_response(response, status):
            result = status if "message" in response and response['message'] == "Successfully updated" else False
            return defer.succeed(result)

        d = self._prepare_data(
            {'auth_request': auth_request, 'action': action, 'status': status, 'auth_request': auth_request}
        )
        d.addCallback(self._send_request, 'PUT', 'logs')
        d.addCallback(process_response, status)
        return d

    def _prepare_data(self, data={}, signature=True):
        """
        Encrypts secret with RSA key and signs
        :param signature: Bool representing if a signature should be added to the response
        :return: Dict with RSA encrypted secret_key and signature of that value
        """

        def _post_ping(result, my_data, signature):
            to_encrypt = {"secret": self.app_secret, "stamped": str(result['launchkey_time'])}
            encrypted_secret = launchkey.encrypt_RSA(result['key'], str(to_encrypt))
            my_data['secret_key'] = encrypted_secret
            if signature:
                signature = launchkey.sign_data(self.private_key, encrypted_secret)
                my_data['signature'] = signature
                my_data['app_key'] = self.app_key

            return my_data

        d = self.ping()
        d.addCallback(_post_ping, data, signature)
        return d

    def _send_request(self, data, method, endpoint, form_data=True):
        uri = self.API_HOST + endpoint
        headers = {
            'User-Agent': ['LaunchKey Twisted Client'],
            'Accept-Type': ['application/json']
        }

        if data is None:
            bodyProducer = NoneBodyProducer()
        elif 'GET' == method:
            uri = '%s?%s' % (uri, urlencode(data, doseq=True))
            bodyProducer = NoneBodyProducer()
        elif form_data:
            headers['Content-Type'] = ['application/x-www-form-urlencoded']
            bodyProducer = JSONToURLEncodedFormDataBodyProducer(data)
        else:
            headers['Content-Type'] = ['application/json']
            bodyProducer = JSONBodyProducer(data)

        deferred_request = self._agent.request(
            six.b(method),
            six.b(uri),
            Headers(headers),
            bodyProducer
        )

        def _process_response(response):
            content_type = response.headers.getRawHeaders('content-type')
            if content_type is None or not content_type.pop().startswith('application/json'):
                return defer.fail(Exception('Non JSON response from API received'))
            d = defer.Deferred()
            response.deliverBody(JSONResponseBodyParser(d))
            return d

        def _check_for_error(response):
            status_code = int(response.get('status_code', 0))
            if status_code >= 300:
                return defer.fail(RequestError(
                    response.get('message_code', response.get('status_code')),
                    response.get('message', 'Unknown request error')
                ))
            else:
                return response

        deferred_request.addCallback(_process_response)
        deferred_request.addCallback(_check_for_error)
        return deferred_request


class PendingResponse(BaseException):
    def __init__(self, auth_request, *args, **kwargs):
        self.auth_request = auth_request
        super(PendingResponse, self).__init__(*args, **kwargs)


class RequestError(BaseException):
    def __init__(self, code, message, *args, **kwargs):
        self.code = code
        self.message = message
        super(RequestError, self).__init__(*args, **kwargs)

    def __str__(self):
        return '[%s] %s' % (self.code, self.message)


from zope.interface import implementer
from twisted.web.iweb import IBodyProducer
from twisted.internet.defer import succeed


@implementer(IBodyProducer)
class JSONBodyProducer(object):
    length = 0

    def __init__(self, o):
        self.body = json.dumps(o)
        self.length = len(self.body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


@implementer(IBodyProducer)
class JSONToURLEncodedFormDataBodyProducer(object):
    def __init__(self, o):
        self.body = urlencode(o, doseq=True)
        self.length = len(self.body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


@implementer(IBodyProducer)
class NoneBodyProducer(object):
    def __init__(self):
        self.length = 0

    def startProducing(self, consumer):
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class JSONResponseBodyParser(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.data = ''

    def dataReceived(self, bytes):
        self.data += bytes

    def connectionLost(self, reason):
        o = json.loads(self.data)
        self.finished.callback(o)
