class ReqRep(dict):

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError("{} isn't object attributes".format(key))

    def __delattr__(self, *args, **kwargs):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            raise AttributeError("Attribute {} is not allowed".format(key))
        super().__setitem__(key, value)

    def __delitem__(self, key):
        raise NotImplementedError()

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, obj):
        for attr in self.__slots__:
            setattr(self, attr, obj[attr])


class Request(ReqRep):
    """
    User request skeleton
    _call: Remote function will be call
    args: Remote function positional arguments
    kwargs: Remote function keyword arguments
    response_channel: Channel of response
    :exception AttributeError if attribute not listing in __slots__
    :exception NotImplementedError for __delattr__ and __delitem__
    """

    __slots__ = ('_call', 'args', 'kwargs', 'response_channel')

    def __init__(self, **kwargs):
        super().__init__()
        self._call = kwargs.get('_call', None)
        self.args = kwargs.get('args', None)
        self.kwargs = kwargs.get('kwargs', None)
        self.response_channel = kwargs.get('response_channel', None)


class Response(ReqRep):
    """
    Request response skeleton
    response: Server response
    exception: Exception occurred during request processing
    reason: Reason of the exception
    return_code: Like HTTP response code
    :exception AttributeError if attribute not listing in __slots__
    :exception NotImplementedError for __delattr__ and __delitem__
    """

    __slots__ = ('response', 'exception', 'reason', 'return_code')

    def __init__(self, **kwargs):
        super().__init__()
        self.response = kwargs.get('response', None)
        self.exception = kwargs.get('exception', None)
        self.reason = kwargs.get('reason', None)
        self.return_code = kwargs.get('return_code', None)
