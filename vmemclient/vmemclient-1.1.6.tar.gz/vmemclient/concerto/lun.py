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


class LUNManager01(restobject.SessionNamespace):
    _LUN_BASE_PATH = '/logicalresource/sanresource'

    def get_luns(self, name=None):
        """Gets the LUN listing.

        Arguments:
            name -- string

        Returns:
            list of dicts

        Raises:
            QueryError

        """
        LUN_TYPES = set(['SAN', 'SANTimeView'])

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

        ans = self.parent.basic.get(self._LUN_BASE_PATH, filters)
        if not ans['success']:
            raise QueryError('Failed to get LUN listing')

        try:
            return [x for x in ans['data']['virtual_devices']
                    if x['type'] in LUN_TYPES]
        except (KeyError, AttributeError):
            return []

    def lun_name_to_object_id(self, name):
        """Finds the object_id for the given LUN name.

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
        ans = self.get_luns(name)

        if len(ans) == 0:
            raise NoMatchingObjectIdError(name)
        elif len(ans) == 1:
            return ans[0]['object_id']
        else:
            raise MultipleMatchingObjectIdsError(
                ', '.join(x['object_id'] for x in ans),
            )

    def get_lun_info(self, name=None, object_id=None):
        """Gets detailed info on the specified LUN.

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
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.lun_name_to_object_id(name)

        # Get the LUN info
        location = '{0}/{1}'.format(self._LUN_BASE_PATH, object_id)
        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

    def create_lun(self, name=None, size=None, dedup=None,
                   thin=None, full_size=None):
        """Creates a LUN.

        Arguments:
            name      -- string
            size      -- int
            dedup     -- bool
            thin      -- bool (optional)
            full_size -- int (optional)

        Returns:
            dict

        """
        # Constants
        BASE_KEY = 'params'
        THIN_PATH = 'thinProvisioning'

        # Build request
        location = self._LUN_BASE_PATH
        args = ()
        args += (((BASE_KEY,), 'name', name, 'str'),)
        args += (((BASE_KEY,), 'sizeMB', size, 'int'),)
        args += (((BASE_KEY,), 'dedup', dedup, 'bool'),)
        args += (((BASE_KEY, THIN_PATH), 'enabled', thin, 'bool'),)
        args += (((BASE_KEY, THIN_PATH), 'fullSizeMB', full_size, 'int'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.post(location, data)

    def rename_lun(self, name=None, new_name=None, object_id=None):
        """Renames a LUN.

        If the object_id is not given, then find it by finding the LUN with
        the name <name>.

        Arguments:
            name      -- string
            new_name  -- string
            object_id -- string (optional)

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'

        # Determine object_id
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.lun_name_to_object_id(name)

        # Build request
        location = '{0}/{1}'.format(self._LUN_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'action', 'update', 'str'),)
        args += (((BASE_KEY,), 'name', new_name, 'str'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def delete_lun(self, name=None, force=None, object_id=None):
        """Delete's the specified LUN.

        If the object_id is given, use that.  Otherwise, use the LUN name
        to find the appropriate object_id.

        Arguments:
            name      -- string
            force     -- bool
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
            object_id = self.lun_name_to_object_id(name)

        # Send request
        location = '{0}/{1}'.format(self._LUN_BASE_PATH, object_id)
        args = ()
        args += (((), 'force', force, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.delete(location, data)

    def _modify_lun_size_using(self, action, name, size, object_id):
        """Internal function for:

            extend_lun
            add_storage_to_lun

        """
        # Constants
        BASE_KEY = 'params'

        # Determine object_id
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.lun_name_to_object_id(name)

        # Sanitize input
        size = 0 if size is None else int(size)

        # Build the request
        location = '{0}/{1}'.format(self._LUN_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'action', action, 'str'),)
        args += (((BASE_KEY,), 'sizeMB', size, 'int'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def extend_lun(self, name=None, size=None, object_id=None):
        """Extends the LUN by 'size' MB.

        If the object_id is given, use that.  Otherwise, use the LUN name
        to find the appropriate object_id.

        Arguments:
            name      -- string
            size      -- int
            object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._modify_lun_size_using('expand', name, size, object_id)

    def add_storage_to_lun(self, name=None, size=None, object_id=None):
        """Adds 'size' MB to the LUN's allocated size.

        If the object_id is given, use that.  Otherwise, use the LUN name
        to find the appropriate object_id.

        Arguments:
            name      -- string
            size      -- int
            object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._modify_lun_size_using('addstorage', name, size, object_id)

    def assign_lun_to_client(self, lun_name=None, client_name=None,
                             mode=None, lun_id=None,
                             mg_wwn=None, client_wwn=None,
                             lun_object_id=None, client_object_id=None):
        """Exports a LUN to a FC client.

        Arguments:
            lun_name         -- string
            client_name      -- string
            mode             -- string
            lun_id           -- int
            mg_wwn           -- string
            client_wwn       -- string
            lun_object_id    -- string
            client_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'
        FC_KEY = 'FC'
        ID_FIELD = 'sanclient_id'

        # Determine all object IDs
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.lun_name_to_object_id(lun_name)
        if client_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            client_object_id = self.parent.client.client_name_to_object_id(
                    client_name)

        # Build request
        location = '{0}/{1}'.format(self.parent.client._CLIENT_BASE_PATH,
                                    client_object_id)
        args = ()
        args += (((BASE_KEY,), 'action', 'assign', 'str'),)
        args += (((BASE_KEY,), 'virtualDeviceObjectID', lun_object_id, 'str'),)
        args += (((BASE_KEY, FC_KEY,), 'lun', lun_id, 'int'),)
        args += (((BASE_KEY, FC_KEY,), 'initiatorWWPN', client_wwn, 'str'),)
        args += (((BASE_KEY, FC_KEY,), 'targetWWPN', mg_wwn, 'str'),)
        args += (((BASE_KEY, FC_KEY,), 'accessMode', mode, 'str'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def unassign_client_lun(self, lun_name=None, client_name=None,
                            force=None, no_group=None,
                            lun_object_id=None, client_object_id=None):
        """Unexport the LUN from the given client.

        Arguments:
            lun_name         -- string
            client_name      -- string
            force            -- bool
            no_group         -- bool
            lun_object_id    -- string
            client_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'

        # Determine all object IDs
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.lun_name_to_object_id(lun_name)
        if client_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            client_object_id = self.parent.client.client_name_to_object_id(
                    client_name)

        # Build request
        location = '{0}/{1}'.format(self.parent.client._CLIENT_BASE_PATH,
                                    client_object_id)
        args = ()
        args += (((BASE_KEY,), 'action', 'unassign', 'str'),)
        args += (((BASE_KEY,), 'virtualDeviceObjectID', lun_object_id, 'str'),)
        args += (((BASE_KEY,), 'force', force, 'bool'),)
        args += (((BASE_KEY,), 'noGroupClientAssignment', no_group, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def _copy_lun_to_lun(self, source=None, new_destination=None,
                         existing_destination=None,
                         source_object_id=None,
                         existing_destination_object_id=None):
        """Copies a LUN to a LUN.

        Worker function for:
            copy_lun_to_new_lun
            copy_lun_to_existing_lun

        """
        # Constants
        BASE_KEY = 'params'

        # Get object id(s)
        if source_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            source_object_id = self.lun_name_to_object_id(source)
        if (existing_destination_object_id is None
                and existing_destination is not None):
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            existing_destination_object_id = \
                self.lun_name_to_object_id(existing_destination)

        # Build the request
        location = '{0}/{1}'.format(
            self.parent.snapshot._SNAPSHOT_RESOURCE_BASE_PATH,
            source_object_id,
        )
        args = ()
        args += (((BASE_KEY,), 'action', 'copy', 'str'),)
        args += (((BASE_KEY,), 'targetName', new_destination, 'str'),)
        args += (((BASE_KEY,), 'targetVirtualDeviceID',
                    existing_destination_object_id, 'str'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def copy_lun_to_new_lun(self, source=None, destination=None,
                            source_object_id=None):
        """Copies a LUN, creating a new LUN in the process.

        Arguments:
            source           -- string
            destination      -- string
            source_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._copy_lun_to_lun(
            source=source,
            new_destination=destination,
            source_object_id=source_object_id,
        )

    def copy_lun_to_existing_lun(self, source=None, destination=None,
                                 source_object_id=None,
                                 destination_object_id=None):
        """Copies a LUN to a LUN that already exists.

        Arguments:
            source                -- string
            destination           -- string
            source_object_id      -- string
            destination_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._copy_lun_to_lun(
            source=source,
            existing_destination=destination,
            source_object_id=source_object_id,
            existing_destination_object_id=destination_object_id,
        )

    def _copy_snapshot_to_lun(self, source_lun=None,
                              source_snapshot_comment=None,
                              new_destination=None, existing_destination=None,
                              include_data=None, source_lun_object_id=None,
                              snapshot_object_id=None,
                              existing_destination_object_id=None):
        """Copy a snapshot to a LUN.

        Internal worker function for:

            copy_snapshot_to_new_lun
            copy_snapshot_to_existing_lun

        """
        # Constants
        BASE_KEY = 'params'

        # Get object id(s)
        if source_lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            source_lun_object_id = self.lun_name_to_object_id(source_lun)
        if snapshot_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            snapshot_object_id = \
                    self.parent.snapshot.snapshot_comment_to_object_id(
                    source_lun, source_snapshot_comment, source_lun_object_id)
        if (existing_destination_object_id is None
                and existing_destination is not None):
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            existing_destination_object_id = \
                    self.lun_name_to_object_id(existing_destination)

        # Build the request
        location = '{0}/{1}'.format(
            self.parent.snapshot._SNAPSHOT_BASE_PATH,
            snapshot_object_id,
        )
        args = ()
        args += (((BASE_KEY,), 'action', 'copy', 'str'),)
        args += (((BASE_KEY,), 'includeTimeviewData', include_data, 'bool'),)
        args += (((BASE_KEY,), 'targetName', new_destination, 'str'),)
        args += (((BASE_KEY,), 'targetVirtualDeviceID',
                    existing_destination_object_id, 'str'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def copy_snapshot_to_new_lun(self, source_lun=None,
                source_snapshot_comment=None, destination=None,
                include_data=None, source_lun_object_id=None,
                snapshot_object_id=None):
        """Copy a snapshot, creating a new LUN in the process.

        Arguments:
            source_lun              -- string
            source_snapshot_comment -- string
            destination             -- string
            include_data            -- bool
            source_lun_object_id    -- string
            snapshot_object_id      -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._copy_snapshot_to_lun(
            source_lun=source_lun,
            source_snapshot_comment=source_snapshot_comment,
            new_destination=destination,
            include_data=include_data,
            source_lun_object_id=source_lun_object_id,
            snapshot_object_id=snapshot_object_id,
        )

    def copy_snapshot_to_existing_lun(self, source_lun=None,
                source_snapshot_comment=None, destination=None,
                include_data=None, source_lun_object_id=None,
                snapshot_object_id=None, destination_object_id=None):
        """Copy a snapshot to a LUN that already exists.

        Arguments:
            source_lun              -- string
            source_snapshot_comment -- string
            destination             -- string
            include_data            -- bool
            source_lun_object_id    -- string
            snapshot_object_id      -- string
            destination_object_id   -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._copy_snapshot_to_lun(
            source_lun=source_lun,
            source_snapshot_comment=source_snapshot_comment,
            existing_destination=destination,
            include_data=include_data,
            source_lun_object_id=source_lun_object_id,
            snapshot_object_id=snapshot_object_id,
            existing_destination_object_id=destination_object_id,
        )

    def remap_thin_clone(self, thin_clone=None, snapshot_comment=None,
                         target_name=None, thin_clone_object_id=None,
                         snapshot_id=None):
        """Remaps the thin clone to the given snapshot.

        Arguments:
            thin_clone           -- string
            snapshot_comment     -- string
            target_name          -- string
            thin_clone_object_id -- string
            snapshot_id          -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        BASE_KEY = 'params'

        # Get required object_id fields
        if thin_clone_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            thin_clone_object_id = self.lun_name_to_object_id(thin_clone)
        if snapshot_id is None:
            source_info = self.get_lun_info(thin_clone, thin_clone_object_id)
            if source_info['type'] != 'SANTimeView':
                raise ValueError('Remap requires a thin clone LUN')
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            snapshot_id = self.parent.snapshot.snapshot_comment_to_id(
                    source_info['timeview_data_set']['name'],
                    snapshot_comment,
                    source_info['timeview_data_set']['object_id'])

        # Build the request
        location = '{0}/{1}'.format(
                self.parent.snapshot._SNAPSHOT_THIN_CLONE_BASE_PATH,
                thin_clone_object_id)
        args = ()
        args += (((BASE_KEY,), 'action', 'remap', 'str'),)
        args += (((BASE_KEY,), 'timestamp', snapshot_id, 'str'),)
        args += (((BASE_KEY,), 'targetName', target_name, 'str'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def _export_unexport_using_iscsi_target(self, action=None, lun_name=None,
            iscsi_target_name=None, lun_id=None, force=None,
            lun_object_id=None, iscsi_target_object_id=None):
        """Internal worker function for:

            * assign_lun_to_iscsi_target
            * unassign_lun_from_iscsi_target

        """
        # Constants
        BASE_KEY = 'params'

        # Determine all object IDs
        if lun_object_id is None:
            lun_object_id = self.lun_name_to_object_id(lun_name)
        if iscsi_target_object_id is None:
            iscsi_target_object_id =  \
                    self.parent.client.iscsi_target_name_to_object_id(
                    iscsi_target_name)

        # Build request
        location = '{0}/{1}'.format(self.parent.client._ISCSI_TARGET_BASE_PATH,
                                    iscsi_target_object_id)
        args = ()
        args += (((BASE_KEY,), 'action', action, 'str'),)
        args += (((BASE_KEY,), 'virtualDeviceObjectID', lun_object_id, 'str'),)
        args += (((BASE_KEY,), 'lun', lun_id, 'int'),)
        args += (((BASE_KEY,), 'force', force, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def assign_lun_to_iscsi_target(self, lun_name=None, iscsi_target_name=None,
            lun_id=None, lun_object_id=None, iscsi_target_object_id=None):
        """Exports a LUN to an iSCSI target / client.

        Arguments:
            lun_name               -- string
            iscsi_target_name      -- string
            lun_id                 -- int
            lun_object_id          -- string
            iscsi_target_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._export_unexport_using_iscsi_target(
            action='assign',
            lun_name=lun_name,
            iscsi_target_name=iscsi_target_name,
            lun_id=lun_id,
            lun_object_id=lun_object_id,
            iscsi_target_object_id=iscsi_target_object_id)

    def unassign_lun_from_iscsi_target(self, lun_name=None,
            iscsi_target_name=None, force=None,
            lun_object_id=None, iscsi_target_object_id=None):
        """Unexports a LUN from an iSCSI target / client.

        Arguments:
            lun_name               -- string
            iscsi_target_name      -- string
            force                  -- bool
            lun_object_id          -- string
            iscsi_target_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._export_unexport_using_iscsi_target(
            action='unassign',
            lun_name=lun_name,
            iscsi_target_name=iscsi_target_name,
            force=force,
            lun_object_id=lun_object_id,
            iscsi_target_object_id=iscsi_target_object_id)

class LUNManager02(LUNManager01):
    def create_lun(self, name=None, size=None, dedup=None,
                   thin=None, full_size=None,
                   storage_pool=None, storage_pool_id=None):
        """Creates a LUN.

        Arguments:
            name            -- string
            size            -- int
            dedup           -- bool
            thin            -- bool (optional)
            full_size       -- int (optional)
            storage_pool    -- string
            storage_pool_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'
        THIN_PATH = 'thinProvisioning'

        # Determine object_id
        if storage_pool_id is None and storage_pool is not None:
            storage_pool_id = \
                self.parent.pool.storage_pool_name_to_id(storage_pool)

        # Build request
        location = self._LUN_BASE_PATH
        args = ()
        args += (((BASE_KEY,), 'name', name, 'str'),)
        args += (((BASE_KEY,), 'sizeMB', size, 'int'),)
        args += (((BASE_KEY,), 'dedup', dedup, 'bool'),)
        args += (((BASE_KEY,), 'storagepoolID', storage_pool_id, 'int'),)
        args += (((BASE_KEY, THIN_PATH), 'enabled', thin, 'bool'),)
        args += (((BASE_KEY, THIN_PATH), 'fullSizeMB', full_size, 'int'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.post(location, data)

    def _copy_lun_to_lun(self, source=None, new_destination=None,
                         existing_destination=None, storage_pool=None,
                         source_object_id=None,
                         existing_destination_object_id=None,
                         storage_pool_id=None):
        """Copies a LUN to a LUN.

        Worker function for:
            copy_lun_to_new_lun
            copy_lun_to_existing_lun

        """
        # Constants
        BASE_KEY = 'params'

        # Get object id(s)
        if source_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            source_object_id = self.lun_name_to_object_id(source)
        if (existing_destination_object_id is None
                and existing_destination is not None):
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            existing_destination_object_id = \
                self.lun_name_to_object_id(existing_destination)
        if storage_pool_id is None and storage_pool is not None:
            storage_pool_id = \
                self.parent.pool.storage_pool_name_to_id(storage_pool)

        # Build the request
        location = '{0}/{1}'.format(
            self.parent.snapshot._SNAPSHOT_RESOURCE_BASE_PATH,
            source_object_id,
        )
        args = ()
        args += (((BASE_KEY,), 'action', 'copy', 'str'),)
        args += (((BASE_KEY,), 'targetName', new_destination, 'str'),)
        args += (((BASE_KEY,), 'targetVirtualDeviceID',
                    existing_destination_object_id, 'str'),)
        args += (((BASE_KEY,), 'storagepoolID', storage_pool_id, 'int'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def copy_lun_to_new_lun(self, source=None, destination=None,
                            storage_pool=None, source_object_id=None,
                            storage_pool_id=None):
        """Copies a LUN, creating a new LUN in the process.

        Arguments:
            source           -- string
            destination      -- string
            storage_pool     -- string
            source_object_id -- string
            storage_pool_id  -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._copy_lun_to_lun(
            source=source,
            new_destination=destination,
            storage_pool=storage_pool,
            source_object_id=source_object_id,
            storage_pool_id=storage_pool_id,
        )

    def _copy_snapshot_to_lun(self, source_lun=None,
                              source_snapshot_comment=None,
                              new_destination=None, existing_destination=None,
                              include_data=None, storage_pool=None,
                              source_lun_object_id=None,
                              snapshot_object_id=None,
                              existing_destination_object_id=None,
                              storage_pool_id=None):
        """Copy a snapshot to a LUN.

        Internal worker function for:

            copy_snapshot_to_new_lun
            copy_snapshot_to_existing_lun

        """
        # Constants
        BASE_KEY = 'params'

        # Get object id(s)
        if source_lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            source_lun_object_id = self.lun_name_to_object_id(source_lun)
        if snapshot_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            snapshot_object_id = \
                    self.parent.snapshot.snapshot_comment_to_object_id(
                    source_lun, source_snapshot_comment, source_lun_object_id)
        if (existing_destination_object_id is None
                and existing_destination is not None):
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            existing_destination_object_id = \
                    self.lun_name_to_object_id(existing_destination)
        if storage_pool_id is None and storage_pool is not None:
            storage_pool_id = \
                self.parent.pool.storage_pool_name_to_id(storage_pool)

        # Build the request
        location = '{0}/{1}'.format(
            self.parent.snapshot._SNAPSHOT_BASE_PATH,
            snapshot_object_id,
        )
        args = ()
        args += (((BASE_KEY,), 'action', 'copy', 'str'),)
        args += (((BASE_KEY,), 'includeTimeviewData', include_data, 'bool'),)
        args += (((BASE_KEY,), 'targetName', new_destination, 'str'),)
        args += (((BASE_KEY,), 'targetVirtualDeviceID',
                    existing_destination_object_id, 'str'),)
        args += (((BASE_KEY,), 'storagepoolID', storage_pool_id, 'int'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def copy_snapshot_to_new_lun(self, source_lun=None,
                source_snapshot_comment=None, destination=None,
                include_data=None, storage_pool=None,
                source_lun_object_id=None,
                snapshot_object_id=None, storage_pool_id=None):
        """Copy a snapshot, creating a new LUN in the process.

        Arguments:
            source_lun              -- string
            source_snapshot_comment -- string
            destination             -- string
            include_data            -- bool
            storage_pool            -- string
            source_lun_object_id    -- string
            snapshot_object_id      -- string
            storage_pool_id         -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._copy_snapshot_to_lun(
            source_lun=source_lun,
            source_snapshot_comment=source_snapshot_comment,
            new_destination=destination,
            include_data=include_data,
            storage_pool=storage_pool,
            source_lun_object_id=source_lun_object_id,
            snapshot_object_id=snapshot_object_id,
            storage_pool_id=storage_pool_id,
        )

    def get_lun_copy_status(self, name=None, object_id=None):
        """
        Gets the status of a "copy LUN to LUN" operation.

        The return value for this function is a three element tuple of:
            * destination object_id (basestring or None)
            * MB copied (int or None)
            * percentage (int)

        Parameters:
            name      -- string
            object_id -- string

        Returns:
            tuple

        """
        # Variables
        destination_object_id = None
        mb_copied = None
        percentage = 0

        # Determine the object_id
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.parent.lun.lun_name_to_object_id(name)

        location = '{0}/{1}'.format(
            self.parent.snapshot._SNAPSHOT_RESOURCE_BASE_PATH,
            object_id,
        )

        # Submit the query
        ans = self.parent.basic.get(
            location,
            get_params={'type': 'copystatus'},
        )

        # We get a basestring back in a few different cases:
        #   * the LUN object_id doesn't exist
        #   * the start-up period where a copy status returns nothing
        #   * if the LUN exists but never had a snapshot copied to it
        if isinstance(ans, dict):
            status = ans['snapcopy_status']
            destination_object_id = status['new_object_id']
            if status['data_copied_(mb)'] == 'finished(100%)':
                percentage = 100
            else:
                mb_copied, percentage = status['data_copied_(mb)'].split()
                mb_copied = int(mb_copied)
                percentage = int(percentage[1:-2])

        # Done
        return (destination_object_id, mb_copied, percentage)
