import abc
import json
import pickle

class PackedException(ValueError):
    pass

class UnpackedException(ValueError):
    pass


class AbstractTransport(abc.ABC):

    @abc.abstractmethod
    def packed(self, data):
        pass

    @abc.abstractmethod
    def unpacked(self, data):
        pass


class JsonTransport(AbstractTransport):

    def packed(self, data):
        return json.dumps(data)

    def unpacked(self, data):
        data = data if isinstance(data, str) else data.decode()
        try:
            return json.loads(data)
        except (TypeError, ValueError) as exc:
            raise UnpackedException("Exception {}: impossible to unpacked data".format(exc.__class__.__name__))


class PickleTransport(AbstractTransport):

    def packed(self, data):
        try:
            return pickle.dumps(data)
        except pickle.PickleError as exc:
            raise PackedException("Exception {}: impossible to packed data".format(exc.__class__.__name__))

    def unpacked(self, data):
        try:
            return pickle.loads(data)
        except pickle.PickleError as exc:
            raise UnpackedException("Exception {}: impossible to unpacked data".format(exc.__class__.__name__))


try:
    import msgpack
except ImportError as exc:
    import warnings

    class FakeMsgPack:
        _fallback = JsonTransport()
        warnings.warn("{}: Msgpack not found. JSON transport is fallback".format(exc), category=ImportWarning)

        def packb(self, data):
            return self._fallback.packed(data)

        def unpackb(self, data):
            return self._fallback.unpacked(data)
    msgpack = FakeMsgPack()


class MsgPackTransport(AbstractTransport):

    def packed(self, data):
        try:
            return msgpack.packb(data)
        except msgpack.exceptions.PackException as exc:
            raise PackedException("Exception {}: impossible to packed data".format(exc.__class__.__name__))

    def unpacked(self, data):
        data = data.encode() if isinstance(data, str) else data
        try:
            retval = msgpack.unpackb(data)
        except msgpack.exceptions.UnpackException as exc:
            raise UnpackedException("Exception {}: impossible to unpacked data".format(exc.__class__.__name__))

        retval = {k if isinstance(k, str) else k.decode(): v for k, v in retval.items()}
        return retval
