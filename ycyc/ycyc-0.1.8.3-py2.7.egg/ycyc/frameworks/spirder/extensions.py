#!/usr/bin/env python
# encoding: utf-8

from functools import partial
from os import path as os_path

from ycyc.base.decoratorutils import chainingmethod
from ycyc.base.filetools import make_sure_dir_empty, available_file_name


class BaseExtension(object):
    def __init__(self, spirder):
        self.spirder = spirder

    def __getattr__(self, name):
        return getattr(self.spirder, name)


class ExtensionsWraper(object):
    def __init__(self, spirder):
        self.spirder = spirder
        self.wraper = spirder

    @chainingmethod
    def install(self, extension_installer):
        extension_installer(self.spirder)


class ResultCacheExtension(BaseExtension):
    @classmethod
    def cache_to(cls, cache_path):
        return partial(cls, cache_path=cache_path)

    def __init__(self, spirder, cache_path=None):
        self.cache_path = cache_path or "./cache"
        make_sure_dir_empty(self.cache_path)

        super(ResultCacheExtension, self).__init__(spirder)
        spirder.on_response = self.on_response

    def on_response(self, response, request, callback):
        name = available_file_name(request.url)
        with open(os_path.join(self.cache_path, name), "rb") as fp:
            fp.write(response.content)

        return self.spirder.on_response(response, request, callback)
