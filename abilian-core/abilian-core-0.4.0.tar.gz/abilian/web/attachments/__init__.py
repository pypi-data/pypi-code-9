# coding=utf-8
"""
"""
from __future__ import absolute_import


from .forms import AttachmentForm
from .extension import AttachmentExtension, AttachmentsManager

def register_plugin(app):
  AttachmentExtension(app=app)
