import logging
import time

from threading import Event

import redis

from rpcviaredis import transport
from rpcviaredis.models import Response
from rpcviaredis import exceptions


class ServerRPC:

    def __init__(
            self,
            redis_connection,
            request_channel,
            transport_klass=transport.JsonTransport,
            event=None):

        assert isinstance(redis_connection, redis.StrictRedis)
        assert isinstance(request_channel, str)
        assert isinstance(event, type(None)) or all((hasattr(event, 'set'), hasattr(event, 'is_set')))
        assert issubclass(transport_klass, transport.AbstractTransport)

        self._redis = redis_connection
        self._request_channel = request_channel

        self.__transport = transport_klass()
        self.__event = event or Event()

    def stop(self):
        self.__event.set()

    def start(self):
        self.__run()

    def ping(self):
        rep = Response(response='pong', return_code=200)
        return rep

    def __run(self):
        self.__init_channel()
        while self.__event.is_set() is False:
            if self._redis.llen(self._request_channel) <= 1:
                time.sleep(0.001)
                continue
            request = self._redis.lpop(self._request_channel)
            try:
                request_unpacked = self.__transport.unpacked(request)
            except transport.UnpackedException:
                _rep = Response(exception=transport.UnpackedException.__name__, return_code=402,
                                reason="Unpack request failed")
                message_packed = self.__prepare_response(_rep)
                logging.debug('RPC Request on %s: Impossible to route request - Unpack failed' % self._request_channel)
            else:
                logging.debug('RPC Request on %s: %r' % (self._request_channel, request_unpacked))
                response_channel = request_unpacked['response_channel']
                callback = request_unpacked['_call']
                cb_args = request_unpacked['args']
                cb_kwargs = request_unpacked['kwargs']

                message_packed = self.__dispatcher(callback, cb_args, cb_kwargs)

            logging.debug('RPC Response send on %s' % response_channel)
            self._redis.rpush(response_channel, message_packed)

        self.__destroy_channel()

    def __destroy_channel(self):
        """
        If channel exists, remove it
        """
        if self._redis.exists(self._request_channel):
            self._redis.delete(self._request_channel)

    def __init_channel(self):
        """
        Remove request channel (list) if it exists and
        create empty list (new request channel)
        :return:
        """
        self.__destroy_channel()
        self._redis.lpush(self._request_channel, "i")

    def __dispatcher(self, cb, cb_args, cb_kwargs):
        """
        Run remote command
        :param cb: remote command
        :param cb_args: callback args
        :param cb_kwargs: callback kwargs
        :return:
        """
        cb = cb if isinstance(cb, str) else cb.decode()
        _response = Response()
        _cb = getattr(self, cb, None)

        if _cb is None:
            _response = Response(return_code=404, exception=exceptions.CallbackNotFound.__name__,
                                 reason="{} not found".format(cb))
            return self.__prepare_response(_response)

        try:
            _response = _cb(*cb_args, **cb_kwargs)
            assert isinstance(_response, Response), "Callback must be return <Response> instance"
        except Exception as exc:
            _response = Response(exception=exc.__class__.__name__, return_code=502,
                                 reason="Error: {} - callback: {} "
                                        "- args: {!r} - kwargs: {!r}".format(str(exc), cb, cb_args, cb_kwargs))
        finally:
            return self.__prepare_response(_response)

    def __prepare_response(self, _rep):
        assert isinstance(_rep, Response)

        try:
            return self.__transport.packed(_rep)
        except transport.PackedException:
            sentinel = Response(return_code=502, reason="Prepare response failed",
                                exception=transport.PackedException.__name__)
            return self.__transport.packed(sentinel)
