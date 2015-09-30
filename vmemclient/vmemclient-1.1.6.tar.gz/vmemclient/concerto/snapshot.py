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


class SnapshotManager01(restobject.SessionNamespace):
    _SNAPSHOT_BASE_PATH = '/logicalresource/timemark'
    _SNAPSHOT_POLICY_BASE_PATH = '/logicalresource/timemarkpolicy'
    _SNAPSHOT_RESOURCE_BASE_PATH = '/logicalresource/snapshotresource'
    _SNAPSHOT_THIN_CLONE_BASE_PATH = '/logicalresource/timeview'

    def get_snapshot_resource_info(self, lun=None, lun_object_id=None):
        """Gets info about the given LUN's snapshot resource.

        Arguments:
            lun           -- string
            lun_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        # Get the snapshot resource info
        location = '{0}/{1}'.format(self._SNAPSHOT_RESOURCE_BASE_PATH,
                                    lun_object_id)
        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

    def get_snapshot_policy_info(self, lun=None, lun_object_id=None):
        """Gets the snapshot policy info for the given LUN.

        Arguments:
            lun           -- string
            lun_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        # Get the snapshot policy info
        location = '{0}/{1}'.format(self._SNAPSHOT_POLICY_BASE_PATH,
                                    lun_object_id)
        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

    def get_snapshots(self, lun=None, comment=None, lun_object_id=None):
        """Returns a list of snapshots for the given LUN.

        Arguments:
            lun           -- string
            comment       -- string
            lun_object_id -- string

        Returns:
            list

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Determine the object_id
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        # Get the snapshots
        location = '{0}/{1}'.format(self._SNAPSHOT_BASE_PATH, lun_object_id)
        try:
            ans = self.parent.basic.get(location)
        except MissingParameterError:
            if not self.lun_has_a_snapshot_policy(lun_object_id=lun_object_id):
                # MissingParameterError is raised when no snapshot resource
                # policy is defined for the given LUN
                return []
            else:
                # Something else went wrong, reraise the same error
                raise

        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        try:
            if comment is None:
                return [x for x in ans['data']['timemarks'] if x['object_id']]
            else:
                comment = str(comment)
                return [x for x in ans['data']['timemarks']
                        if x['comment'] == comment]
        except (KeyError, AttributeError):
            return []

    def _find_snapshot_and_return_field(self, field, lun,
                                        comment, lun_object_id):
        """Internal function for:

            snapshot_comment_to_object_id
            snapshot_comment_to_id

        """
        # Raises:  QueryError
        ans = self.get_snapshots(lun, comment, lun_object_id)

        if len(ans) == 0:
            raise NoMatchingObjectIdError(str(lun) or lun_object_id)
        elif len(ans) == 1:
            return ans[0][field]
        else:
            raise MultipleMatchingObjectIdsError(
                    ', '.join(x['object_id'] for x in ans))

    def snapshot_comment_to_object_id(self, lun=None, comment=None,
                                      lun_object_id=None):
        """Returns a snapshot's object_id.

        Arguments:
            lun           -- string
            comment       -- string
            lun_object_id -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._find_snapshot_and_return_field(
                    'object_id', lun, comment, lun_object_id)

    def snapshot_comment_to_id(self, lun=None, comment=None,
                               lun_object_id=None):
        """Returns a snapshot's id.

        Arguments:
            lun           -- string
            comment       -- string
            lun_object_id -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._find_snapshot_and_return_field(
                    'id', lun, comment, lun_object_id)

    def get_snapshot_info(self, lun=None, comment=None,
                          lun_object_id=None, snapshot_object_id=None):
        """Gets information about the specified snapshot.

        Arguments:
            lun                -- string
            comment            -- string
            lun_object_id      -- string
            snapshot_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Determine the object_id
        if snapshot_object_id is None:
            # Raises: QueryError, NoMatchingObjectIdError,
            #         MultipleMatchingObjectIdsError
            snapshot_object_id = self.snapshot_comment_to_object_id(
                    lun, comment, lun_object_id)

        location = '{0}/{1}'.format(self._SNAPSHOT_BASE_PATH,
                                    snapshot_object_id)
        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

    def lun_has_a_snapshot_resource(self, lun=None, lun_object_id=None):
        """Returns if a given LUN have a snapshot resource or not.

        Arguments:
            lun           -- string
            lun_object_id -- string

        Returns:
            boolean

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Raises:  QueryError, NoMatchingObjectIdError,
        #          MultipleMatchingObjectIdsError
        info = self.get_snapshot_resource_info(lun, lun_object_id)
        return 'snapshot_resource' in info

    def lun_has_a_snapshot_policy(self, lun=None, lun_object_id=None):
        """Returns if a given LUN have a snapshot policy or not.

        Arguments:
            lun           -- string
            lun_object_id -- string

        Returns:
            boolean

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Raises:  QueryError, NoMatchingObjectIdError,
        #          MultipleMatchingObjectIdsError
        info = self.get_snapshot_resource_info(lun, lun_object_id)
        return info['timemarkEnabled']

    def create_snapshot_resource(self, lun=None, size=None,
                enable_notification=None, policy=None, enable_expansion=None,
                expansion_threshold=None, expansion_increment=None,
                expansion_max_size=None, enable_shrink=None,
                shrink_trigger_size=None, shrink_min_size=None,
                lun_object_id=None):
        """Create a snapshot resource for the given LUN.

        Arguments:
            lun                 -- string
            size                -- int
            enable_notification -- bool
            policy              -- string
            enable_expansion    -- bool
            expansion_threshold -- int
            expansion_increment -- string
            expansion_max_size  -- string
            enable_shrink       -- bool
            shrink_trigger_size -- string
            shrink_min_size     -- string
            lun_object_id       -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'
        EXPANSION_KEY = 'automaticExpansion'
        SHRINK_KEY = 'automaticShrink'

        # Get the LUN's object_id
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        # Build the request
        location = '{0}/{1}'.format(self._SNAPSHOT_RESOURCE_BASE_PATH,
                                    lun_object_id)
        args = ()
        args += (((BASE_KEY,), 'sizeMB', size, 'int'),)
        args += (((BASE_KEY,),
                    'snapshotNotificationEnabled',
                    enable_notification, 'bool'),)
        args += (((BASE_KEY,), 'policy', policy, 'str'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'enabled', enable_expansion, 'bool'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'threshold', expansion_threshold, 'int'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'increment', expansion_increment, 'str'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'maxSizeMB', expansion_max_size, 'str'),)
        args += (((BASE_KEY, SHRINK_KEY,),
                'enabled', enable_shrink, 'bool', True),)
        args += (((BASE_KEY, SHRINK_KEY,),
                'trigger', shrink_trigger_size, 'str'),)
        args += (((BASE_KEY, SHRINK_KEY,),
                'minSize', shrink_min_size, 'str'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.post(location, data)

    def delete_snapshot_resource(self, lun=None, lun_object_id=None):
        """Delete the LUN's snapshot resource.

        Arguments:
            lun           -- string
            lun_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        location = '{0}/{1}'.format(self._SNAPSHOT_RESOURCE_BASE_PATH,
                                    lun_object_id)

        # Send the request
        return self.parent.basic.delete(location)

    def _create_snapshot_policy(self, object_id,
                max_snapshots, enable_replication,
                enable_snapshot_schedule, schedule_start_time,
                schedule_interval, enable_schedule_notification,
                schedule_notification_frequency, enable_cdp,
                cdp_size, cdp_selection_criteria,
                cdp_physical_devices, cdp_storage_pool,
                cdp_performance, enable_cdp_automatic_expansion,
                cdp_expansion_coverage_period,
                cdp_expansion_threshold, cdp_expansion_increment,
                cdp_expansion_max_size, retention_mode,
                retention_most_recent, retention_all,
                retention_hourly, retention_hourly_minute,
                retention_daily, retention_daily_hour,
                retention_weekly, retention_weekly_day,
                retention_monthly, retention_monthly_day,
                cdp_physical_device_ids, cdp_storage_pool_id):
        """
        Internal function for:

            * create_snapshot_policy
            * create_snapgroup_policy

        """
        # Constants
        BASE_KEY = 'params'
        SCHEDULE_KEY = 'automatic'
        SCHEDULE_NOTIFICATION_KEY = 'notificationFrequency'
        CDP_KEY = 'CDPOption'
        CDP_POLICY_KEY = 'policy'
        CDP_EXPANSION_KEY = 'automaticExpansion'
        RETENTION_KEY = 'RetentionPolicy'

        # Get the various object_ids necessary
        if cdp_storage_pool_id is None and cdp_storage_pool:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            cdp_storage_pool_id = \
                    self.parent.pool.storage_pool_name_to_object_id(
                    cdp_storage_pool)

        # Build the request
        location = '{0}/{1}'.format(self._SNAPSHOT_POLICY_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'maxTimeMarkCount', max_snapshots, 'int'),)
        args += (((BASE_KEY,),
                    'triggerReplication', enable_replication, 'bool'),)
        args += (((BASE_KEY, SCHEDULE_KEY),
                    'enabled', enable_snapshot_schedule, 'bool'),)
        args += (((BASE_KEY, SCHEDULE_KEY),
                    'initialTime', schedule_start_time, 'datetime'),)
        args += (((BASE_KEY, SCHEDULE_KEY),
                    'interval', schedule_interval, 'str'),)
        args += (((BASE_KEY, SCHEDULE_KEY, SCHEDULE_NOTIFICATION_KEY),
                    'enabled', enable_schedule_notification, 'bool'),)
        args += (((BASE_KEY, SCHEDULE_KEY, SCHEDULE_NOTIFICATION_KEY),
                    'frequency', schedule_notification_frequency, 'int'),)
        args += (((BASE_KEY, CDP_KEY),
                    'enabled', enable_cdp, 'bool'),)
        args += (((BASE_KEY, CDP_KEY),
                    'sizeMB', cdp_size, 'int'),)
        args += (((BASE_KEY, CDP_KEY),
                    'selectionCriteria', cdp_selection_criteria, 'str'),)
        args += (((BASE_KEY, CDP_KEY),
                    'physicaldevices', cdp_physical_device_ids, 'listofstr'),)
        args += (((BASE_KEY, CDP_KEY),
                    'storagepoolID', cdp_storage_pool_id, 'str'),)
        args += (((BASE_KEY, CDP_KEY, CDP_POLICY_KEY),
                    'performanceLevel', cdp_performance, 'str'),)
        args += (((BASE_KEY, CDP_KEY, CDP_EXPANSION_KEY),
                    'enabled', enable_cdp_automatic_expansion, 'bool'),)
        args += (((BASE_KEY, CDP_KEY, CDP_EXPANSION_KEY),
                    'CDPCoveragePeriod',
                    cdp_expansion_coverage_period, 'str'),)
        args += (((BASE_KEY, CDP_KEY, CDP_EXPANSION_KEY),
                    'threshold', cdp_expansion_threshold, 'str'),)
        args += (((BASE_KEY, CDP_KEY, CDP_EXPANSION_KEY),
                    'increment', cdp_expansion_increment, 'str'),)
        args += (((BASE_KEY, CDP_KEY, CDP_EXPANSION_KEY),
                    'maxSizeMB', cdp_expansion_max_size, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'mode', retention_mode, 'str'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'mostRecent', retention_most_recent, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'retentionAll', retention_all, 'str'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'retentionHourly', retention_hourly, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'closestMinuteForHourly', retention_hourly_minute, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'retentionDaily', retention_daily, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'closestHourForDaily', retention_daily_hour, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'retentionWeekly', retention_weekly, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'closestDayOfWeekForWeekly', retention_weekly_day, 'str'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'retentionMonthly', retention_monthly, 'int'),)
        args += (((BASE_KEY, RETENTION_KEY),
                    'closestDayForMonthly', retention_monthly_day, 'int'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.post(location, data)


    def create_snapshot_policy(self, lun=None,
                max_snapshots=None, enable_replication=None,
                enable_snapshot_schedule=None, schedule_start_time=None,
                schedule_interval=None, enable_schedule_notification=None,
                schedule_notification_frequency=None, enable_cdp=None,
                cdp_size=None, cdp_selection_criteria=None,
                cdp_physical_devices=None, cdp_storage_pool=None,
                cdp_performance=None, enable_cdp_automatic_expansion=None,
                cdp_expansion_coverage_period=None,
                cdp_expansion_threshold=None, cdp_expansion_increment=None,
                cdp_expansion_max_size=None, retention_mode=None,
                retention_most_recent=None, retention_all=None,
                retention_hourly=None, retention_hourly_minute=None,
                retention_daily=None, retention_daily_hour=None,
                retention_weekly=None, retention_weekly_day=None,
                retention_monthly=None, retention_monthly_day=None,
                lun_object_id=None,
                cdp_physical_device_ids=None, cdp_storage_pool_id=None):
        """Create a snapshot policy.

        Arguments:
            lun                             -- string
            max_snapshots                   -- int
            enable_replication              -- bool
            enable_snapshot_schedule        -- bool
            schedule_start_time             -- datetime / string
            schedule_interval               -- string
            enable_schedule_notification    -- bool
            schedule_notification_frequency -- int
            enable_cdp                      -- bool
            cdp_size                        -- int
            cdp_selection_criteria          -- str
            cdp_physical_devices            -- list of strings
            cdp_storage_pool                -- string
            cdp_performance                 -- string
            enable_cdp_automatic_expansion  -- bool
            cdp_expansion_coverage_period   -- string
            cdp_expansion_threshold         -- string
            cdp_expansion_increment         -- string
            cdp_expansion_max_size          -- int
            retention_mode                  -- string
            retention_most_recent           -- int
            retention_all                   -- string
            retention_hourly                -- int
            retention_hourly_minute         -- int
            retention_daily                 -- int
            retention_daily_hour            -- int
            retention_weekly                -- int
            retention_weekly_day            -- str
            retention_monthly               -- int
            retention_monthly_day           -- int
            lun_object_id                   -- string
            cdp_physical_device_ids         -- list
            cdp_storage_pool_id             -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Get the various object_ids necessary
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._create_snapshot_policy(lun_object_id,
                max_snapshots, enable_replication,
                enable_snapshot_schedule, schedule_start_time,
                schedule_interval, enable_schedule_notification,
                schedule_notification_frequency, enable_cdp,
                cdp_size, cdp_selection_criteria,
                cdp_physical_devices, cdp_storage_pool,
                cdp_performance, enable_cdp_automatic_expansion,
                cdp_expansion_coverage_period,
                cdp_expansion_threshold, cdp_expansion_increment,
                cdp_expansion_max_size, retention_mode,
                retention_most_recent, retention_all,
                retention_hourly, retention_hourly_minute,
                retention_daily, retention_daily_hour,
                retention_weekly, retention_weekly_day,
                retention_monthly, retention_monthly_day,
                cdp_physical_device_ids, cdp_storage_pool_id)

    def _delete_snapshot_policy(self, object_id):
        """
        Internal worker function for:

            * delete_snapshot_policy
            * delete_snapgroup_policy

        """
        location = '{0}/{1}'.format(self._SNAPSHOT_POLICY_BASE_PATH, object_id)

        # Send the request
        return self.parent.basic.delete(location)

    def delete_snapshot_policy(self, lun=None, lun_object_id=None):
        """Delete the LUN's snapshot resource.

        Arguments:
            lun           -- string
            lun_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        # Send the request
        return self._delete_snapshot_policy(lun_object_id)

    def _create_snapshot(self, object_id, comment,
                         priority, enable_notification):
        """
        Internal function for:

            * create_lun_snapshot
            * create_snapgroup_snapshot

        """
        # Constants
        BASE_KEY = 'params'

        # Build the request
        location = '{0}/{1}'.format(self._SNAPSHOT_BASE_PATH, object_id)
        args = ()
        args += (((BASE_KEY,), 'comment', comment, 'str'),)
        args += (((BASE_KEY,), 'priority', priority, 'str'),)
        args += (((BASE_KEY,),
                    'snapshotNotification', enable_notification, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.post(location, data)

    def create_lun_snapshot(self, lun=None, comment=None, priority=None,
                        enable_notification=None, lun_object_id=None):
        """Creates a snapshot of the given LUN.

        Arguments:
            lun                 -- string
            comment             -- string
            priority            -- string
            enable_notification -- bool
            lun_object_id       -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Determine the object_id
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        return self._create_snapshot(lun_object_id, comment,
                                     priority, enable_notification)

    def _delete_snapshot(self, object_id):
        """
        Internal worker function for:

            * delete_lun_snapshot
            * delete_snapgroup_snapshot

        """
        location = '{0}/{1}'.format(self._SNAPSHOT_BASE_PATH, object_id)
        return self.parent.basic.delete(location)

    def delete_lun_snapshot(self, lun=None, comment=None,
                        lun_object_id=None, snapshot_object_id=None):
        """Deletes the LUN snapshot.

        Arguments:
            lun                -- string
            comment            -- string
            lun_object_id      -- string
            snapshot_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        if snapshot_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            snapshot_object_id = self.snapshot_comment_to_object_id(
                    lun, comment, lun_object_id)

        return self._delete_snapshot(snapshot_object_id)

    def create_thin_clone(self, lun=None, snapshot_comment=None,
                          name=None, storage_size=None,
                          storage_devices=None, storage_pool=None,
                          enable_expansion=None, expansion_threshold=None,
                          expansion_increment=None, expansion_max_size=None,
                          timeview_copy=None, include_timeview_data=None,
                          lun_object_id=None, snapshot_id=None,
                          storage_pool_object_id=None):
        """Creates a thin clone of a snapshot.

        Arguments:
            lun                    -- string
            snapshot_comment       -- string
            name                   -- string
            storage_size           -- int
            storage_devices        -- list of strings
            storage_pool           -- string
            enable_expansion       -- bool
            expansion_threshold    -- string
            expansion_increment    -- string
            expansion_max_size     -- int
            timeview_copy          -- bool
            include_timeview_data  -- bool
            lun_object_id          -- string
            snapshot_id            -- string
            storage_pool_object_id -- string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'
        STORAGE_KEY = 'storage'
        EXPANSION_KEY = 'automaticExpansion'

        # Get the various object_ids necessary
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)
        if storage_pool_object_id is None and storage_pool is not None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            storage_pool_object_id = \
                    self.parent.pool.storage_pool_name_to_object_id(
                    storage_pool)
        if snapshot_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            snapshot_id = self.snapshot_comment_to_id(
                    lun, snapshot_comment, lun_object_id)

        # Build the request
        location = '{0}/{1}'.format(self._SNAPSHOT_THIN_CLONE_BASE_PATH,
                                    lun_object_id)
        args = ()
        args += (((BASE_KEY,), 'targetName', name, 'str'),)
        args += (((BASE_KEY,), 'timestamp', snapshot_id, 'str'),)
        args += (((BASE_KEY,), 'timeviewCopy', timeview_copy, 'bool'),)
        args += (((BASE_KEY,),
                    'includeTimeviewData', include_timeview_data, 'bool'),)
        args += (((BASE_KEY, STORAGE_KEY), 'sizeMB', storage_size, 'int'),)
        args += (((BASE_KEY, STORAGE_KEY),
                    'physicaldevices', storage_devices, 'listofstr'),)
        args += (((BASE_KEY, STORAGE_KEY),
                    'storagepoolID', storage_pool_object_id, 'str'),)
        args += (((BASE_KEY, EXPANSION_KEY),
                    'enabled', enable_expansion, 'bool'),)
        args += (((BASE_KEY, EXPANSION_KEY),
                    'threshold', expansion_threshold, 'str'),)
        args += (((BASE_KEY, EXPANSION_KEY),
                    'increment', expansion_increment, 'str'),)
        args += (((BASE_KEY, EXPANSION_KEY),
                    'maxSizeMB', expansion_max_size, 'int'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.post(location, data)

    def delete_thin_clone(self, lun=None, snapshot_comment=None,
                          keep_data=None, lun_object_id=None,
                          snapshot_object_id=None, object_id=None):
        """Deletes the specified thin clone.

        Arguments:
            lun                -- string
            snapshot_comment   -- string
            keep_data          -- bool
            lun_object_id      -- string
            snapshot_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'
        THIN_CLONE_OBJECT_ID_KEY = 'timeview_object_id'

        # Get the object_id if necessary
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            info = self.get_snapshot_info(lun, snapshot_comment,
                                          lun_object_id, snapshot_object_id)
            if THIN_CLONE_OBJECT_ID_KEY not in info:
                raise QueryError('No thin clone present')
            else:
                object_id = info[THIN_CLONE_OBJECT_ID_KEY]

        # Build the request
        location = '{0}/{1}'.format(self._SNAPSHOT_THIN_CLONE_BASE_PATH,
                                    object_id)
        args = ()
        args += (((BASE_KEY,), 'keepTimeViewData', keep_data, 'bool'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.delete(location, data)

class SnapshotManager02(SnapshotManager01):
    _SNAPSHOT_GROUP_BASE_PATH = '/logicalresource/snapshotgroup'

    def create_snapshot_resource(self, lun=None, size=None,
                enable_notification=None, policy=None, enable_expansion=None,
                expansion_threshold=None, expansion_increment=None,
                expansion_max_size=None, enable_shrink=None,
                shrink_trigger_size=None, shrink_min_size=None,
                storage_pool=None, lun_object_id=None, storage_pool_id=None):
        """Create a snapshot resource for the given LUN.

        Arguments:
            lun                 -- string
            size                -- int
            enable_notification -- bool
            policy              -- string
            enable_expansion    -- bool
            expansion_threshold -- int
            expansion_increment -- string
            expansion_max_size  -- string
            enable_shrink       -- bool
            shrink_trigger_size -- string
            shrink_min_size     -- string
            storage_pool        -- string
            lun_object_id       -- string
            storage_pool_id     -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        BASE_KEY = 'params'
        EXPANSION_KEY = 'automaticExpansion'
        SHRINK_KEY = 'automaticShrink'

        # Get the LUN's object_id
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)
        if storage_pool_id is None and storage_pool is not None:
            storage_pool_id = \
                self.parent.pool.storage_pool_name_to_id(storage_pool)

        # Build the request
        location = '{0}/{1}'.format(self._SNAPSHOT_RESOURCE_BASE_PATH,
                                    lun_object_id)
        args = ()
        args += (((BASE_KEY,), 'sizeMB', size, 'int'),)
        args += (((BASE_KEY,),
                    'snapshotNotificationEnabled',
                    enable_notification, 'bool'),)
        args += (((BASE_KEY,), 'policy', policy, 'str'),)
        args += (((BASE_KEY,), 'storagepoolID', storage_pool_id, 'int'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'enabled', enable_expansion, 'bool'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'threshold', expansion_threshold, 'int'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'increment', expansion_increment, 'str'),)
        args += (((BASE_KEY, EXPANSION_KEY,),
                'maxSizeMB', expansion_max_size, 'str'),)
        args += (((BASE_KEY, SHRINK_KEY,),
                'enabled', enable_shrink, 'bool', True),)
        args += (((BASE_KEY, SHRINK_KEY,),
                'trigger', shrink_trigger_size, 'str'),)
        args += (((BASE_KEY, SHRINK_KEY,),
                'minSize', shrink_min_size, 'str'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.post(location, data)

    def get_snapshots(self, lun=None, comment=None, lun_object_id=None):
        """Returns a list of snapshots for the given LUN.

        Arguments:
            lun           -- string
            comment       -- string
            lun_object_id -- string

        Returns:
            list

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Determine the object_id
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        filters = {}
        if comment is not None:
            filters['comment'] = str(comment)

        # Get the snapshots
        location = '{0}/{1}'.format(self._SNAPSHOT_BASE_PATH, lun_object_id)
        try:
            ans = self.parent.basic.get(location, filters)
        except MissingParameterError:
            if not self.lun_has_a_snapshot_policy(lun_object_id=lun_object_id):
                # MissingParameterError is raised when no snapshot resource
                # policy is defined for the given LUN
                return []
            else:
                # Something else went wrong, reraise the same error
                raise

        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        try:
            return [x for x in ans['data']['timemarks'] if x['object_id']]
        except (KeyError, AttributeError):
            return []

    def get_snapshot_copy_status(self, lun=None, lun_object_id=None):
        """
        Gets the status of a "copy snapshot to LUN" operation.

        The return value for this function is a three element tuple of:
            * destination virtual device ID (int or None)
            * MB copied (int or None)
            * percentage (int)

        Arguments:
            lun           -- string
            lun_object_id -- string

        Returns:
            tuple

        """
        # Variables
        destination_vdev_id = None
        mb_copied = None
        percentage = 0

        # Determine the object_id
        if lun_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            lun_object_id = self.parent.lun.lun_name_to_object_id(lun)

        location = '{0}/{1}'.format(
            self._SNAPSHOT_BASE_PATH,
            lun_object_id,
        )

        # Submit the query
        ans = self.parent.basic.get(
            location,
            get_params={'type': 'operationstatus'},
        )

        # Leaving the basestring check here just in case
        if isinstance(ans, dict) and ans['success']:
            status = ans['timemark_status']
            # What we get back is a list of strings that needs to be parsed.
            if len(status) > 1:
                destination_vdev_id = int(status[1].split()[9])
                if len(status) == 2:
                    percentage = 100
                else:
                    mb_copied, percentage = status[-1].split()[-2:]
                    mb_copied = int(mb_copied)
                    percentage = int(percentage[1:-2])

        # Done
        return (destination_vdev_id, mb_copied, percentage)

    def _find_snapgroup_snapshot_and_return_field(self, field, group,
            comment, group_object_id):
        """Internal function for:

            snapgroup_snapshot_comment_to_object_id
            snapgroup_snapshot_comment_to_id

        """
        # Raises:  QueryError
        ans = self.get_snapgroup_snapshots(group, comment, group_object_id)

        if len(ans) == 0:
            raise NoMatchingObjectIdError(str(lun) or group_object_id)
        elif len(ans) == 1:
            return ans[0][field]
        else:
            raise MultipleMatchingObjectIdsError(
                    ', '.join(x['object_id'] for x in ans))

    def snapgroup_snapshot_comment_to_object_id(self, group=None, comment=None,
            group_object_id=None):
        """Returns a snapgroup snapshot's object_id.

        Arguments:
            group           -- string
            comment         -- string
            group_object_id -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._find_snapgroup_snapshot_and_return_field(
                    'object_id', group, comment, group_object_id)

    def snapgroup_snapshot_comment_to_id(self, group=None, comment=None,
            group_object_id=None):
        """Returns a snapgroup snapshot's id.

        Arguments:
            group           -- string
            comment         -- string
            group_object_id -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._find_snapgroup_snapshot_and_return_field(
                    'id', group, comment, group_object_id)

    def get_snapgroups(self, name=None):
        """Returns a list of snapshot groups.

        Arguments:
            name -- string

        Returns:
            list

        Raises:
            QueryError

        """
        location = self._SNAPSHOT_GROUP_BASE_PATH
        filters = {}
        if name is not None:
            filters = {
                'filters': [
                    {
                        'name': 'name',
                        'operator': '=',
                        'value': str(name),
                    },
                ],
            }

        # Get the snapshot groups
        ans = self.parent.basic.get(location, filters)
        if not hasattr(ans, 'get'):
            raise QueryError(str(ans))
        elif not ans['success']:
            raise QueryError(ans['msg'])

        try:
            ans = [x for x in ans['data']['snapshot_groups'] if x['object_id']]
        except (KeyError, AttributeError):
            ans = []

        return ans

    def snapgroup_name_to_object_id(self, name):
        """Returns a snapshot group's object_id.

        Arguments:
            name -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        ans = self.get_snapgroups(name)
        if len(ans) == 0:
            raise NoMatchingObjectIdError(str(name))
        elif len(ans) == 1:
            return ans[0]['object_id']
        else:
            raise MultipleMatchingObjectIdsError(
                    ', '.join(x['object_id'] for x in ans))

    def create_snapgroup_policy(self, snapgroup=None,
                max_snapshots=None, enable_replication=None,
                enable_snapshot_schedule=None, schedule_start_time=None,
                schedule_interval=None, enable_schedule_notification=None,
                schedule_notification_frequency=None, enable_cdp=None,
                cdp_size=None, cdp_selection_criteria=None,
                cdp_physical_devices=None, cdp_storage_pool=None,
                cdp_performance=None, enable_cdp_automatic_expansion=None,
                cdp_expansion_coverage_period=None,
                cdp_expansion_threshold=None, cdp_expansion_increment=None,
                cdp_expansion_max_size=None, retention_mode=None,
                retention_most_recent=None, retention_all=None,
                retention_hourly=None, retention_hourly_minute=None,
                retention_daily=None, retention_daily_hour=None,
                retention_weekly=None, retention_weekly_day=None,
                retention_monthly=None, retention_monthly_day=None,
                snapgroup_object_id=None,
                cdp_physical_device_ids=None, cdp_storage_pool_id=None):
        """Create a snapshot policy for a snapshot group.

        Arguments:
            snapgroup                       -- string
            max_snapshots                   -- int
            enable_replication              -- bool
            enable_snapshot_schedule        -- bool
            schedule_start_time             -- datetime / string
            schedule_interval               -- string
            enable_schedule_notification    -- bool
            schedule_notification_frequency -- int
            enable_cdp                      -- bool
            cdp_size                        -- int
            cdp_selection_criteria          -- str
            cdp_physical_devices            -- list of strings
            cdp_storage_pool                -- string
            cdp_performance                 -- string
            enable_cdp_automatic_expansion  -- bool
            cdp_expansion_coverage_period   -- string
            cdp_expansion_threshold         -- string
            cdp_expansion_increment         -- string
            cdp_expansion_max_size          -- int
            retention_mode                  -- string
            retention_most_recent           -- int
            retention_all                   -- string
            retention_hourly                -- int
            retention_hourly_minute         -- int
            retention_daily                 -- int
            retention_daily_hour            -- int
            retention_weekly                -- int
            retention_weekly_day            -- str
            retention_monthly               -- int
            retention_monthly_day           -- int
            snapgroup_object_id             -- string
            cdp_physical_device_ids         -- list
            cdp_storage_pool_id             -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Get the various object_ids necessary
        if snapgroup_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            snapgroup_object_id = self.snapgroup_name_to_object_id(snapgroup)

        return self._create_snapshot_policy(snapgroup_object_id,
                max_snapshots, enable_replication,
                enable_snapshot_schedule, schedule_start_time,
                schedule_interval, enable_schedule_notification,
                schedule_notification_frequency, enable_cdp,
                cdp_size, cdp_selection_criteria,
                cdp_physical_devices, cdp_storage_pool,
                cdp_performance, enable_cdp_automatic_expansion,
                cdp_expansion_coverage_period,
                cdp_expansion_threshold, cdp_expansion_increment,
                cdp_expansion_max_size, retention_mode,
                retention_most_recent, retention_all,
                retention_hourly, retention_hourly_minute,
                retention_daily, retention_daily_hour,
                retention_weekly, retention_weekly_day,
                retention_monthly, retention_monthly_day,
                cdp_physical_device_ids, cdp_storage_pool_id)

    def create_snapgroup(self, name=None):
        """Create a snapshot group.

        Arguments:
            name -- string

        Returns:
            dict

        """
        # Constants
        BASE_KEY = 'params'

        # Build the request
        location = self._SNAPSHOT_GROUP_BASE_PATH
        args = ()
        args += (((BASE_KEY,), 'name', name, 'str'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.post(location, data)

    def get_snapgroup_info(self, name=None, object_id=None):
        """Gets info about the given snapgroup.

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
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.snapgroup_name_to_object_id(name)

        location = '{0}/{1}'.format(self._SNAPSHOT_GROUP_BASE_PATH,
                object_id)

        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans['msg'])

        return ans['data']

    def delete_snapgroup_policy(self, group=None, group_object_id=None):
        """Delete the snapgroup's snapshot resource.

        Arguments:
            group           -- string
            group_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        if group_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            group_object_id = self.snapgroup_name_to_object_id(group)

        # Send the request
        return self._delete_snapshot_policy(group_object_id)

    def _update_luns_in_snapgroup(self, action, snapgroup, luns,
            snapgroup_object_id, lun_object_ids):
        """Internal worker function for:

            * add_luns_to_snapshot_group
            * remove_luns_from_snapshot_group

        """
        # Constants
        BASE_KEY = 'params'

        # Variables
        device_ids = []

        # Perform all object_id lookups
        if snapgroup_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError
            snapgroup_object_id = self.snapgroup_name_to_object_id(snapgroup)
        if isinstance(luns, basestring):
            luns = [luns,]
        if isinstance(luns, list):
            for lun in luns:
                # Raises:  QueryError, NoMatchingObjectIdError,
                #          MultipleMatchingObjectIdsError
                device_ids.append(self.parent.lun.lun_name_to_object_id(lun))
        else:
            raise ValueError(luns)
        device_ids.extend(lun_object_ids)

        # Build the request
        location = '{0}/{1}'.format(self._SNAPSHOT_GROUP_BASE_PATH,
                                    snapgroup_object_id)
        args = ()
        args += (((BASE_KEY,), 'action', action, 'str'),)
        args += (((BASE_KEY,), 'virtualdevices', device_ids, 'listofstr'),)
        data = self.parent.build_request_data(args)

        # Send the request
        return self.parent.basic.put(location, data)

    def add_luns_to_snapgroup(self, snapgroup=None, luns=[],
            snapgroup_object_id=None, lun_object_ids=[]):
        """Add one or more LUNs to a snapshot group.

        Arguments:
            snapgroup           -- string
            luns                -- string / list
            snapgroup_object_id -- string
            lun_object_ids      -- list

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._update_luns_in_snapgroup('join', snapgroup, luns,
                snapgroup_object_id, lun_object_ids)

    def remove_luns_from_snapgroup(self, snapgroup=None, luns=[],
            snapgroup_object_id=None, lun_object_ids=[]):
        """Remove one or more LUNs from a snapshot group.

        Arguments:
            snapgroup           -- string
            luns                -- string / list
            snapgroup_object_id -- string
            lun_object_ids      -- list

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._update_luns_in_snapgroup('leave', snapgroup, luns,
                snapgroup_object_id, lun_object_ids)

    def delete_snapgroup(self, name=None, object_id=None):
        """Delete the specified snapshot group.

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
        # Perform all object_id lookups
        if object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            object_id = self.snapgroup_name_to_object_id(name)

        location = '{0}/{1}'.format(self._SNAPSHOT_GROUP_BASE_PATH, object_id)

        # Send the request
        return self.parent.basic.delete(location)

    def get_snapgroup_snapshots(self, group=None, comment=None,
            group_object_id=None):
        """
        Return a list of snapshots for the given snapshot group.

        Arguments:
            group           -- string
            comment         -- string
            group_object_id -- string

        Returns:
            list

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        ans = []

        # Determine the object_id
        if group_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            group_object_id = self.snapgroup_name_to_object_id(group)

        # Get the snapshots
        location = '{0}/{1}'.format(self._SNAPSHOT_BASE_PATH, group_object_id)
        result = self.parent.basic.get(location)
        if not result['success']:
            if 'Error: 0x09022049' in result['msg']:
                # This is when the snapgroup does not yet have a snapgroup
                # snapshot policy in place
                pass
            else:
                raise QueryError(ans.get('msg', str(ans)))
        else:
            try:
                if comment is None:
                    ans = [x for x in result['data']['timemarks']['timemarks']
                           if x['object_id']]
                else:
                    comment = str(comment)
                    ans = [x for x in result['data']['timemarks']['timemarks']
                           if x['comment'] == comment]
            except (KeyError, AttributeError):
                pass

        return ans

    def create_snapgroup_snapshot(self, name=None, comment=None,
            priority=None, enable_notification=None, object_id=None):
        """Creates a snapshot of the given snapshot group.

        Arguments:
            name                -- string
            comment             -- string
            priority            -- string
            enable_notification -- bool
            object_id           -- string

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
            object_id = self.snapgroup_name_to_object_id(name)

        # Send the request
        return self._create_snapshot(object_id, comment,
                priority, enable_notification)

    def delete_snapgroup_snapshot(self, group=None, comment=None,
            group_object_id=None, snapshot_object_id=None):
        """Delete a snapshot of the given snapshot group.

        Arguments:
            group              -- string
            comment            -- string
            group_object_id    -- string
            snapshot_object_id -- string

        Returns:
            dict

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Determine the object_id
        if snapshot_object_id is None:
            # Raises:  QueryError, NoMatchingObjectIdError,
            #          MultipleMatchingObjectIdsError
            snapshot_object_id = self.snapgroup_snapshot_comment_to_object_id(
                    group, comment, group_object_id)

        # Send the request
        return self._delete_snapshot(snapshot_object_id)
