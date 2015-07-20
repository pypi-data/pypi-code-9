# coding: utf-8
from sqlalchemy import TypeDecorator, VARCHAR, event
from sqlalchemy.orm.mapper import Mapper
from werkzeug.datastructures import FileStorage
from flask import current_app
from .mediasets import Media


__all__ = (
    'MediaType',
)


__author__ = 'vadim'


class MediaType(TypeDecorator):
    """
    Usage::
        MediaType(255)
    """

    impl = VARCHAR

    PATH_LEN = 255

    def __init__(self, *args, **kwargs):
        # TODO: Implement default file
        self.media_name = kwargs.pop('mediaset') if 'mediaset' in kwargs else None
        self.default_file = kwargs.pop('default_file') if 'default_file' in kwargs else None

        if not args and not 'length' in kwargs:
            kwargs['length'] = self.PATH_LEN
        super(MediaType, self).__init__(*args, **kwargs)

    @property
    def _media(self):
        return current_app.extensions['media'].media

    def process_bind_param(self, value, dialect):
        """
        Python to database
        """
        assert self.media_name, 'mediaset not initialized'
        if value is not None:
            media = self._media
            if isinstance(value, FileStorage):
                mediafile = media[self.media_name].save(value)
                value = mediafile.filename
            elif isinstance(value, media.MediaFile):
                value = value.filename
            elif isinstance(value, media.MediaStubFile):
                value = None
        return value

    def process_result_value(self, value, dialect):
        """
        Database to python
        """
        assert self.media_name, 'mediaset not initialized'
        mediaset = self._media[self.media_name]
        if value:
            value = mediaset[value]
        else:
            value = mediaset.get_stub(self.default_file)
        return value


def _remove_related_files_after_delete_row(mapper, connection, target):
    """
    Hook removed deleted files
    :param mapper: Mapper model ORM
    :param connection:
    :param target: entity
    :return:
    """
    for c in mapper.columns:
        try:
            field = getattr(target, c.name)
            if field and isinstance(field, Media.MediaFile):
                field.remove()
        except Exception:
            pass

event.listen(Mapper, 'after_delete', _remove_related_files_after_delete_row)
