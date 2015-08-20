# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest_lib.common.utils import data_utils

from functional.common import test

BASIC_LIST_HEADERS = ['ID', 'Name']


class NetworkTests(test.TestCase):

    NETWORK_FIELDS = ['id', 'name']

    def _create_dummy_network(self):
        network_name = data_utils.rand_name('TestNetwork')
        raw_output = self.openstack(
            'network create '
            '%s' % network_name)
        self.addCleanup(
            self.openstack,
            'network delete %s' % network_name)
        items = self.parse_show(raw_output)
        self.assert_show_structure(items, self.NETWORK_FIELDS)
        return network_name

    def test_network_create(self):
        network_name = data_utils.rand_name('TestNetwork')
        raw_output = self.openstack(
            'network create '
            '%s' % network_name)
        self.addCleanup(
            self.openstack,
            'network delete %s' % network_name)
        items = self.parse_show(raw_output)
        self.assert_show_structure(items, self.NETWORK_FIELDS)

    def test_network_delete(self):
        network_name = data_utils.rand_name('TestNetwork')
        self.openstack(
            'network create '
            '%s' % network_name)
        raw_output = self.openstack('network delete %s' % network_name)
        self.assertEqual(0, len(raw_output))

    def test_network_list(self):
        raw_output = self.openstack('network list')
        items = self.parse_listing(raw_output)
        self.assert_table_structure(items, BASIC_LIST_HEADERS)

    def test_network_show(self):
        network_name = self._create_dummy_network()
        raw_output = self.openstack('network show %s' % network_name)
        items = self.parse_show(raw_output)
        self.assert_show_structure(items, self.NETWORK_FIELDS)

    def test_network_set(self):
        network_name = self._create_dummy_network()
        raw_output = self.openstack(
            'network set '
            '--disable '
            '%s' % network_name
        )
        self.assertEqual(0, len(raw_output))
        raw_output = self.openstack(
            'network show %s' % network_name)
        network = self.parse_show_as_object(raw_output)
        self.assertEqual('DOWN', network['state'])
