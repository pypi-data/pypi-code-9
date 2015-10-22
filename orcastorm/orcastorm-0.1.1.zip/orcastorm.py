"""Asyncronous client for SAASPASS and Tornado."""
import sys
import time
import json
from contextlib import contextmanager
from urllib.parse import urlencode
import tornado
import tornado.httpclient
import tornado.concurrent
import tornado.ioloop

if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    raise Exception("OrcaStorm requires at least Python version 3.5.")
if tornado.version < "4.3":
    raise Exception("OrcaStorm requires at least tornado version 3.5.")

__version__ = "0.1.1"


class BusTimeoutError(Exception):
    """Raised when the waiter has been waiting for too long."""
    pass


class AsyncBus(object):
    """Asynchronous notification bus.

    This is a helper class that is used for asynchronous notifications between http requests. You can await for
    notifications on a set of keys, and you can send notifications for waiters of a given key. This is similar to
    a Condition object, with the following differences:

     * AsyncBus.waitfor does have a timeout parameter (Condition does not)
     * AsyncBus can automatically route notifications to multiple waiters using message identifiers (keys).

    """

    def __init__(self):
        self._waiters = {}

    def notify(self, key, message):
        """Notify a single waiter.

        :param key: Key value that identifies the waiter. Should be immutable.
        :param message: The message to be delivered to the waiter.
        :return: True if the waiter was notified, False otherwise.
        """
        if key in self._waiters and self._waiters[key]:
            waiter = next(iter(self._waiters[key]))
            waiter.set_result((key, message))
            return True
        return False

    def notifyall(self, key, message):
        """Notify all waiters. Return the number of waiters notified.

        :param key: Key value that identifies the waiters. Should be immutable.
        :param message: The message to be delivered to the waiters.
        :return: The number of waiters notified
        :type: int
        """
        result = 0
        if key in self._waiters and self._waiters[key]:
            for waiter in iter(self._waiters[key]):
                waiter.set_result((key, message))
                result += 1
        return result

    @contextmanager
    def _listen(self, keys, waiter):
        # Add waiters to the dict of waiters
        for key in keys:
            if key in self._waiters:
                self._waiters[key].append(waiter)
            else:
                self._waiters[key] = [waiter]
        try:
            # Execute code
            yield
        finally:
            # Remove waiters from the dict of waiters
            for key in keys:
                if key in self._waiters:
                    self._waiters[key].remove(waiter)
                    if not self._waiters[key]:
                        del self._waiters[key]

    async def waitforkeys(self, keys, timeout=None):
        """Wait for notification.

        :param keys: An iterable that contains keys to be listened to. Keys should be immutable.
        :param timeout: If there is no notification coming in for the given timeout, then raise a BusTimeoutError.
        :return: A tuple of (key, message) that was sent by a notify() or notifyall() call.
        """
        waiter = tornado.concurrent.Future()
        with self._listen(keys, waiter):
            ioloop = tornado.ioloop.IOLoop.current()
            if timeout:
                handle = ioloop.add_timeout(timeout, lambda: waiter.set_exception(BusTimeoutError()))
            else:
                handle = None
            try:
                result = await waiter
            finally:
                if handle:
                    ioloop.remove_timeout(handle)
            return result

    async def waitforkey(self, key, timeout=None):
        """Wait for notification on a single key.

        :param key: An key to be listened to. Key should be immutable.
        :param timeout: If there is no notification coming in for the given timeout, then raise a BusTimeoutError.
        :return: A message that was sent by a notify() or notifyall() call.
        """
        _key, message = await self.waitforkeys([key], timeout)
        return message


class TrackerValidationError(Exception):
    """Raised by OrcaStorm.verify_tracker when verification fails."""
    pass


