# coding: utf-8
"""
    flask.ext.media
    ~~~~~~~~~~~~~~~~~~~

    Flask-Media is a Flask extension that provides an easy way upload, manage and download stored file

    :copyright: (c) 2014 Vadim Statishin.
    :license: MIT, see LICENSE for more details.

    Based on Flask-Uploads
    :copyright: 2010 Matthew "LeafStorm" Frazier
    :license:   MIT/X11, see LICENSE for details
"""
import glob
import os
import random
import logging
from datetime import date
from flask import send_from_directory, abort
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename, import_string
try:
    from .image import thumbnail
except:
    thumbnail = None


__all__ = (
    'Media',
)


__author__ = 'vadim'


__version__ = '0.1'


class UploadNotAllowed(Exception):
    """
    This exception is raised if the upload was not allowed. You should catch
    it in your view code and display an appropriate message to the user.
    """


class MediaSetNotConfigured(Exception):
    """
    This exception is raised if the mediaset was not configured. You should catch
    it in your view code and display an appropriate message to the user.
    """


def extension(filename, without_dot=None):
    name, ext = os.path.splitext(filename)
    if ext:
        if without_dot and ext[0] == '.':
            ext = ext[1:]
        return ext.lower()


def make_dir(x):
    if not os.path.exists(x):
        os.makedirs(x)


RANDOM_LITERAL = '0123456789abcdef'


def make_path(num=None):
    if num:
        gen_fun = lambda: random.choice(RANDOM_LITERAL) + random.choice(RANDOM_LITERAL)
        p = [gen_fun() for i in range(num)]
        return os.path.join(*p)
    return ''


class _MediaState(object):
    """Remembers configuration for the (media, app) tuple."""

    def __init__(self, media, app):
        self.media = media
        self.app = app


