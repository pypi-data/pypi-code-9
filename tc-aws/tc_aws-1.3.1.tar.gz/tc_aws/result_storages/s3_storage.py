#coding: utf-8

from thumbor.result_storages import BaseStorage

from ..aws.storage import AwsStorage


class Storage(AwsStorage, BaseStorage):
    def __init__(self, context):
        BaseStorage.__init__(self, context)
        AwsStorage.__init__(self, context, 'RESULT_STORAGE')

    def put(self, bytes):
        path = self.normalize_path(self.context.request.url)
        self.set(bytes, path)

        return path

    def get(self, path=None):
        if path is None:
            path = self.context.request.url

        return super(Storage, self).get(path)
