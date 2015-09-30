#!/usr/bin/env python

"""
Copyright 2015 Violin Memory, Inc..

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


class ReplicationManager01(restobject.SessionNamespace):
    _REPLICATION_BASE_PATH = '/logicalresource/replication'

    def create_replication_target(self, server=None, server_ip=None, server_username=None, server_password=None, target_device_object_id=None, target_device_name=None, target_device_size=None, target_device_thin=None, target_device_dedup=None, target_device_storage_pool_id=None, target_device_disable_mirror=None, transfer_continuous=None, transfer_sync_replica_timemark=None, transfer_create_primary_timemark=None, transfer_use_existing_timemark=None, transfer_preserve_replication_timemark=None, trigger_initial_time=None, trigger_interval=None, trigger_watermark_mb=None, trigger_watermark_retry=None, cdr_size_mb=None, cdr_storage_pool_id=None, policy_compression=None, policy_enable_encryption=None, policy_encryption_option=None, policy_microscan=None):

        # Constants
        BASE_KEY = 'params'
        SERVER_KEY = 'targetServer'
        DEVICE_KEY = 'targetDevice'
        THIN_KEY = 'thinProvisioning'
        TRANSFER_KEY = 'transferMode'
        TRIGGER_KEY = 'trigger'
        CDR_KEY = 'CDR'
        POLICY_KEY = 'policy'
        ENCRYPTION_KEY = 'encryption'

        # Build request
        foo = None
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY, SERVER_KEY), 'serverName', server, 'str'),)
        args += (((BASE_KEY, SERVER_KEY), 'ipaddress', server_ip, 'str'),)
        args += (((BASE_KEY, SERVER_KEY), 'username', server_username, 'str'),)
        args += (((BASE_KEY, SERVER_KEY), 'password', server_password, 'str'),)
        args += (((BASE_KEY, DEVICE_KEY), 'object_id', target_device_object_id, 'str'),)
        args += (((BASE_KEY, DEVICE_KEY), 'name', target_device_name, 'str'),)
        args += (((BASE_KEY, DEVICE_KEY), 'sizeMB', target_device_size, 'int'),)
        args += (((BASE_KEY, DEVICE_KEY, THIN_KEY), 'enabled', target_device_thin, 'bool'),)
        args += (((BASE_KEY, DEVICE_KEY), 'dedup', target_device_dedup, 'bool'),)
        args += (((BASE_KEY, DEVICE_KEY), 'storagepoolID', target_device_storage_pool_id, 'int'),)
        args += (((BASE_KEY, DEVICE_KEY), 'disableMirror', target_device_disable_mirror, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY), 'continuousMode', transfer_continuous, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY), 'synchronizeReplicaTimemark', transfer_sync_replica_timemark),)
        args += (((BASE_KEY, TRANSFER_KEY), 'createPrimaryTimemark', transfer_create_primary_timemark, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY), 'useExistingTimemark', foo, 'bool'),)
        args += (((BASE_KEY, TRANSFER_KEY), 'preserveReplicationTimemark', foo, 'bool'),)
        args += (((BASE_KEY, TRIGGER_KEY), 'initialTime', foo, 'datetime'),)
        args += (((BASE_KEY, TRIGGER_KEY), 'interval', foo, 'str'),)
        args += (((BASE_KEY, TRIGGER_KEY), 'watermarkMB', foo, 'int'),)
        args += (((BASE_KEY, CDR_KEY), 'sizeMB', foo, 'int'),)
        args += (((BASE_KEY, CDR_KEY), 'storagepoolID', foo, 'int'),)
        args += (((BASE_KEY, POLICY_KEY), 'compression', foo, 'bool'),)
        args += (((BASE_KEY, POLICY_KEY, ENCRYPTION_KEY), 'enabled', foo, 'bool'),)
        args += (((BASE_KEY, POLICY_KEY, ENCRYPTION_KEY), 'option', foo, 'str'),)
        args += (((BASE_KEY, POLICY_KEY), 'microscan', foo, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def _promote_replication_target(self, object_id, force):
        """Internal worker function for:
        """
        # Constants
        BASE_KEY = 'params'

        # Build request
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'action', 'promote', 'str'),)
        args += (((BASE_KEY,), 'force', force, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.put(location, data)

    def promote_replication_lun(self, lun=None, force=None, object_id=None):
        if object_id is None:
            object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._promote_replication_target(object_id, force)

    def _delete_replication_target(self, object_id, force):
        """Internal worker function for:
        """
        # Constants
        BASE_KEY = 'params'

        # Build request
        location = '{0}/{1}'.format(self._REPLICATION_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'force', force, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send request
        return self.parent.basic.delete(location, data)
