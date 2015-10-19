'''
This module contains a factory of data related with SX API functions.

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

from .defaults import FILTER_NAME_TO_UUID
from .exceptions import InvalidAPIFunctionError
from .models import QueryParameters

class QueryDataFactory(object):
    '''
    For a given API function and input parameters return QueryParameters
    object and query body.
    '''

    valid_functions = ('list_users',
                       'list_volumes',
                       'create_user',
                       'modify_user',
                       'remove_user',
                       'list_nodes',
                       'get_node_status',
                       'get_cluster_metadata',
                       'set_cluster_metadata',
                       'locate_volume',
                       'create_volume',
                       'modify_volume',
                       'delete_volume',
                       'mass_delete_files',
                       'get_volume_acl',
                       'update_volume_acl')

    def __call__(self, name, *args, **kwargs):
        if name not in self.valid_functions:
            err_msg = '{} is not a valid API function'.format(repr(name))
            raise InvalidAPIFunctionError(err_msg)
        query_params, body = getattr(self, '_' + name)(*args, **kwargs)
        return query_params, body

    @staticmethod
    def _list_users(clones=None):
        dict_params = {}
        if clones is not None:
            dict_params[u'clones'] = clones
        query_params = QueryParameters(sx_verb='GET',
                                       path_items=['.users'],
                                       bool_params={'desc', 'quota'},
                                       dict_params=dict_params)
        body = {}
        return query_params, body

    @staticmethod
    def _list_volumes(includeMeta=False, includeCustomMeta=False):
        bool_params = {'volumeList'}
        if includeMeta:
            bool_params.add('volumeMeta')
        if includeCustomMeta:
            bool_params.add('customVolumeMeta')
        query_params = QueryParameters(sx_verb='GET',
                                       bool_params=bool_params)
        body = {}
        return query_params, body

    @staticmethod
    def _create_user(userName, userType, userKey, quota=None, desc=None,
            existingName=None):
        query_params = QueryParameters(sx_verb='JOB_PUT',
                                       path_items=['.users'])
        body = {}
        body[u'userName'] = userName
        body[u'userType'] = userType
        body[u'userKey'] = userKey
        if quota is not None:
            body[u'userQuota'] = int(quota)
        if desc is not None:
            body[u'userDesc'] = desc
        if existingName is not None:
            body[u'existingName'] = existingName

        return query_params, body

    @staticmethod
    def _modify_user(userName, userKey=None, quota=None, desc=None):
        query_params = QueryParameters(sx_verb='JOB_PUT',
                                       path_items=['.users', userName])

        body = {}
        if userKey is not None:
            body[u'userKey'] = userKey
        if quota is not None:
            body[u'quota'] = int(quota)
        if desc is not None:
            body[u'desc'] = desc

        return query_params, body

    @staticmethod
    def _remove_user(userName, all=False):
        bool_params = set()
        if all:
            bool_params.add('all')
        query_params = QueryParameters(sx_verb='JOB_DELETE',
                                       path_items=['.users', userName],
                                       bool_params=bool_params)
        body = {}
        return query_params, body

    @staticmethod
    def _list_nodes():
        query_params = QueryParameters(sx_verb='GET',
                                       bool_params={'nodeList'})
        body = {}
        return query_params, body

    @staticmethod
    def _get_node_status():
        query_params = QueryParameters(sx_verb='GET',
                                       path_items=['.status'])
        body = {}
        return query_params, body

    @staticmethod
    def _get_cluster_metadata():
        query_params = QueryParameters(sx_verb='GET',
                                       bool_params={'clusterMeta'})
        body = {}
        return query_params, body

    @staticmethod
    def _set_cluster_metadata(clusterMeta):
        query_params = QueryParameters(sx_verb='JOB_PUT',
                                       path_items=['.clusterMeta'])
        body = {}
        body[u'clusterMeta'] = clusterMeta

        return query_params, body

    @staticmethod
    def _locate_volume(volume, size=None, includeMeta=False,
            includeCustomMeta=False):
        bool_params = set()
        dict_params = {'o': 'locate'}
        if size is not None:
            dict_params['size'] = size
        if includeMeta:
            bool_params.add('volumeMeta')
        if includeCustomMeta:
            bool_params.add('customVolumeMeta')

        query_params = QueryParameters(sx_verb='GET',
                                       path_items=[volume],
                                       bool_params=bool_params,
                                       dict_params=dict_params)
        body = {}
        return query_params, body

    @staticmethod
    def _create_volume(volume, volumeSize, owner, replicaCount,
            maxRevisions=None, volumeMeta=None):
        query_params = QueryParameters(sx_verb='JOB_PUT',
                                       path_items=[volume])
        body = {}
        body[u'volumeSize'] = int(volumeSize)
        body[u'owner'] = owner
        body[u'replicaCount'] = int(replicaCount)
        if maxRevisions is not None:
            body[u'maxRevisions'] = int(maxRevisions)
        if volumeMeta:
            if u'filterActive' in volumeMeta:
                filter_name = volumeMeta[u'filterActive']
                volumeMeta[u'filterActive'] = FILTER_NAME_TO_UUID[filter_name]

            body[u'volumeMeta'] = volumeMeta

        return query_params, body

    @staticmethod
    def _modify_volume(volume, size=None, owner=None, maxRevisions=None,
            customVolumeMeta=None):
        query_params = QueryParameters(sx_verb='JOB_PUT',
                                       path_items=[volume],
                                       dict_params={'o': 'mod'})
        body = {}
        if size is not None:
            body[u'size'] = int(size)
        if owner is not None:
            body[u'owner'] = owner
        if maxRevisions is not None:
            body[u'maxRevisions'] = int(maxRevisions)
        if customVolumeMeta:
            body[u'customVolumeMeta'] = customVolumeMeta
        return query_params, body

    @staticmethod
    def _delete_volume(volume):
        query_params = QueryParameters(sx_verb='JOB_DELETE',
                                       path_items=[volume])
        body = {}
        return query_params, body

    @staticmethod
    def _mass_delete_files(volume):
        query_params = QueryParameters(sx_verb='JOB_DELETE',
                                       path_items=[volume],
                                       bool_params={'recursive'},
                                       dict_params={'filter':''})
        body = {}
        return query_params, body

    @staticmethod
    def _get_volume_acl(volume):
        query_params = QueryParameters(sx_verb='GET',
                                       path_items=[volume],
                                       bool_params={'manager'},
                                       dict_params={'o': 'acl'})
        body = {}
        return query_params, body

    @staticmethod
    def _update_volume_acl(volume, actions):
        query_params = QueryParameters(sx_verb='JOB_PUT',
                                       path_items=[volume],
                                       dict_params={'o': 'acl'})
        body = actions
        return query_params, body
