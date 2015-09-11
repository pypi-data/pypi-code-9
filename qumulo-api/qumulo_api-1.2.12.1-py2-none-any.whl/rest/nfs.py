# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import qumulo.lib.request as request
import qumulo.lib.obj as obj

class NFSRestriction(obj.Object):
    def __init__(self, d=None):
        super(NFSRestriction, self).__init__(d)

    @classmethod
    def create_default(cls):
        return cls({'read_only': False, 'host_restrictions': [],
                    'user_mapping': 'NFS_MAP_NONE', 'map_to_user_id': '0'})

# Rally US1902: change this to /v1/nfs/shares/*
@request.request
def nfs_list_shares(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/shares/nfs/"

    return request.rest_request(conninfo, credentials, method, uri)

# Rally US1902: change this to /v1/nfs/shares/*
@request.request
def nfs_add_share(conninfo, credentials, export_path, fs_path, description,
                  restrictions, allow_fs_path_create=False):
    method = "POST"
    allow_fs_path_create_ = "true" if allow_fs_path_create else "false"
    uri = "/v1/conf/shares/nfs/?allow-fs-path-create=%s" % allow_fs_path_create_

    share_info = {
        'export_path':       unicode(export_path),
        'fs_path':           unicode(fs_path),
        'description':       unicode(description),
        'restrictions': [r.dictionary() for r in restrictions]
    }

    return request.rest_request(conninfo, credentials, method, uri,
        body=share_info)

# Rally US1902: change this to /v1/nfs/shares/*
@request.request
def nfs_list_share(conninfo, credentials, id_):
    id_ = unicode(id_)

    method = "GET"
    uri = "/v1/conf/shares/nfs/%s" % id_

    return request.rest_request(conninfo, credentials, method, uri)

# Rally US1902: change this to /v1/nfs/shares/*
@request.request
def nfs_modify_share(conninfo, credentials, id_, export_path, fs_path,
                     description, restrictions, allow_fs_path_create=False,
                     if_match=None):
    id_ = unicode(id_)
    allow_fs_path_create_ = "true" if allow_fs_path_create else "false"

    if_match = if_match if if_match is None else unicode(if_match)

    method = "PUT"
    uri = "/v1/conf/shares/nfs/%s?allow-fs-path-create=%s" % \
        (id_, allow_fs_path_create_)

    share_info = {
        'id': id_,
        'export_path':  unicode(export_path),
        'fs_path':      unicode(fs_path),
        'description':  unicode(description),
        'restrictions': [r.dictionary() for r in restrictions]
    }

    return request.rest_request(conninfo, credentials, method, uri,
        body=share_info, if_match=if_match)

# Rally US1902: change this to /v1/nfs/shares/*
@request.request
def nfs_delete_share(conninfo, credentials, id_):
    id_ = unicode(id_)

    method = "DELETE"
    uri = "/v1/conf/shares/nfs/%s" % id_

    return request.rest_request(conninfo, credentials, method, uri)
