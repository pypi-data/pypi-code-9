import uuid

import redis

from .exceptions import *
from . import transport
from .models import Request, Response


class Client:
    def __init__(
            self,
            redis_connection,
            request_channel,
            transport_klass=transport.JsonTransport,
            response_timeout=1):

        assert isinstance(redis_connection, redis.StrictRedis)
        assert isinstance(request_channel, str)
        assert isinstance(response_timeout, int)
        assert issubclass(transport_klass, transport.AbstractTransport)

        self._redis = redis_connection
        self._request_channel = request_channel
        self._timeout = response_timeout
        self._transport = transport_klass()

        self.__fname = None
        self.__response_channel = None
        self.__unauthorized_cb = ('stop', 'start')

        self.__null_response = self._transport.packed(Response())

    def __getattr__(self, name):
        if any([name.startswith('__'), name.endswith('__')]):
            raise AttributeError("Remote function not start with '__' or end with '__' ")

        if name in self.__unauthorized_cb:
            raise AttributeError("Callback {} is unauthorized".format(name))

        def wrapper(*args, **kwargs):
            self.__fname = name
            return self.__run(*args, **kwargs)

        return wrapper

    def __run(self, *args, **kwargs):
        assert self.__fname is not None
        assert self.__response_channel is None

        if self._redis.exists(self._request_channel) is False:
            raise RequestChannelNotExists("{} not exists - May be server not started".format(self._request_channel))

        _response_channel = '{}:rpc:{}'.format(self._request_channel, uuid.uuid4())
        if self._redis.exists(_response_channel):
            raise ResponseChannelAlreadyExists("{} already exists".format(_response_channel))
        self.__response_channel = _response_channel
        return self.__execute(args, kwargs)

    def __execute(self, _call_args, _call_kwargs):
        request = Request(_call=self.__fname, args=_call_args,
                          kwargs=_call_kwargs, response_channel=self.__response_channel)
        try:
            request_packed = self._transport.packed(request)
        except transport.PackedException:
            raise PackedRequestFail("Impossible to packed {!r} with {}".format(request,
                                                                               self._transport.__class__.__name__))

        self._redis.lpushx(self._request_channel, request_packed)
        try:
            _chan, retval = self._redis.blpop(self.__response_channel, timeout=self._timeout)
            assert _chan.decode() == self.__response_channel
            retval_unpacked = self._transport.unpacked(retval or self.__null_response)
        except (redis.exceptions.TimeoutError,):
            raise ResponseTimeOutError("Response not receive after {}s waiting".format(self._timeout))
        except transport.UnpackedException:
            raise UnpackedResponseFail("Impossible to unpack "
                                       "response {!r} with {}".format(retval, self._transport.__class__.__name__))
        else:
            assert isinstance(retval_unpacked, dict)
            return Response(**retval_unpacked)
        finally:
            self.__close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def __close(self):
        self._redis.delete(self.__response_channel)
        self.__response_channel = None
