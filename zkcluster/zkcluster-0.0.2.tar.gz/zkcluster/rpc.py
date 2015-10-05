"""Implement a simple RPC model on top of p2p.
"""
import collections
import re
import logging
import itertools

from . import util
from . import exc

log = logging.getLogger(__name__)


class RPCService(object):

    def __init__(self, rpc_reg, transport, rpc_call_timeout=5):
        self.rpc_reg = rpc_reg
        self.transport = transport
        self._message_id = itertools.count(1)
        self.async_suite = transport.async_suite
        self.rpc_call_timeout = rpc_call_timeout
        self._callbacks = {}
        self._listeners = collections.defaultdict(list)

    def speak_rpc(self, rpc_reg):
        self.rpc_reg = self.rpc_reg.join(rpc_reg)

    def listen(self, fn, evt_cls):
        self._listeners[evt_cls].append(fn)

    def message_received(self, message, expected=None):
        match = re.match(
            "^RPC_(REQ|RESP|ERR|EVT)\((\d+), (.+?)\)\: (.*)", message)
        if not match:
            return
        log.debug("received RPC message %s", message)
        message_type = match.group(1)
        message_id = int(match.group(2))
        rpc_name = match.group(3)
        message = match.group(4)

        if message_type == 'REQ':
            self._service_request(
                message_id, rpc_name, message, expected=expected)
        elif expected:
            raise exc.RPCError("Expected only request of type %s" % expected)
        elif message_type == 'RESP':
            self._service_response(message_id, rpc_name, message)
        elif message_type == 'ERR':
            self._service_error(message_id, rpc_name, message)
        elif message_type == 'EVT':
            self._service_event(message_id, rpc_name, message)
        else:
            assert False

    def _service_request(self, message_id, rpc_name, message, expected=None):
        rpc_cls = self.rpc_reg._calls[rpc_name]

        if expected and not issubclass(expected, rpc_cls):
            self._send_error(message_id, rpc_name, "unexpected message")

        try:
            rpc_obj = rpc_cls(*util.json_loads(message))
        except TypeError as te:
            self._send_error(message_id, rpc_name, str(te))
        else:
            try:
                response = rpc_obj.receive_request(self, self.transport)
            except Exception as err:
                log.error("Error from RPC handler", exc_info=True)
                self._send_error(message_id, rpc_name, err)
            else:
                msg = "RPC_RESP(%s, %s): %s" % (
                    message_id, rpc_name, util.json_dumps(response)
                )
                log.debug("send RPC response %s", msg)
                self.transport.send_message(msg)

    def _service_response(self, message_id, rpc_name, message):
        response = util.json_loads(message)
        waiter = self._callbacks.pop(message_id, None)
        if waiter:
            waiter.set(response)

    def _service_error(self, message_id, rpc_name, message):
        exception = exc.RPCError(message)
        waiter = self._callbacks.pop(message_id, None)
        if waiter:
            waiter.set_exception(exception)

    def _service_event(self, message_id, rpc_name, message):
        rpc_cls = self.rpc_reg._calls[rpc_name]
        try:
            rpc_obj = rpc_cls(*util.json_loads(message))
        except TypeError:
            log.error("Couldn't deserialize rpc event: %s", message)
        else:
            rpc_obj.receive_request(self, self.transport)
            for listener in self._listeners[rpc_cls]:
                listener(rpc_obj)
        return message_id, None, None

    def _send_sync(self, cmd, timeout):
        waiter = self._send_async(cmd, timeout=timeout)
        return waiter.get()

    def _send_async(
            self, cmd, callback=None, exception_callback=None, timeout=None):
        if timeout is None:
            timeout = self.rpc_call_timeout

        message_id = next(self._message_id)

        waiter = self.async_suite.spawn_waiter(
            success=callback,
            failure=exception_callback,
            timeout=timeout,
            on_timeout=lambda: self._callbacks.pop(message_id)
        )
        self._callbacks[message_id] = waiter

        waiter.start()

        self.transport.send_message(
            "RPC_REQ(%s, %s): %s" % (
                message_id, cmd.__class__.__name__, util.json_dumps(cmd))
        )

        return waiter

    def _send_error(self, message_id, rpc_name, errmsg):
        msg = "RPC_ERR(%s, %s): %s" % (
            message_id, rpc_name, errmsg
        )
        log.debug("send RPC error %s", msg)
        self.transport.send_message(msg)

    def _send_event(self, cmd):
        rpc_obj = cmd
        rpc_name = rpc_obj.__class__.__name__
        message_id = next(self._message_id)
        msg = "RPC_EVT(%s, %s): %s" % (
            message_id, rpc_name, util.json_dumps(rpc_obj)
        )
        log.debug("send RPC event %s", msg)
        self.transport.send_message(msg)


class RPCReg(object):
    def __init__(self):
        self._calls = {}

    def join(self, other):
        reg = RPCReg()
        reg._calls.update(self._calls)
        reg._calls.update(other._calls)
        return reg

    def call(self, *fields):

        def decorate(cls):
            new_rpc_type = type(
                cls.__name__,
                (
                    cls,
                    collections.namedtuple(cls.__name__, fields),
                    RPC
                ),
                {}
            )
            self._calls[cls.__name__] = new_rpc_type
            return new_rpc_type
        return decorate


class RPC(tuple):

    def send_async(
            self, rpc, callback, exception_callback=None, timeout=None):
        return rpc._send_async(self, callback, exception_callback, timeout)

    def send(self, rpc, timeout=None):
        return rpc._send_sync(self, timeout=timeout)

    def receive_request(self, rpc, service):
        raise NotImplementedError()

    def _serialize(self):
        return util.json_dumps(self)

    def __nonzero__(self):
        return True


class RPCEvent(RPC):
    def send_async(
            self, rpc, callback, exception_callback=None, timeout=None):
        raise NotImplementedError("Call send() for RPCEvent sending")

    def send(self, rpc):
        rpc._send_event(self)

    def receive_request(self, rpc, service):
        pass

rpc_reg = RPCReg()


@rpc_reg.call('target', 'greeting')
class HelloRPC(RPC):
    """Sample RPC message.

    E.g.::

        msg = rpc.HelloRPC("some nodename", "some greeting")
        response = msg.send(some_rpc_module, some_target)
        print "Got repsonse! %s" % response

    """
    def receive_request(self, rpc, service):
        return ("Well %s to you too, %s!" % (self.greeting, self.target))
