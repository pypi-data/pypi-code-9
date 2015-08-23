# coding: utf-8
import copy

from drivigo_api_client.sync import SyncResources


class Client(object):
    __slots__ = ('args', 'kwargs')

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def make_args_kwargs(self, *args, **kwargs):
        kwargs2 = copy.deepcopy(self.kwargs)
        kwargs2.update(kwargs)
        return self.args + args, kwargs2

    def sync(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return SyncResources(*args2, **kwargs2)
