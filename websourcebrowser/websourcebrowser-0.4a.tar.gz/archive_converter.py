# encoding: UTF-8
# Copyright (C) 2009-2010, Stefan Schwarzer

"""
File converters for archive files like tar or zip files.
"""

import cgi
import tarfile
import zipfile


def tar_file(doc):
    # FIXME add error handling
    tar_file_ = tarfile.open(doc.path)
    names = [cgi.escape(name) for name in tar_file_.getnames()]
    doc.html = u"<br />".join(names)
    doc.mime_type = "text/html"
    return doc
    
def zip_file(doc):
    # FIXME add error handling
    zip_file_ = zipfile.ZipFile(doc.path)
    names = [cgi.escape(name) for name in zip_file_.namelist()]
    doc.html = u"<br />".join(names)
    doc.mime_type = "text/html"
    return doc
