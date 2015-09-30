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

import sys
import random
import datetime

from vmemclient.core import restobject
from vmemclient.core.error import *


class PoolManager01(restobject.SessionNamespace):
    _STORAGE_POOL_BASE_PATH = '/physicalresource/storagepool'

    def get_storage_pools(self, name=None, verify=False,
                          include_full_info=False):
        """Gets the storage pools.

        If "verify" is set to True, then perform get_storage_pool_info() on
        the given storage pool to ensure its existence.

        If "include_full_info" is set to True, then each entry in the list will
        be a tuple, where the first element is the short entry and the second
        element is the full entry.  If "verify" is set to False and the lookup
        fails, then the second element will be None.

        None if the lookup
        Arguments:
            name              -- string
            verify            -- bool
            include_full_info -- bool

        Returns:
            list

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

        ans = self.parent.basic.get(self._STORAGE_POOL_BASE_PATH, filters)
        if not ans['success']:
            raise QueryError('Failed to get storage pools')

        # Retrieve the storage pools
        try:
            ans = [x for x in ans['data']['storage_pools']
                   if x['object_id']]
        except (KeyError, AttributeError):
            ans = []
        else:
            if verify or include_full_info:
                # Perform verification lookups
                new_answer = []
                for short_info in ans:
                    try:
                        full_info = self.get_storage_pool_info(
                            object_id=short_info['object_id'],
                        )
                    except QueryError:
                        if verify:
                            continue
                        full_info = None
                    if include_full_info:
                        new_answer.append((
                            short_info,
                            full_info,
                        ))
                    else:
                        new_answer.append(short_info)
                ans = new_answer

        return ans

    def storage_pool_name_to_object_id(self, name):
        """Finds the object_id for the given storage pool.

        Arguments:
            name -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._find_storage_pool_and_return_field(name, 'object_id')

    def storage_pool_name_to_id(self, name):
        """Finds the id for the given storage pool.

        Arguments:
            name -- string

        Returns:
            string

        Raises:
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        return self._find_storage_pool_and_return_field(name,
                                                        'storage_pool_id')

    def _find_storage_pool_and_return_field(self, name, field):
        """Internal function for:

            storage_pool_name_to_object_id
            storage_pool_name_to_id

        """
        # Raises: QueryError
        ans = self.get_storage_pools(name, verify=True)

        # Return the answer
        if len(ans) == 0:
            raise NoMatchingObjectIdError(str(name))
        elif len(ans) == 1:
            return ans[0][field]
        else:
            raise MultipleMatchingObjectIdsError(
                ', '.join(x['object_id'] for x in ans),
            )

    def get_storage_pool_info(self, name=None, object_id=None):
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
        if object_id is None:
            # Raises: QueryError, NoMatchingObjectIdError,
            #         MultipleMatchingObjectIdsError
            object_id = self.storage_pool_name_to_object_id(name)

        # Get the storage pool info
        location = '{0}/{1}'.format(self._STORAGE_POOL_BASE_PATH, object_id)
        ans = self.parent.basic.get(location)
        if not ans['success']:
            raise QueryError(ans.get('msg', str(ans)))

        return ans['data']

class PoolManager02(PoolManager01):
    def select_storage_pool(self, size, pool_type='thick', pool_name=None,
                            dedup_only_pools=[], mixed_pools=[],
                            method='random', usage=None):
        """Select a storage pool based on the given parameters.

        By default, the dict returned from this function will have two keys:

            * storage_pool
            * storage_pool_id

        Arguments:
            size             -- int.  The size of the LUN (in MB) that the
                                pool should be capable of making.
            pool_type        -- string.  One of the following values:
                                    * thick
                                    * thin
                                    * dedup
            pool_name        -- string.  The specific pool name that you would
                                like to use.
            dedup_only_pools -- list of strings.  The storage pools that only
                                support dedup LUNs.  Used for external head
                                setups only, as dedup capable pools can be
                                determined for internal head Concertos.
            mixed_pools      -- list of strings.  The storage pools that can
                                support all three pool types (thick, thin,
                                and dedup).  Used for external head setups
                                only, as dedup capable pools can be determined
                                for internal head Concertos.
            method           -- string.  How this function should choose the
                                storage pool to select.  Of the pools that
                                supports the requested pool_type and has at
                                least "size" MB free, the "method" is how to
                                choose between them.  This can be any of the
                                following values:
                                    * random
                                    * largest
                                    * smallest
            usage            -- string.  If you are planning on using the
                                returned dict from this function to feed
                                another one, then you can give that
                                operation here, and the dict returned will
                                contain some extra fields.  The following
                                usages are supported:
                                    * create_lun:
                                        - dedup: bool
                                        - thin: bool

        Returns:
            dict

        Raises:
            ValueError
            QueryError
            NoMatchingObjectIdError
            MultipleMatchingObjectIdsError

        """
        # Constants
        POOL_NAME_FIELD = 'storage_pool'
        POOL_ID_FIELD = 'storage_pool_id'
        THIN_KEY = 'thin'
        DEDUP_KEY = 'dedup'

        # Sanity check the input arguments
        if pool_type not in ('thick', 'thin', 'dedup'):
            raise ValueError('pool_type: {0}'.format(pool_type))
        size = int(size)
        if size <= 0:
            raise ValueError('size should be > 0')
        if method not in ('random', 'largest', 'smallest'):
            raise ValueError('method: {0}'.format(method))
        if usage not in ('create_lun', None):
            raise ValueError('usage: {0}'.format(usage))

        # Get all the pools to choose from.  This also makes sure that
        # the connection is still open (and that we can trust what is in
        # this object's properties dict).
        # Raises:  QueryError
        pools = self.get_storage_pools(pool_name, verify=True,
                                       include_full_info=True)

        # Remove config repository storage pools
        pools = [short_info
            for short_info, full_info in pools
            if 'Configuration' not in full_info.get('resource_type', [])
        ]

        # Limit pool selection: size
        pools = [x for x in pools if x['availsize_mb'] >= size]

        # Limit pool selection: pool type
        if self.parent.utility.is_external_head:
            # External head Concerto
            if pool_type == 'dedup':
                pools = [x for x in pools
                         if x['name'] in dedup_only_pools
                         or x['name'] in mixed_pools]
            else:
                pools = [x for x in pools if x['name'] not in dedup_only_pools]
        else:
            # Internal head Concerto
            if pool_type == 'dedup':
                if not self.parent.utility.is_dedup_enabled():
                    # MG does not have dedup capabilities
                    del(pools[:])

        # Choose a storage pool based on the selection method
        if not pools:
            ans = None
        else:
            if method == 'random':
                # Choose a random storage pool
                choice = random.choice(pools)
            elif method == 'largest':
                # Choose the largest storage pool
                choice = {'availsize_mb': 0}
                for info in pools:
                    if info['availsize_mb'] > choice['availsize_mb']:
                        choice = info
            else:
                # Choose the smallest storage pool
                choice = {'availsize_mb': sys.maxint}
                for info in pools:
                    if info['availsize_mb'] < choice['availsize_mb']:
                        choice = info

            # Convert choice to answer dict
            ans = {
                POOL_NAME_FIELD: choice['name'],
                POOL_ID_FIELD: choice['storage_pool_id'],
            }

        # Handle usage
        if ans is not None:
            if usage == 'create_lun':
                # Returned dict should also have 'thick' and 'dedup' keys
                if pool_type == 'thick':
                    ans[DEDUP_KEY] = False
                    ans[THIN_KEY] = False
                else:
                    # Both thin and dedup LUNs are thin LUNs
                    ans[THIN_KEY] = True

                    # Now we need to set the dedup flag.  This should be set
                    # to True iff the pool_type is dedup AND this is not an
                    # external head Concerto.
                    if (pool_type == 'dedup' and
                            not self.parent.utility.is_external_head):
                        ans[DEDUP_KEY] = True
                    else:
                        ans[DEDUP_KEY] = False

        # Done
        return ans
