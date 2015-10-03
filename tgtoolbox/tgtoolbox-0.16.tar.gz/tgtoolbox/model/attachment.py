# -*- coding: utf-8 -*-
__author__ = 'vahid'

import os.path
from sqlalchemy import event
from sqlalchemy.orm.attributes import InstrumentedAttribute
from tgext.datahelpers.fields import Attachment as DataHelperAttachment
from tgext.datahelpers.attachments import AttachedImage as DataHelperAttachedImage, AttachedFile

try:
    from PIL import Image
except ImportError:
    import Image


class Attachment(DataHelperAttachment):

    def process_bind_param(self, value, dialect):
        if isinstance(value, NullAttachedImage):
            value = None
        return super(Attachment, self).process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        result = super(Attachment, self).process_result_value(value, dialect)
        if result:
            return result
        return self.attachment_type.create_null_attachment()


class NullAttachedImage(object):
    #url = '/img/no-image-available.jpg'
    thumb_url = url ='/img/no-image-available.jpg'

    def __eq__(self, other):
        return other is None

    def __ne__(self, other):
        return other is not None

    def __nonzero__(self):
        return False


class NullGrayscaleAttachedImage(NullAttachedImage):
    gray_thumb_url = NullAttachedImage.url


class AttachedImage(DataHelperAttachedImage):

    def write(self):
        AttachedFile.write(self)

        if getattr(self.file, 'name', None) != self.local_path:
            self.file.seek(0)
            thumbnail = Image.open(self.file)
            thumbnail.thumbnail(self.thumbnail_size, Image.ANTIALIAS)
            thumbnail = thumbnail.convert('RGBA')
            thumbnail.format = self.thumbnail_format
            thumbnail.save(self.thumb_local_path)

    @classmethod
    def create_null_attachment(cls):
        return NullAttachedImage()


class GrayscaleAttachedImage(AttachedImage):

    def __init__(self, file, filename, uuid=None):
        super(GrayscaleAttachedImage, self).__init__(file, filename, uuid=uuid)

        gray_thumb_filename = 'thumb-gray.'+self.thumbnail_format.lower()
        self.gray_thumb_local_path = os.path.join(self.attachment_dir, gray_thumb_filename)
        self.gray_thumb_url = '/'.join([self.attachments_url, self.uuid, gray_thumb_filename])

    def write(self):
        super(GrayscaleAttachedImage, self).write()

        if getattr(self.file, 'name', None) != self.local_path:
            self.file.seek(0)
            thumbnail = Image.open(self.file)
            thumbnail.thumbnail(self.thumbnail_size, Image.ANTIALIAS)
            thumbnail = thumbnail.convert('LA') # Make grayscale
            thumbnail.format = self.thumbnail_format
            thumbnail.save(self.gray_thumb_local_path)

    @classmethod
    def create_null_attachment(cls):
        return NullGrayscaleAttachedImage()

class GoldenRatioAttachedImage(AttachedImage):
    golden_ratio = 1.6180339887
    width = 230
    thumbnail_size = (width, width / golden_ratio )


class AttachmentCleanerMixin(object):

    @staticmethod
    def after_delete_banner(mapper, connection, target):
        for k, v in target.__table__.columns.items():
            if isinstance(v.type, Attachment):
                column_value = getattr(target, k)
                if column_value is not None and isinstance(column_value, AttachedFile):
                    column_value.unlink()

    @staticmethod
    def on_set(target, value, oldvalue, initiator):
        if oldvalue and isinstance(oldvalue, AttachedFile):
            oldvalue.unlink()

    @classmethod
    def register_events(cls):
        event.listen(cls, 'after_delete', cls.after_delete_banner)
        columns = {name: attr for name, attr in cls.__dict__.copy().iteritems()\
                   if isinstance(attr, InstrumentedAttribute)\
                        and hasattr(attr.property, 'columns')\
                        and len(attr.property.columns)\
                        and isinstance(attr.property.columns[0].type, Attachment)}
        for name, attr in columns.iteritems():
            event.listen(getattr(cls, name), 'set', cls.on_set)

