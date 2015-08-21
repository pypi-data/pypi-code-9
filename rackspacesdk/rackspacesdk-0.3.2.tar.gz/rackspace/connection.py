# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import connection
from openstack import profile as _profile


class Connection(connection.Connection):

    def __init__(self, region=None, profile=None, **kwargs):
        """Create a connection to the Rackspace Public Cloud

        This is a subclass of :class:`openstack.connection.Connection` that
        provides a specialization to enable the Rackspace authentication
        plugin as well as the Rackspace provider extension.

        :param str region: The region to interact with. Valid values include:
        IAD, ORD, DFW, SYD, HKG, and LON. **This parameter is
        required and will raise ValueError if it is omitted.**

        :raises: ValueError if no `region` is specified.
        """
        if profile is None:
            profile = _profile.Profile(plugins=["rackspace"])

        if region is None:
            raise ValueError("You must specify a region to work with.")

        profile.set_region(profile.ALL, region)

        super(Connection, self).__init__(auth_plugin="rackspace",
                                         profile=profile,
                                         **kwargs)