class OrcaStorm(object):
    """Asynchronous SaasPass authentication client that works with tornado."""
    """Clear this flag to disable validation of SSL certificates. (Not recommended.)"""
    validate_cert = True
    """After this timeout (seconds), token will invalidated from the cache. See `get_token`."""
    token_ttl = 3000.0

    """User agent to be used for making requests to www.saaspass.com"""
    user_agent = "OrcaStorm %s" % __version__

    _token_validuntil = 0
    _token = None

    def __init__(self, api_key, api_password, logger=None):
        """

        :param api_key: Your API key for your custom saaspass applicaiton.
        :param api_password: Your API secret password for your custom saaspass applicaiton.
        :param logger: A logger object that will be used for logging.
        """
        self.http_client = tornado.httpclient.AsyncHTTPClient(defaults=dict(user_agent=self.user_agent))
        self.api_key = api_key
        self.api_password = api_password
        self.logger = logger
        self.login_eventbus = AsyncBus()

    async def get(self, rel_url):
        """Send asnyc GET request to saaspass.com.

        :param rel_url: URL to get, relative to https://www.saaspass.com (including the starting /)
        :return: a Future that has the future value of tornado.httpclient.HTTPResponse object.
        """
        assert (rel_url.startswith("/"))
        url = "https://www.saaspass.com" + rel_url
        if self.logger:
            self.logger.debug("get: awaiting GET %s", url)
        request = tornado.httpclient.HTTPRequest(url=url, method="GET", validate_cert=self.validate_cert)
        response = await self.http_client.fetch(request)
        if self.logger:
            self.logger.debug("get: completed GET %s, code=%s reason='%s'", url, response.code, response.reason)
        if response.error:
            response.rethrow()
        else:
            return response

    async def get_and_parse(self, rel_url):
        """Send asnyc GET request to saaspass.com and parse the response body as JSON data.

        :param rel_url: URL to get, relative to https://www.saaspass.com (including the starting /)
        :return: a data structure loaded with json.loads on the response body."""
        response = await self.get(rel_url)
        return json.loads(response.body.decode("ascii"))

    async def get_token(self):
        """Get a valid token from SaasPass.

        The token is fetched from saaspass.com and cached for `token_ttl` seconds.
        """
        now = time.time()
        if not self._token or self._token_validuntil <= now:
            if self.logger:
                self.logger.debug("get_token: need new token")
            # need new token
            args = urlencode(dict(password=self.api_password))
            response = await self.get_and_parse("/sd/rest/applications/%s/tokens?%s" % (self.api_key, args))
            self._token = response["token"]
            self._token_validuntil = now + self.token_ttl
            if self.logger:
                self.logger.debug("get_token: authenticated, token='%s'", self._token)
        elif self.logger:
            self.logger.debug("get_token: reusing token '%s' (expires in %.1f sec)",
                              self._token, self._token_validuntil - now)
        return self._token

    async def get_barcode(self, typ, sid):
        """Request, fetch barcode image.

        :param typ: Type of the barcode. Can be: "IL", "IRIL" etc. Look at the saaspass API documentation.
        :param sid: Session identifier. This identifies the user session and will be stored in the generated barcode.
        :return: base64 encoded barcode PNG image data
        :rtype: str
        """
        args = urlencode(dict(token=await self.get_token(), type=typ, session=sid))
        relurl = "/sd/rest/applications/%s/barcodes?%s" % (self.api_key, args)
        if self.logger:
            self.logger.debug("get_barcode: %s", relurl)
        response = await self.get_and_parse(relurl)
        return response["barcodeimage"]

    async def verify_tracker(self, tracker_id, username):
        """Verify a tracker id.

        :param tracker_id: The tracker id, as passed in the headers of the login POST callback.
        :param username: The username to be verified.
        :return: If the verification is successful then it returns True. Otherwise it raises a TrackerValidationError
            exception. If the GET request to saaspass fails then it raises tornado.httpclient.HTTPError.
        """
        args = urlencode(dict(token=await self.get_token(), account=username))
        relurl = "/sd/rest/applications/%s/trackers/%s?%s" % (self.api_key, tracker_id, args)
        if self.logger:
            self.logger.debug("verify_tracker: tracker_id='%s', username='%s'", tracker_id, username)
        response = await self.get(relurl)
        if response.code == 200:
            if self.logger:
                self.logger.debug("verify_tracker: VERIFIED tracker_id='%s', username='%s'", tracker_id, username)
            return True
        else:
            if self.logger:
                self.logger.warning("verify_tracker: INVALID tracker_id='%s', username='%s', code='%s', reason='%s'",
                                    tracker_id, username, response.code, response.reason)
            raise TrackerValidationError(response.reason)

    async def verify_otp(self, username, otp):
        """Verify otp code for a user.

        :param username: Name of the user (as assigned to the application account at www.saaspass.com)
        :param otp: One time password, provided by the SaasPass app.
        :return: The response object returned from the verification GET request.
            If the verification fails, then this method will raise tornado.httpclient.HTTPError
        """
        args = urlencode(dict(token=await self.get_token(), username=username, otp=otp))
        relurl = "/sd/rest/applications/%s/otpchecks?%s" % (self.api_key, args)
        if self.logger:
            self.logger.debug("verify_otp: %s", relurl)
        return await self.get(relurl)

    async def notify_login(self, sid, username):
        """Notify client(s) that a user has been logged in.

        :param sid: The session id of the client who has just logged in with saaspass.
        :param username: The name of the user that has been logged in.
        :return: Number of clients notified.
        """
        return self.login_eventbus.notifyall(sid, username)

    async def wait_for_login(self, sid, timeout):
        """Wait until a user is logged in.

        :param sid: The session id of the client who is waiting for a login callback from saaspass.
        :param timeout: A datetime.timedelta instance.After the given timeout, a BusTimeoutError
            will be raised.
        :return: The name of the user that was logged in.(Saaspass returns a username that depends on
            the saaspass registration profile. It can be an email address or a phone number etc.)
        :rtype: str
    """
        return await self.login_eventbus.waitforkey(sid, timeout)
