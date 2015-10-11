# coding: utf-8

import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


IMAGES_EXTENSIONS = [
    '.jpeg', '.jpg', '.jfif', '.exif', '.tiff', '.gif', '.bmp',
    '.png', '.ppm', '.pgm', '.pbm', '.pnm', '.webp', '.svg', '.ico',
]


@python_2_unicode_compatible
class FileBase(models.Model):
    file = models.FileField('Файл', upload_to='sticky/files/')

    class Meta:
        abstract = True
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    @property
    def filetype(self):
        if not self.file:
            return None

        if os.path.splitext(self.file.name)[1] in IMAGES_EXTENSIONS:
            return 'image'

        return 'document'

    def __str__(self):
        if self.file:
            return self.file.name
        return u'no file: {}'.format(self.id)


class File(FileBase):
    pass
