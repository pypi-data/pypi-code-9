# encoding: utf-8

from django.utils.version import get_version


if get_version() < (1, 7, 0):
    from semantic_ui.patch import patch_all
    patch_all()
