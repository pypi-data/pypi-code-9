# encoding: UTF-8
# Copyright (C) 2009-2010, Stefan Schwarzer

"""
Converter for image data. (See `converter.py` for more.)
"""

import coding
import config
import urlpath


def html(doc):
    """Return HTML code to embed an image."""
    image_path = doc.path
    image_url = coding.encode_uri(urlpath.to_url(image_path, config.root))
    url = "/image%s" % image_url
    doc.html = u'<img src="%s" />' % url
    doc.mime_type = u"text/html"
    return doc
