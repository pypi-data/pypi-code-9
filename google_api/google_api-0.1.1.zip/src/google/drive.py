#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Google API
# Copyright (C) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Google API.
#
# Hive Google API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Google API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Google API. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import json

import appier

class DriveApi(object):

    def list_drive(self):
        url = self.base_url + "drive/v2/files"
        contents = self.get(url)
        return contents

    def insert_drive(
        self,
        data,
        content_type = "application/octet-stream",
        title = None
    ):
        data = appier.legacy.bytes(data)
        metadata = dict()
        if title: metadata["title"] = title
        metadata_s = json.dumps(metadata)
        is_unicode = appier.legacy.is_unicode(metadata_s)
        if is_unicode: metadata_s = metadata_s.encode("utf-8")
        metadata_p = {
            "Content-Type" : "application/json;charset=utf-8",
            "data" : metadata_s
        }
        media_p = {
            "Content-Type" : content_type,
            "data" : data
        }
        url = self.base_url + "upload/drive/v2/files"
        contents = self.post(
            url,
            params = dict(
                uploadType = "multipart"
            ),
            data_m = dict(file = [metadata_p, media_p]),
            mime = "multipart/related"
        )
        return contents

    def folder_drive(self, title, parent = "root"):
        metadata = dict(
            title = title,
            parents = [dict(id = parent)],
            mimeType = "application/vnd.google-apps.folder"
        )
        metadata_s = json.dumps(metadata)
        is_unicode = appier.legacy.is_unicode(metadata_s)
        if is_unicode: metadata_s = metadata_s.encode("utf-8")
        metadata_p = {
            "Content-Type" : "application/json;charset=utf-8",
            "data" : metadata_s
        }
        url = self.base_url + "upload/drive/v2/files"
        contents = self.post(
            url,
            params = dict(
                uploadType = "multipart"
            ),
            data_m = dict(file = [metadata_p]),
            mime = "multipart/related"
        )
        return contents

    def get_drive(self, id):
        url = self.base_url + "drive/v2/files/%s" % id
        contents = self.get(url)
        return contents

    def children_drive(self, id = "root"):
        url = self.base_url + "drive/v2/files/%s/children" % id
        contents = self.get(url)
        return contents
