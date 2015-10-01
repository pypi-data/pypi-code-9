#coding: utf-8

from json import loads, dumps

from os.path import splitext

from thumbor.storages import BaseStorage

from ..aws.storage import AwsStorage


class Storage(AwsStorage, BaseStorage):

    def __init__(self, context):
        BaseStorage.__init__(self, context)
        AwsStorage.__init__(self, context, 'STORAGE')

    def put(self, path, bytes):
        self.set(bytes, self.normalize_path(path))

        return path

    def put_crypto(self, path):
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return

        if not self.context.server.security_key:
            raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

        file_abspath = self.normalize_path(path)
        crypto_path = '%s.txt' % splitext(file_abspath)[0]

        self.set(self.context.server.security_key, crypto_path)

        return crypto_path

    def put_detector_data(self, path, data):
        file_abspath = self.normalize_path(path)

        path = '%s.detectors.txt' % splitext(file_abspath)[0]

        self.set(dumps(data), path)

        return path

    def get_crypto(self, path):
        file_abspath = self.normalize_path(path)
        crypto_path = "%s.txt" % (splitext(file_abspath)[0])

        file_key = self.storage.get_key(crypto_path)

        if not file_key:
            return None

        return file_key.read()

    def get_detector_data(self, path):
        file_abspath = self.normalize_path(path)
        path = '%s.detectors.txt' % splitext(file_abspath)[0]

        file_key = self.storage.get_key(path)

        if not file_key or self.is_expired(file_key):
            return None

        return loads(file_key.read())

    def exists(self, path):
        file_abspath = self.normalize_path(path)
        file_key = self.storage.get_key(file_abspath)

        if not file_key:
            return False

        return True

    def remove(self, path):
        if not self.exists(path):
            return

        if not self.storage.delete_key(path):
            return False

        return True

    def resolve_original_photo_path(self, filename):
        return filename
