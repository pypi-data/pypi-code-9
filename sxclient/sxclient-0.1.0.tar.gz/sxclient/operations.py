'''
This module contains operation functions; when ran, every function makes
a number of queries in order to complete an operation (e.g. remove a volume
or get node's status) and returns the content of the final response.

Every function designed for the end-user requires a fixed set of arguments:
    - cluster -- a Cluster data structure containing cluster's localization
      data
    - session -- a ClusterSession object

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

from collections import defaultdict
from itertools import product

from requests.compat import urlparse

from .exceptions import SXClusterNonFatalError
from .queries import QueryHandler
from .querydata import QueryDataFactory
from .utils import dict_of_lists_to_tuples

__all__ = ('listUsers',
           'listVolumes',
           'createUser',
           'modifyUser',
           'removeUser',
           'listNodes',
           'getNodeStatus',
           'getClusterMetadata',
           'setClusterMetadata',
           'locateVolume',
           'createVolume',
           'modifyVolume',
           'deleteVolume',
           'getVolumeACL',
           'setVolumeACL',
           'updateVolumeACL')


def listUsers(cluster, session, clones=None):
    '''
    List all users in the cluster, along with additional information.

    Required access: admin.

    Query-specific parameters:
      - clones -- if not None, list only the clones of the user named by the
        parameter value
    '''
    response = _run_cluster_operation('list_users', cluster, session, clones)
    return response.json()

def listVolumes(cluster, session, includeMeta=False, includeCustomMeta=False):
    '''
    List all volumes accessible by the user in the cluster.

    Required access: normal.

    Query-specific parameters:
      - includeMeta -- if True, additionally request volumes' metadata
      - includeCustomMeta -- if True, additionally request volumes' custom
        metadata
    '''
    response = _run_cluster_operation('list_volumes', cluster, session,
        includeMeta, includeCustomMeta)
    return response.json()

def createUser(cluster, session, userName, userType, userKey, quota=None,
        desc=None, existingName=None):
    '''
    Create a new cluster user.

    Required access: admin.

    Query-specific parameters:
      - userName -- name of the user to be created
      - userType -- role of the user (either "normal" or "admin")
      - userKey -- lowercase hex encoded 20 byte user key
      - quota -- quota for all volume sized owned by the user; if 0 or
        None, quota is unlimited
      - desc -- description of the user; if None, it is set to an empty
        string
      - existingName -- name of an existing user to create a clone of; if None,
        a new user will be created
    '''
    response = _run_cluster_operation('create_user', cluster, session,
        userName, userType, userKey, quota, desc, existingName)
    return response.json()

def modifyUser(cluster, session, userName, userKey=None, quota=None,
        desc=None):
    '''
    Update properties of an existing user.

    Required access: normal (own key) / admin (any property)

    Query-specific parameters:
      - userName -- name of the user whose key is to be changed
      - userKey -- new lowercase hex encoded 20 byte user key; if None, user
        key will not be changed
      - quota -- new user quota; if set to 0, the quota will be unlimited; if
        None, quota will not be changed
      - desc -- new user description; if None, description will not be changed

    Note: at least one of userKey, quota, desc has to be provided and not be
    None for the query to succeed.
    '''
    response = _run_cluster_operation('modify_user', cluster, session,
        userName, userKey, quota, desc)
    return response.json()

def removeUser(cluster, session, userName, all=False):
    '''
    Remove an existing cluster user.

    Required access: admin.

    Query-specific parameters:
      - userName -- name of the user to be deleted
      - all -- if set to True, additionally remove all user's clones
    '''
    response = _run_cluster_operation('remove_user', cluster, session,
        userName, all)
    return response.json()

def listNodes(cluster, session):
    '''
    List the cluster's nodes.

    Required access: normal.
    '''
    response = _run_node_operation('list_nodes', cluster.host, cluster,
        session)
    return response.json()

def getNodeStatus(cluster, session, node_address):
    '''
    Get status information about the node specified by the address.

    Required access: admin.

    Query-specific parameters:
      - node_address -- address of the node to connect to
    '''
    response = _run_node_operation('get_node_status', node_address, cluster,
        session)
    return response.json()

def getClusterMetadata(cluster, session):
    '''
    Get metadata associated with the cluster.

    Required access: normal.
    '''
    response = _run_cluster_operation('get_cluster_metadata', cluster, session)
    return response.json()

def setClusterMetadata(cluster, session, clusterMeta):
    '''
    Set metadata associated with the cluster.

    Required access: admin.

    Query-specific parameters:
      - clusterMeta -- dictionary containing key-value metadata pairs. The
        values have to be hex-encoded.
    '''
    response = _run_cluster_operation('set_cluster_metadata', cluster, session,
        clusterMeta)
    return response.json()

def locateVolume(cluster, session, volume, size=None, includeMeta=False,
        includeCustomMeta=False):
    '''
    List the VolumeNodes -- nodes responsible for a specific volume.
    Optionally, get additional volume-related data.

    Required access: user with any kind of permissions for the volume.

    Query-specific parameters:
      - volume -- name of the volume to locate
      - size -- parameter used to additionally request correct blocksize for a
        file of 'size' size; if None, blocksize will not be provided
      - includeMeta -- if True, additionally request volume's metadata
      - includeCustomMeta -- if True, additionally request volume's custom
        metadata
    '''
    response = _run_cluster_operation('locate_volume', cluster, session,
        volume, size, includeMeta, includeCustomMeta)
    return response.json()

def createVolume(cluster, session, volume, volumeSize, owner, replicaCount,
        maxRevisions=None, volumeMeta=None):
    '''
    Create a new volume.

    Required access: admin.

    Query specific parameters:
      - volume -- name of the volume to create
      - volumeSize -- size of the new volume
      - owner -- owner of the new volume
      - replicaCount -- number of replicas for the new volume
      - maxRevisions -- maximum number of revisions for each file on the
        volume; if True, it is set to 1
      - volumeMeta -- dictionary containing key-value metadata pairs. The
        values have to be hex-encoded -- with one exception, 'filterActive',
        where it has to be a valid filter name. If None or empty, no metadata
        is set for the volume.
    '''
    response = _run_cluster_operation('create_volume', cluster, session,
        volume, volumeSize, owner, replicaCount, maxRevisions, volumeMeta)
    return response.json()

def modifyVolume(cluster, session, volume, size=None, owner=None,
        maxRevisions=None, customVolumeMeta=None):
    '''
    Modify properties of an existing volume.

    Required access: admin.

    Query specific parameters:
        - volume -- name of the volume to modify
        - size -- new size of the volume; if None, size is not changed
        - owner -- new owner of the volume; if None, owner is not changed
        - maxRevisions -- new maximum number of revisions for files on the
          volume; if None, the number is not changed
        - customVolumeMeta -- dictionary containing key-value custom metadata
          pairs. The values have to be hex-encoded. If None or empty, no custom
          metadata is set for the volume.
    '''
    response = _run_cluster_operation('modify_volume', cluster, session,
        volume, size, owner, maxRevisions, customVolumeMeta)
    return response.json()

def deleteVolume(cluster, session, volume, force=False):
    '''
    Remove a volume.

    Required access: admin.

    Query specific parameters:
        - volume -- name of the volume to delete
        - force -- if set to True, mass delete all the files on the volume
          prior to volume deletion

    Note: cluster doesn't let the removal of volumes containing any files. In
    order to forcibly remove such volume, pass True to the 'force' parameter.
    '''
    if force:
        response = _run_cluster_operation('locate_volume', cluster, session,
            volume)
        nodelist = response.json()[u'nodeList']
        _run_nodelist_operation('mass_delete_files', nodelist, cluster,
            session, volume)

    response = _run_cluster_operation('locate_volume', cluster, session,
        volume)
    nodelist = response.json()[u'nodeList']
    response = _run_nodelist_operation('delete_volume', nodelist, cluster,
        session, volume)
    return response.json()

def getVolumeACL(cluster, session, volume):
    '''
    Get volume's access control list.

    Required access: user with any kind of permissions for the volume.

    Query specific parameters:
      - volume -- name of the volume to get ACL of
    '''
    response = _run_cluster_operation('get_volume_acl', cluster, session,
        volume)
    return response.json()

def setVolumeACL(cluster, session, volume, permissions):
    '''
    Set volume's access control list, replacing the permissions for the
    specified users.

    Required access: volume manager.

    Query specific parameters:
      - volume -- name of the volume to change ACL of
      - permissions -- dictionary describing new permission sets for a group of
        users, containing usernames as keys and lists of permission names
        ('read', 'write', 'manager') as values.
    '''
    users = permissions.iterkeys()
    perms = ('read', 'write', 'manager')
    possible_entries = product(users, perms)
    new_entries = set(dict_of_lists_to_tuples(permissions))

    action_tuples = set()
    for entry in possible_entries:
        user, perm = entry
        if entry in new_entries:
            action_tup = ('grant-' + perm, user)
        else:
            action_tup = ('revoke-' + perm, user)
        action_tuples.add(action_tup)

    actions = defaultdict(list)
    for action, user in action_tuples:
        actions[action].append(user)

    resp_content = updateVolumeACL(cluster, session, volume, actions)
    return resp_content

def updateVolumeACL(cluster, session, volume, actions):
    '''
    Update volume's access control list.

    Required access: volume manager.

    Query specific parameters:
      - volume -- name of the volume to change ACL of
      - actions -- dictionary consisting of at least one of 'grant-read',
        'grant-write', 'grant-manager', 'revoke-read', 'revoke-write',
        'revoke-manager' as keys, each having a list of user names as a value.
        Actions described in the dictionary will be applied on top of the
        existing ACL.
    '''
    response = _run_cluster_operation('update_volume_acl', cluster, session,
        volume, actions)
    return response.json()


def _run_cluster_operation(fnname, cluster, session, *args, **kwargs):
    response = _run_node_operation('list_nodes', cluster.host, cluster,
        session)
    nodelist = response.json()[u'nodeList']
    response = _run_nodelist_operation(fnname, nodelist, cluster, session,
        *args, **kwargs)
    return response

def _run_nodelist_operation(fnname, nodelist, cluster, session, *args,
        **kwargs):
    for node in nodelist:
        try:
            response = _run_node_operation(fnname, node, cluster, session,
                *args, **kwargs)
            break
        except SXClusterNonFatalError:
            continue
    else:
        raise
    return response

def _run_node_operation(fnname, addr, cluster, session, *args, **kwargs):
    factory = QueryDataFactory()
    params, body = factory(fnname, *args, **kwargs)
    response = _make_query(addr, cluster, session, params, body)
    return response

def _make_query(addr, cluster, session, params, body):
    query_handler = QueryHandler(addr, cluster, session)
    query_handler.prepare_query(params, body)
    query_handler.make_query()
    return query_handler.response
