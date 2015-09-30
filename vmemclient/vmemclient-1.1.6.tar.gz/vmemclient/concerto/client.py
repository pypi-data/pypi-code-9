#!/usr/bin/env python

"""
Copyright 2014 - 2015 Violin Memory, Inc..

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from vmemclient.core import restobject
from vmemclient.core.error import *


class ClientManager01(restobject.SessionNamespace):
    _CLIENT_BASE_PATH = '/client/sanclient'
    _ISCSI_TARGET_BASE_PATH = '/client/iscsitarget'

    def get_clients(self, name=None):
        """Gets the clients available.

        Returns:
            list of dicts

        Raises:
            QueryError

        """
        if name is None:
            filters = {}
        else:
            filters = {
                'filters': [
                    {
                        'name': 'name',
                        'operator': '=',
                        'value': str(name),
                    },
                ],
            }

        ans = self.parent.basic.get(self._CLIENT_BASE_PATH, filters)
        if not ans['success']:
            raise QueryError('Failed to get client listing')

        try:
            return [x for x in ans['data']['san_clients'] if x['object_id']]
        except (KeyError, AttributeError):
            return []

    def client_name_to_object_id(self, name):
        """Finds the object_id for the given client name.

        Arguments:
            name -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        name = str(name)

        # Raises:  QueryError
        ans = self.get_clients(name)

        if len(ans) == 0:
            raise NoMatchingObjectIdError(name)
        elif len(ans) == 1:
            return ans[0]['object_id']
        else:
            raise MultipleMatchingObjectIdsError(
                    ', '.join(x['object_id'] for x in ans))

    def get_client_info(self, name=None, object_id=None):
        """Gets detailed info on the specified client object_id.

        Arguments:
            name      -- string
            object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Determine the object_id
        if not object_id:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.client_name_to_object_id(name)

        # Get the client info
        location = '{0}/{1}'.format(self._CLIENT_BASE_PATH, object_id)
        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

    def update_client_basic_info(self, name=None, ip=None, client_os=None,
                                 clustered=None, reserved=None,
                                 object_id=None):
        """Update client basic information.

        Arguments:
            name      -- string
            ip        -- string
            client_os -- string
            clustered -- bool
            reserved  -- bool
            object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'

        # Get the object_id
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.client_name_to_object_id(name)

        # Build the request
        location = '{0}/{1}'.format(self._CLIENT_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'object_id', object_id, 'str'),)
        args += (((BASE_KEY,), 'action', 'update', 'str'),)
        args += (((BASE_KEY,), 'ipAddress', ip, 'str'),)
        args += (((BASE_KEY,), 'OSType', client_os, 'str'),)
        args += (((BASE_KEY,), 'clustered', clustered, 'bool'),)
        args += (((BASE_KEY,), 'reserved', reserved, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def update_client_iscsi_info(self, name=None, iscsi_iqns=None,
                                 iscsi_enable_authentication=None,
                                 iscsi_users=None, iscsi_default_user=None,
                                 iscsi_secret=None,
                                 iscsi_enable_mutual_chap=None,
                                 iscsi_mutual_chap_user=None,
                                 iscsi_mutual_chap_secret=None,
                                 object_id=None,
                                ):
        """Update client iSCSI information.

        Arguments:
            name
            iscsi_iqns                  -- string/list
            iscsi_enable_authentication -- bool
            iscsi_users                 -- string/list
            iscsi_default_user          -- string
            iscsi_secret                -- string
            iscsi_enable_mutual_chap    -- bool
            iscsi_mutual_chap_user      -- string
            iscsi_mutual_chap_secret    -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'
        AUTH_KEY = 'authentication'
        CHAP_KEY = 'mutualCHAP'

        # Find the client as it exists right now
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.client_name_to_object_id(name)

        # Build up submit data
        location = '{0}/{1}'.format(self._CLIENT_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'object_id', object_id, 'str'),)
        args += (((BASE_KEY,), 'action', 'updateiSCSI', 'str'),)
        args += (((BASE_KEY,), 'initiators', iscsi_iqns, 'csvstr'),)
        args += (((BASE_KEY, AUTH_KEY),
                    'enabled', iscsi_enable_authentication, 'bool'),)
        args += (((BASE_KEY, AUTH_KEY), 'users', iscsi_users, 'csvstr'),)
        args += (((BASE_KEY, AUTH_KEY),
                    'defaultUser', iscsi_default_user, 'str'),)
        args += (((BASE_KEY, AUTH_KEY), 'secret', iscsi_secret, 'bool'),)
        args += (((BASE_KEY, AUTH_KEY, CHAP_KEY),
                    'enabled', iscsi_enable_mutual_chap, 'bool'),)
        args += (((BASE_KEY, AUTH_KEY, CHAP_KEY),
                    'user', iscsi_mutual_chap_user, 'str'),)
        args += (((BASE_KEY, AUTH_KEY, CHAP_KEY),
                    'secret', iscsi_mutual_chap_secret, 'str'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def update_client_fc_info(self, name=None, fc_wwns=None, fc_vsa=None,
                              fc_as400=None, object_id=None):
        """Update client FC information.

        Arguments:
            name      -- string
            fc_wwns   -- string/list
            fc_vsa    -- bool
            fc_as400  -- bool
            object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'

        # Find the client as it exists right now
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.client_name_to_object_id(name)

        # Build up submit data
        location = '{0}/{1}'.format(self._CLIENT_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'object_id', object_id, 'str'),)
        args += (((BASE_KEY,), 'action', 'updateFC', 'str'),)
        args += (((BASE_KEY,), 'initiatorWWPNList', fc_wwns, 'csvstr'),)
        args += (((BASE_KEY,), 'VSAenabled', fc_vsa, 'bool'),)
        args += (((BASE_KEY,), 'AS400enabled', fc_as400, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def create_client(self, name=None, proto=None, ip=None, client_os=None,
                      clustered=None, reserved=None,
                      fc_wwns=None, fc_vsa=None, fc_as400=None,
                      iscsi_iqns=None, iscsi_enable_authentication=None,
                      iscsi_users=None, iscsi_default_user=None,
                      iscsi_secret=None, iscsi_enable_mutual_chap=None,
                      iscsi_mutual_chap_user=None,
                      iscsi_mutual_chap_secret=None):
        """Creates a client.

        Arguments:
            name                        -- string
            proto                       -- string/list
            ip                          -- string
            client_os                   -- string
            clustered                   -- bool
            reserved                    -- bool
            fc_wwns                     -- string/list
            fc_vsa                      -- bool
            fc_as400                    -- bool
            iscsi_iqns                  -- string/list
            iscsi_enable_authentication -- bool
            iscsi_users                 -- string/list
            iscsi_default_user          -- string
            iscsi_secret                -- string
            iscsi_enable_mutual_chap    -- bool
            iscsi_mutual_chap_user      -- string
            iscsi_mutual_chap_secret    -- string

        Returns:
            dict

        """
        # Constants
        BASE_KEY = 'params'
        FC_KEY = 'FCPolicy'
        ISCSI_KEY = 'iSCSIPolicy'
        ISCSI_AUTH_KEY = 'authentication'
        MCHAP_KEY = 'mutualCHAP'

        # Build up submit data
        args = ()
        args += (((BASE_KEY,), 'name', name, 'str'),)
        args += (((BASE_KEY,), 'protocolType', proto, 'csvstr'),)
        args += (((BASE_KEY,), 'ipAddress', ip, 'str'),)
        args += (((BASE_KEY,), 'OSType', client_os, 'str'),)
        args += (((BASE_KEY,), 'clustered', clustered, 'bool'),)
        args += (((BASE_KEY,), 'reserved', reserved, 'bool'),)
        args += (((BASE_KEY, FC_KEY), 'initiatorWWPNList', fc_wwns, 'csvstr'),)
        args += (((BASE_KEY, FC_KEY), 'VSAenabled', fc_vsa, 'bool'),)
        args += (((BASE_KEY, FC_KEY), 'AS400enabled', fc_as400, 'bool'),)
        args += (((BASE_KEY, ISCSI_KEY), 'initiators', iscsi_iqns, 'csvstr'),)
        args += (((BASE_KEY, ISCSI_KEY, ISCSI_AUTH_KEY),
                    'enabled', iscsi_enable_authentication, 'bool'),)
        args += (((BASE_KEY, ISCSI_KEY, ISCSI_AUTH_KEY),
                    'users', iscsi_users, 'csvstr'),)
        args += (((BASE_KEY, ISCSI_KEY, ISCSI_AUTH_KEY),
                    'defaultUser', iscsi_default_user, 'str'),)
        args += (((BASE_KEY, ISCSI_KEY, ISCSI_AUTH_KEY),
                    'secret', iscsi_secret, 'str'),)
        args += (((BASE_KEY, ISCSI_KEY, ISCSI_AUTH_KEY, MCHAP_KEY),
                    'enabled', iscsi_enable_mutual_chap, 'bool'),)
        args += (((BASE_KEY, ISCSI_KEY, ISCSI_AUTH_KEY, MCHAP_KEY),
                    'user', iscsi_mutual_chap_user, 'str'),)
        args += (((BASE_KEY, ISCSI_KEY, ISCSI_AUTH_KEY, MCHAP_KEY),
                    'secret', iscsi_mutual_chap_secret, 'str'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.post(self._CLIENT_BASE_PATH, data)

    def delete_client(self, name=None, object_id=None):
        """Deletes the specified client.

        If the object_id is given, use that.  Otherwise, use the client name
        to find the appropriate object_id.

        Arguments:
            name      -- string
            object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Determine object_id
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.client_name_to_object_id(name)

        # Send request
        location = '{0}/{1}'.format(self._CLIENT_BASE_PATH, object_id)
        return self.parent.basic.delete(location)

    def get_iscsi_targets(self, name=None):
        """Gets the iSCSI targets.

        Arguments:
            name -- string

        Returns:
            list of dicts

        Raises:
            QueryError

        """
        location = self._ISCSI_TARGET_BASE_PATH
        if name is None:
            filters = {}
        else:
            filters = {
                'filters': [{
                    'name': 'name',
                    'operator': '=',
                    'value': str(name)}]}

        ans = self.parent.basic.get(location, filters)
        if not ans['success']:
            raise QueryError(ans['msg'])

        try:
            return [x for x in ans['data']['iscsitargets'] if x['object_id']]
        except (KeyError, AttributeError):
            return []

    def iscsi_target_name_to_object_id(self, name):
        """Finds the object_id for the given iscsi target name.

        Arguments:
            name -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        name = str(name)
        ans = self.get_iscsi_targets(name)

        if len(ans) == 0:
            raise NoMatchingObjectIdError(name)
        elif len(ans) == 1:
            return ans[0]['object_id']
        else:
            raise MultipleMatchingObjectIdsError(
                    ', '.join(x['object_id'] for x in ans))

    def create_iscsi_target(self, name=None, client_name=None, ip=None,
                            access_mode=None, starting_lun=None,
                            infiniband=None, client_id=None):
        """Creates an iSCSI target for the specified client.

        Arguments:
            name         -- string
            client_name  -- string
            ip           -- string/list
            access_mode  -- string
            starting_lun -- int
            infiniband   -- bool
            client_id    -- int

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'

        # Determine ids
        if client_id is None:
            info = self.get_client_info(client_name)
            client_id = info['sanclient_id']

        # Build up submit data
        location = self._ISCSI_TARGET_BASE_PATH
        args = ()
        args += (((BASE_KEY,), 'clientId', client_id, 'int'),)
        args += (((BASE_KEY,), 'targetName', name, 'str'),)
        args += (((BASE_KEY,), 'ipAddress', ip, 'ssvstr'),)
        args += (((BASE_KEY,), 'accessMode', access_mode, 'str'),)
        args += (((BASE_KEY,), 'startingLun', starting_lun, 'int'),)
        args += (((BASE_KEY,), 'infiniband', infiniband, 'bool'),)
        data = self.parent.build_request_data(args)

        # Submit request
        return self.parent.basic.post(location, data)