class Media(object):
    """
    A Flask extension for manage Media.

    :param app: a :class:`~flask.Flask` instance. Defaults to `None`. If no
        application is provided on creation, then it can be provided later on
        via :meth:`init_app`.
    """
    def __init__(self, app=None, folder_level=None, use_folder_date=None):
        self.sets = {}
        self.folder_level = folder_level or 3
        self.use_folder_date = use_folder_date or False
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        """
        Initialize this Flask-Media extension for the given application.

        :param app: a :class:`~flask.Flask` instance
        """
        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if 'media' in app.extensions:
            app.logger.warning('Flask-Media already configure!')
            return

        app.extensions['media'] = _MediaState(self, app)

        app.config.setdefault('MEDIA_SETS', '')
        app.config.setdefault('MEDIA_HANDLER', True)
        app.config.setdefault('MEDIA_URL', '/media')
        app.config.setdefault('MEDIA_PATH', 'media')
        app.config.setdefault('MEDIA_ALLOW', [])
        app.config.setdefault('MEDIA_DENY', [])
        app.config.setdefault('MEDIA_SPLIT', 0)
        app.config.setdefault('MEDIA_THUMB_PATH', 'thumb')

        self.use_folder_date = app.config.get('MEDIA_FOLDER_DATE', self.use_folder_date)
        self.folder_level = app.config.get('MEDIA_FOLDER_LEVEL', self.folder_level)

        for name in app.config['MEDIA_SETS'].split():
            upname = name.upper()

            path = app.config.get('MEDIA_PATH_' + upname) or os.path.join(app.config['MEDIA_PATH'], name)
            if not path.startswith('/'):
                path = os.path.join(app.instance_path, path)
            path = os.path.normpath(path)

            allow = app.config.get('MEDIA_ALLOW_' + upname) or app.config['MEDIA_ALLOW']
            if isinstance(allow, basestring):
                allow = tuple(allow.split())

            deny = app.config.get('MEDIA_DENY_' + upname) or app.config['MEDIA_DENY']
            if isinstance(deny, basestring):
                deny = tuple(deny.split())

            hook = app.config.get('MEDIA_HOOK_' + name.upper())
            if hook:
                hook = import_string(hook)

            mediaset = Media.MediaSet(name)

            mediaset.init_set(
                url=app.config.get('MEDIA_URL_' + upname) or os.path.join(app.config['MEDIA_URL'], name),
                path=path,
                allow=allow,
                deny=deny,
                hook=hook,
                split_folder=app.config.get('MEDIA_SPLIT_' + upname) or app.config['MEDIA_SPLIT'],
                thumbnail_path=app.config.get('MEDIA_THUMB_PATH_' + upname) or app.config['MEDIA_THUMB_PATH']
            )

            self.sets[name] = mediaset

        if app.config['MEDIA_HANDLER']:
            @app.route(app.config['MEDIA_URL'] + '/<setname>/<path:filename>')
            def uploaded_file(setname, filename):
                """
                Handler download via app uploaded files
                """
                try:
                    mediaset = self[setname]
                    if not mediaset:
                        abort(404)
                    media = mediaset[filename]
                    filepath = media.path
                    if not os.path.exists(filepath):
                        fun = mediaset.hook
                        if fun:
                            fun('demand', setname, filename)
                    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))
                except MediaSetNotConfigured:
                    abort(400)

    def __getitem__(self, item):
        """
        Return named mediaset
        :param item: name mediaset
        :return:
        """
        if not item in self.sets:
            raise MediaSetNotConfigured()
        return self.sets.get(item)

    class MediaBaseFile(object):
        """
        Base media file class
        """
        empty = True  # Media file don't set. Get from default value.

    class MediaStubFile(MediaBaseFile):
        def __init__(self, stub_file):
            self.stub_file = stub_file

        @property
        def url(self):
            try:
                url = self.stub_file
                if callable(url):
                    url = url(None)
                return url
            except Exception:
                return None

        @property
        def path(self):
            return None

        def remove(self):
            pass

        def thumbnail(self, size, crop=None):
            url = self.stub_file
            if callable(url):
                url = url(size)
            return url

    class MediaFile(MediaBaseFile):
        empty = False  # Media file set

        def __init__(self, mediaset, filename):
            self.mediaset = mediaset
            self.filename = filename

        @property
        def url(self):
            """
            :param filename: The filename to return the URL for.
            """
            return os.path.join(self.mediaset.url, self.filename)

        @property
        def path(self):
            """
            Returns the absolute path of a file uploaded to this media set.

            :param filename: The filename to return the path for.
            """
            return os.path.join(self.mediaset.path, self.filename)

        @property
        def exist(self):
            """
            Check file exist in mediaset
            :return:
            """
            return os.path.isfile(self.path)

        def remove(self):
            """
            Remove of a uploaded file from this media set.

            :param filename: The filename to return the path for.
            """
            path = self.path

            if self.mediaset.hook:
                self.mediaset.hook('remove', self.mediaset.name, self.filename)

            if os.path.isfile(path):
                os.unlink(path)

            filename = os.path.basename(path)
            name, ext = os.path.splitext(filename)
            path_to_thumbs = '{thumb_path}/{name}*{ext}'.format(thumb_path=self.thumbnail_path, name=name, ext=ext)
            for rmfile in glob.glob(path_to_thumbs):
                if os.path.isfile(rmfile):
                    os.unlink(rmfile)

        @property
        def thumbnail_path(self):
            """
            Format thumbnails path
            :return:
            """
            if self.mediaset.thumbnail_path is None:
                thumb_path = os.path.join(os.path.dirname(self.path), 'thumb')
            elif not self.mediaset.thumbnail_path.startswith('/'):
                thumb_path = os.path.join(os.path.dirname(self.path), self.mediaset.thumbnail_path)
            else:
                thumb_path = self.mediaset.thumbnail_path
            return thumb_path

        def thumbnail(self, size, crop=None):
            """
            Make image thumbnail
            :param size: Size thumbnail WidthxHegight. Example: 250x150
            :param crop: cropping method. Support: 'fit', 'pad' or None(default)
            :return:
            """
            if not thumbnail:
                logging.warning(u'Image package not installed')
                return ''
            thumb_file = thumbnail(self.path, size, crop, thumb_path=self.thumbnail_path)
            if thumb_file:
                thumb_file = thumb_file[len(self.mediaset.path) + 1:]
                return os.path.join(self.mediaset.url, thumb_file)
            return ''

    class MediaSet(object):
        """
        Class define mediaset
        """
        def __init__(self, name, url=None, path=None, allow=None, deny=None, hook=None, split_folder=0, thumbnail_path=None):
            self.name = name
            self.url = url
            self.path = path
            self.allow = allow
            self.deny = deny
            self.hook = hook
            self.split_folder = split_folder
            self.thumbnail_path = thumbnail_path or 'thumb'

        def init_set(self, url, path, allow, deny, hook=None, split_folder=0, thumbnail_path=None):
            self.url = url
            self.path = path
            self.allow = allow
            self.deny = deny
            self.hook = hook
            self.split_folder = split_folder
            if thumbnail_path:
                self.thumbnail_path = thumbnail_path

        @property
        def is_configure(self):
            return not self.path is None

        def assert_configure(self):
            if not self.is_configure:
                raise MediaSetNotConfigured(u'Media set {} not configured'.format(self.name))

        def file_allowed(self, storage=None, filename=None):
            """
            Check allowed file by extension
            :param storage: storage file
            :param filename:
            :return:
            """
            if not filename and storage:
                filename = storage.filename
            if filename:
                ext = extension(filename, True)
                if self.allow and ext in self.allow:
                    if not self.deny or (self.deny and not ext in self.deny):
                        return True
            return False

        def __getitem__(self, item):
            """
            Return media file
            :param item:
            :return:
            """
            self.assert_configure()
            return Media.MediaFile(self, item)

        @property
        def items(self):
            """
            Generator created media files
            :return:
            """
            def iterate_dir(p):
                for path, dir, files in os.walk(p):
                    if not path.endswith(self.thumbnail_path):
                        for f in files:
                            yield os.path.join(path, f)
            for item in iterate_dir(self.path):
                item = os.path.relpath(item, self.path)
                yield self[item]

        @classmethod
        def get_stub(cls, default_file):
            return Media.MediaStubFile(default_file)

        def save(self, storage):
            """
            This saves a `werkzeug.FileStorage` into this upload set. If the
            upload is not allowed, an `UploadNotAllowed` error will be raised.
            Otherwise, the file will be saved and its name (including the folder)
            will be returned.

            :param storage: The uploaded file to save.
            """
            self.assert_configure()

            if not isinstance(storage, FileStorage):
                raise TypeError("storage must be a werkzeug. FileStorage")

            if not self.file_allowed(None, storage.filename):
                raise UploadNotAllowed()

            # filesize = storage.stream.tell()
            if self.split_folder >= 0:
                extra_path = make_path(self.split_folder)
            else:
                extra_path = date.today().strftime('%Y/%m/%d')
            origname, ext = os.path.splitext(secure_filename(secure_filename(storage.filename)))

            filename = os.path.join(extra_path, '%s%s' % (origname, ext))
            target = os.path.join(self.path, filename)
            count = 0
            while True:
                if not os.path.exists(target):
                    break
                count += 1
                filename = os.path.join(extra_path, '%s_%d%s' % (origname, count, ext))
                target = os.path.join(self.path, filename)

            make_dir(os.path.dirname(target))

            storage.save(target)

            if self.hook:
                self.hook('save', self.name, filename)

            return Media.MediaFile(self, filename)
