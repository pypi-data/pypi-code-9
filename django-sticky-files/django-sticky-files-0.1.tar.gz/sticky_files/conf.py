# coding: utf-8

from django.conf import settings


FILE_MODEL = getattr(settings, 'STICKY_FILE_MODEL', 'sticky_files.File')
IMAGE_MODEL = getattr(settings, 'STICKY_IMAGE_MODEL', 'sticky_files.File')
