from frasco import current_app, url_for
from flask import safe_join
import os


upload_backends = {}


def file_upload_backend(cls):
    upload_backends[cls.name] = cls
    return cls


class StorageBackend(object):
    def __init__(self, options):
        self.options = options

    def save(self, file, filename):
        raise NotImplementedError

    def url_for(self, filename, **kwargs):
        raise NotImplementedError

    def delete(self, filename):
        raise NotImplementedError


@file_upload_backend
class LocalStorageBackend(StorageBackend):
    name = 'local'

    def save(self, file, filename):
        filename = safe_join(self.options["upload_dir"], filename)
        if not os.path.isabs(filename):
            filename = os.path.join(current_app.root_path, filename)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        file.save(filename)

    def url_for(self, filename, **kwargs):
        return url_for("static_upload", filename=filename, **kwargs)

    def delete(self, filename):
        filename = safe_join(self.options["upload_dir"], filename)
        if not os.path.isabs(filename):
            filename = os.path.join(current_app.root_path, filename)
        if os.path.exists(pathname):
            os.unlink(pathname)


@file_upload_backend
class HttpStorageBackend(StorageBackend):
    name = 'http'

    def url_for(self, filename, **kwargs):
        return 'http://' + filename


@file_upload_backend
class HttpsStorageBackend(StorageBackend):
    name = 'https'

    def url_for(self, filename, **kwargs):
        return 'https://' + filename