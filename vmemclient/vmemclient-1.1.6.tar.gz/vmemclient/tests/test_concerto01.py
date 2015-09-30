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

import os
import sys
import unittest

import mock

import vmemclient
from vmemclient.core.error import *

import vmemclient.concerto.concerto


# Constants
GENERIC_SUCCESS_RESPONSE = {
    u'msg': u'Successful',
    u'success': True}
GENERIC_FAILURE_RESPONSE = {
    u'msg': u'Generic failure response',
    u'success': False}
GENERIC_BUILD_REQUEST_DATA_ANSWER = {'params': {
        'action': 'store',
        'location': 'front'}}

ALL_ADAPTERS_DATA = [{u'adaptermode': u'',
        u'info': u'ahci',
        u'mode': u'',
        u'module_name': u'ahci',
        u'number': 0,
        u'object_id': u'36dcd0cd-476a-529f-919d-15564f597412',
        u'port_status': u'',
        u'type': u'scsi'},
    {u'adaptermode': u'',
        u'info': u'ahci',
        u'mode': u'',
        u'module_name': u'ahci',
        u'number': 1,
        u'object_id': u'd5d71684-dac4-5202-bf94-a78797f9542c',
        u'port_status': u'',
        u'type': u'scsi'},
    {u'adaptermode': u'',
        u'info': u'ahci',
        u'mode': u'',
        u'module_name': u'ahci',
        u'number': 2,
        u'object_id': u'8902ea71-b645-553f-9f94-b69983279fa3',
        u'port_status': u'',
        u'type': u'scsi'},
    {u'adaptermode': u'',
        u'info': u'ahci',
        u'mode': u'',
        u'module_name': u'ahci',
        u'number': 3,
        u'object_id': u'fdc830d6-492c-520e-ac22-9205280c96c5',
        u'port_status': u'',
        u'type': u'scsi'},
    {u'adaptermode': u'',
        u'info': u'ahci',
        u'mode': u'',
        u'module_name': u'ahci',
        u'number': 4,
        u'object_id': u'9f430fc2-57ad-58b3-bb74-0aea0ede6cad',
        u'port_status': u'',
        u'type': u'scsi'},
    {u'adaptermode': u'',
        u'info': u'ahci',
        u'mode': u'',
        u'module_name': u'ahci',
        u'number': 5,
        u'object_id': u'1c565dcd-ce38-51be-b759-fe7b0d697847',
        u'port_status': u'',
        u'type': u'scsi'},
    {u'adaptermode': u'',
        u'info': u'Violin',
        u'mode': u'',
        u'module_name': u'blkscsi',
        u'number': 98,
        u'object_id': u'082043b2-be79-5643-8236-1db488487c53',
        u'port_status': u'',
        u'type': u'blockscsi'},
    {u'adaptermode': u'Fibre',
        u'info': u'QLogic',
        u'mode': u'Dual',
        u'module_name': u'qla2xxx',
        u'number': 100,
        u'object_id': u'aaa81336-c650-5088-8f32-06f115f13edb',
        u'port_status': u'Link Down',
        u'type': u'fc'},
    {u'adaptermode': u'Fibre',
        u'info': u'QLogic',
        u'mode': u'Dual',
        u'module_name': u'qla2xxx',
        u'number': 101,
        u'object_id': u'8723ebb6-d54a-5a6f-8f70-820f0dd622d7',
        u'port_status': u'Link Up',
        u'type': u'fc'},
    {u'adaptermode': u'Fibre',
        u'info': u'QLogic',
        u'mode': u'Dual',
        u'module_name': u'qla2xxx',
        u'number': 102,
        u'object_id': u'89b156e7-f43f-5e3b-89ff-df780ac11cae',
        u'port_status': u'Link Down',
        u'type': u'fc'},
    {u'adaptermode': u'Fibre',
        u'info': u'QLogic',
        u'mode': u'Dual',
        u'module_name': u'qla2xxx',
        u'number': 103,
        u'object_id': u'4a52e7ee-805c-50f1-b821-ab1ae9f35ab6',
        u'port_status': u'Link Up',
        u'type': u'fc'}]
ALL_ADAPTERS_RESPONSE = {
    u'data': {
        u'physical_adapters': ALL_ADAPTERS_DATA,
        u'total_physical_adapters': len(ALL_ADAPTERS_DATA)},
    u'msg': u'Successful',
    u'success': True}

ADAPTER_OBJECT_ID = u'4a52e7ee-805c-50f1-b821-ab1ae9f35ab6'
ADAPTER_INFO_DATA = {
    u'adapter_mode': u'Fibre',
    u'alias_wwpn_list': [{
            u'alpa': u'ff',
            u'mode': u'target',
            u'name': u'2100001b9722ae51'}],
    u'alpa': u'00',
    u'bios_wwpn': u'21-00-00-0e-1e-22-ae-51',
    u'bus': u'6',
    u'device': u'1',
    u'info': u'QLogic',
    u'irq': u'45',
    u'maxAliasCount': u'15',
    u'mismatch': u'false',
    u'mode': u'Dual',
    u'module_name': u'qla2xxx',
    u'monitor_wwpn': u'21-00-00-0e-1e-22-ae-51',
    u'name': u'',
    u'number': 103,
    u'object_id': u'4a52e7ee-805c-50f1-b821-ab1ae9f35ab6',
    u'persistent_binding': [],
    u'port_status': u'Link Up',
    u'secondary_standby_wwpn': u'',
    u'slot': u'0',
    u'sns': [],
    u'spoof_wwpn': u'',
    u'type': u'fc',
    u'vsaEnabled': u'false',
    u'wwpn': u'21-00-00-0e-1e-22-ae-51'}
ADAPTER_INFO_RESPONSE = {
    u'data': ADAPTER_INFO_DATA,
    u'msg': u'Successful',
    u'success': True}

ALL_CLIENTS_DATA = [{
        u'isbmr_enabled': False,
        u'isclustered': False,
        u'isfibrechannel_enabled': True,
        u'isiscsi_enabled': False,
        u'issanip_enabled': False,
        u'isxboot_enabled': False,
        u'name': u'qa-dl380g8-n1',
        u'object_id': u'f235e551-6dde-50c6-9a62-0edfe7632729',
        u'persistent_reservation': True,
        u'sanclient_id': 3,
        u'type': u'Linux',
        u'useracl': None},
    {u'isbmr_enabled': False,
        u'isclustered': False,
        u'isfibrechannel_enabled': True,
        u'isiscsi_enabled': False,
        u'issanip_enabled': False,
        u'isxboot_enabled': False,
        u'name': u'qa-reg7-cn2',
        u'object_id': u'2af8d0ca-b9ab-562e-9c42-ec41c1bbeae3',
        u'persistent_reservation': True,
        u'sanclient_id': 2,
        u'type': u'Linux',
        u'useracl': None},
    {u'isbmr_enabled': False,
        u'isclustered': False,
        u'isfibrechannel_enabled': True,
        u'isiscsi_enabled': False,
        u'issanip_enabled': False,
        u'isxboot_enabled': False,
        u'name': u'qa-dl380g8-n2',
        u'object_id': u'6461bc63-b68d-5538-9a1f-a9b9910fa7f0',
        u'persistent_reservation': True,
        u'sanclient_id': 4,
        u'type': u'Linux',
        u'useracl': None},
    {u'isbmr_enabled': False,
        u'isclustered': False,
        u'isfibrechannel_enabled': False,
        u'isiscsi_enabled': False,
        u'issanip_enabled': True,
        u'isxboot_enabled': False,
        u'name': u'lab-fil3494-mg-a',
        u'object_id': u'76dca00d-f45d-5c1c-a577-74bfafff906b',
        u'persistent_reservation': False,
        u'sanclient_id': 1,
        u'type': u'Undefined',
        u'useracl': None}]
ALL_CLIENTS_RESPONSE = {
    u'data': {
        u'san_clients': ALL_CLIENTS_DATA,
        u'total_san_clients': len(ALL_CLIENTS_DATA)},
    u'msg': u'Successful',
    u'success': True}

FILTERED_CLIENTS_DATA = [{u'isbmr_enabled': False,
        u'isclustered': False,
        u'isfibrechannel_enabled': True,
        u'isiscsi_enabled': False,
        u'issanip_enabled': False,
        u'isxboot_enabled': False,
        u'name': u'qa-dl380g8-n2',
        u'object_id': u'6461bc63-b68d-5538-9a1f-a9b9910fa7f0',
        u'persistent_reservation': True,
        u'sanclient_id': 4,
        u'type': u'Linux',
        u'useracl': None}]
FILTERED_CLIENTS_RESPONSE = {
    u'data': {
        u'san_clients': FILTERED_CLIENTS_DATA,
        u'total_san_clients': 1},
    u'msg': u'Successful',
    u'success': True}

EMPTY_CLIENTS_DATA = []
EMPTY_CLIENTS_RESPONSE = {
    u'data': {
        u'san_clients': [],
        u'total_san_clients': 0},
    u'msg': u'Successful',
    u'success': True}

CLIENT_NAME = u'qa-dl380g8-n2'
CLIENT_OBJECT_ID = u'6461bc63-b68d-5538-9a1f-a9b9910fa7f0'
CLIENT_INFO_DATA = {
    u'FCPolicy': {
        u'AS400enabled': False,
        u'VSAenabled': False,
        u'initiatorWWPNList': [
            u'50-01-43-80-18-6b-50-c0',
            u'50-01-43-80-18-6b-50-c2']},
    u'FibreChannelDevices': [],
    u'clusterName': u'',
    u'ipAddress': u'10.5.11.31',
    u'isbmr_enabled': False,
    u'isclustered': False,
    u'isfibrechannel_enabled': True,
    u'isiscsi_enabled': False,
    u'issanip_enabled': False,
    u'isxboot_enabled': False,
    u'name': u'qa-dl380g8-n2',
    u'persistent_reservation': True,
    u'sanclient_id': 4,
    u'type': u'Linux',
    u'useracl': None,
    u'username': u''}
CLIENT_INFO_RESPONSE = {
    u'data': CLIENT_INFO_DATA,
    u'msg': u'Successful',
    u'success': True}

ISCSI_TARGET_NAME = u'iqn.2004-02.com.vmem:lab-srv3083.lab-srv3079-0'
ISCSI_TARGET_OBJECT_ID = u'ba2a505a-e9b8-50a3-9745-59d9cb5c419e'

ALL_ISCSI_TARGETS_DATA = [
    {u'access': u'ReadWrite',
        u'ipAddr': u'192.168.70.1 192.168.71.1 192.168.72.1 192.168.73.1',
        u'isInfiniBand': False,
        u'iscsiurl': u'',
        u'name': u'iqn.2004-02.com.vmem:lab-srv3083.lab-srv3596-0',
        u'object_id': u'0b2acdac-548c-54ad-94da-44b558067d26',
        u'startingLun': u'0'},
    {u'access': u'ReadWrite',
        u'ipAddr': u'192.168.70.1 192.168.71.1 192.168.72.1 192.168.73.1',
        u'isInfiniBand': False,
        u'iscsiurl': u'',
        u'name': u'iqn.2004-02.com.vmem:lab-srv3083.lab-srv3079-0',
        u'object_id': u'ba2a505a-e9b8-50a3-9745-59d9cb5c419e',
        u'startingLun': u'0'}]
ALL_ISCSI_TARGETS_RESPONSE = {
    u'data': {
        u'iscsitargets': ALL_ISCSI_TARGETS_DATA,
        u'total_iscsitargets': len(ALL_ISCSI_TARGETS_DATA)},
    u'msg': u'Successful',
    u'success': True}

FILTERED_ISCSI_TARGETS_DATA = [
    {u'access': u'ReadWrite',
        u'ipAddr': u'192.168.70.1 192.168.71.1 192.168.72.1 192.168.73.1',
        u'isInfiniBand': False,
        u'iscsiurl': u'',
        u'name': u'iqn.2004-02.com.vmem:lab-srv3083.lab-srv3079-0',
        u'object_id': u'ba2a505a-e9b8-50a3-9745-59d9cb5c419e',
        u'startingLun': u'0'}]
FILTERED_ISCSI_TARGETS_RESPONSE = {
    u'data': {
        u'iscsitargets': FILTERED_ISCSI_TARGETS_DATA,
        u'total_iscsitargets': 1},
    u'msg': u'Successful',
    u'success': True}

EMPTY_ISCSI_TARGETS_DATA = []
EMPTY_ISCSI_TARGETS_RESPONSE = {
    u'data': {
        u'iscsitargets': EMPTY_ISCSI_TARGETS_DATA,
        u'total_iscsitargets': 0},
    u'msg': u'Successful',
    u'success': True}


class TestConcerto01(unittest.TestCase):
    CLASS_UNDER_TEST = vmemclient.concerto.concerto.Concerto01

    def setUp(self):
        super(TestConcerto01, self).setUp()
        session_attributes = {
            'host': 'fake.host.int',
            'user': 'username',
            'password': 'password',
            'debug': False,
            'proto': 'https',
            'keepalive': True,
            '_closed': False}
        version_info = {
            'api_version': '',
            'build': 1001,
            'concerto_version': '7.50',
            'version': '7.50.1001'}

        session = mock.Mock(**session_attributes)
        self.con = self.CLASS_UNDER_TEST(session, version_info)

    def mock_vmemclient(self, *args):
        """Mock out namespace / function with the given constructor params.

        Arguments passed to this function should be a three element tuple:
            * namespace (string) that exists off of self.con; if this is
                not specified, then the function to be mocked should exist
                off of self.con directly (a.k.a. - build_request_data)
            * function (string) that exists as self.con.<namespace>
            * attributes (dict) to be passed into the Mock() constructor

        """
        for namespace, function, attrs in args:
            if namespace is None:
                x = self.con
            else:
                x = getattr(self.con, namespace)
            setattr(x, function, mock.Mock(**attrs))

    def test_get_physical_adapters(self):
        '''adapter.get_physical_adapters()'''
        expected = ALL_ADAPTERS_DATA

        self.mock_vmemclient(
            ('basic', 'get', {'return_value': ALL_ADAPTERS_RESPONSE}))

        actual = self.con.adapter.get_physical_adapters()

        self.assertEqual(expected, actual)

    def test_get_physical_adapter_info(self):
        '''adapter.get_physical_adapter_info()'''
        expected = ADAPTER_INFO_DATA

        self.mock_vmemclient(
            ('basic', 'get', {'return_value': ADAPTER_INFO_RESPONSE}))

        actual = self.con.adapter.get_adapter_info(ADAPTER_OBJECT_ID)

        self.assertEqual(expected, actual)

    def test_get_fc_info(self):
        '''adapter.get_fc_info()'''
        adapter_info_list = [
                {'alias_wwpn_list': [{'name': '2100001b9722b3e0'}]},
                {'alias_wwpn_list': [{'name': '2100001b9722b3e1'}]},
                {'alias_wwpn_list': [{'name': '2100001b9722ae50'}]},
                {'alias_wwpn_list': [{'name': '2100001b9722ae51'}]}]
        expected = {
            u'4a52e7ee-805c-50f1-b821-ab1ae9f35ab6': [u'2100001b9722ae51'],
            u'8723ebb6-d54a-5a6f-8f70-820f0dd622d7': [u'2100001b9722b3e1'],
            u'89b156e7-f43f-5e3b-89ff-df780ac11cae': [u'2100001b9722ae50'],
            u'aaa81336-c650-5088-8f32-06f115f13edb': [u'2100001b9722b3e0']}

        self.mock_vmemclient(
            ('adapter', 'get_physical_adapters',
                {'return_value': ALL_ADAPTERS_DATA}),
            ('adapter', 'get_adapter_info',
                {'side_effect': adapter_info_list}))

        actual = self.con.adapter.get_fc_info()
        self.assertEqual(expected, actual)
        self.assertEqual(
            len(adapter_info_list),
            self.con.adapter.get_adapter_info.call_count)

    def test_get_clients(self):
        '''client.get_clients()'''
        expected = ALL_CLIENTS_DATA

        self.mock_vmemclient(
            ('basic', 'get', {'return_value': ALL_CLIENTS_RESPONSE}))

        actual = self.con.client.get_clients()

        self.assertEqual(expected, actual)

    def test_get_clients_no_results(self):
        '''client.get_clients() returns no results'''
        expected = EMPTY_CLIENTS_DATA

        self.mock_vmemclient(
            ('basic', 'get', {'return_value': EMPTY_CLIENTS_RESPONSE}))

        actual = self.con.client.get_clients()

        self.assertEqual(expected, actual)

    def test_get_clients_with_filter(self):
        '''client.get_clients(name)'''
        expected = FILTERED_CLIENTS_DATA

        self.mock_vmemclient(
            ('basic', 'get', {'return_value': FILTERED_CLIENTS_RESPONSE}))

        actual = self.con.client.get_clients(CLIENT_NAME)

        self.assertEqual(expected, actual)

    def test_client_name_to_object_id(self):
        '''client.client_name_to_object_id(name)'''
        expected = CLIENT_OBJECT_ID

        self.mock_vmemclient(
            ('client', 'get_clients', {'return_value': FILTERED_CLIENTS_DATA}))

        actual = self.con.client.client_name_to_object_id(CLIENT_NAME)

        self.assertEqual(expected, actual)

    def test_client_name_to_object_id_no_match_error(self):
        '''client.client_name_to_object_id(name) returns []'''
        self.mock_vmemclient(
            ('client', 'get_clients', {'return_value': []}))

        self.assertRaises(
            NoMatchingObjectIdError,
            self.con.client.client_name_to_object_id, CLIENT_NAME)

    def test_client_name_to_object_id_multi_match_error(self):
        '''client.client_name_to_object_id(name) returns many results'''
        self.mock_vmemclient(
            ('client', 'get_clients', {'return_value': ALL_CLIENTS_DATA}))

        self.assertRaises(
            MultipleMatchingObjectIdsError,
            self.con.client.client_name_to_object_id, CLIENT_NAME)

    def test_get_client_info_using_name(self):
        expected = CLIENT_INFO_DATA
        self.mock_vmemclient(
            ('client', 'client_name_to_object_id',
                {'return_value': CLIENT_OBJECT_ID}),
            ('basic', 'get', {'return_value': CLIENT_INFO_RESPONSE}))

        actual = self.con.client.get_client_info(CLIENT_NAME)

        self.assertEqual(expected, actual)

    def test_get_client_info_using_object_id(self):
        expected = CLIENT_INFO_DATA
        self.mock_vmemclient(
            ('basic', 'get', {'return_value': CLIENT_INFO_RESPONSE}))

        actual = self.con.client.get_client_info(object_id=CLIENT_OBJECT_ID)

        self.assertEqual(expected, actual)

    def test_update_client_basic_info_using_name(self):
        expected = GENERIC_SUCCESS_RESPONSE
        self.mock_vmemclient(
            ('client', 'client_name_to_object_id',
                {'return_value': CLIENT_OBJECT_ID}),
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'put', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.update_client_basic_info(
            name=CLIENT_NAME,
            ip='1.2.3.4',
            client_os='Linux',
            clustered=False,
            reserved=False)

        self.assertEqual(expected, actual)

    def test_update_client_basic_info_using_object_id(self):
        expected = GENERIC_SUCCESS_RESPONSE
        self.mock_vmemclient(
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'put', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.update_client_basic_info(
            object_id=CLIENT_OBJECT_ID,
            ip='1.2.3.4',
            client_os='Linux',
            clustered=False,
            reserved=False)

        self.assertEqual(expected, actual)

    def test_update_client_iscsci_info_using_name(self):
        expected = GENERIC_SUCCESS_RESPONSE
        self.mock_vmemclient(
            ('client', 'client_name_to_object_id',
                {'return_value': CLIENT_OBJECT_ID}),
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'put', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.update_client_iscsi_info(
            name=CLIENT_NAME,
            iscsi_iqns='iqn.fake',
            iscsi_enable_authentication=True,
            iscsi_users=['user1', 'user2'],
            iscsi_default_user='user1',
            iscsi_secret='swordfish',
            iscsi_enable_mutual_chap=True,
            iscsi_mutual_chap_user='old',
            iscsi_mutual_chap_secret='chap')

        self.assertEqual(expected, actual)

    def test_update_client_iscsci_info_using_object_id(self):
        expected = GENERIC_SUCCESS_RESPONSE
        self.mock_vmemclient(
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'put', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.update_client_iscsi_info(
            object_id=CLIENT_OBJECT_ID,
            iscsi_iqns='iqn.fake',
            iscsi_enable_authentication=True,
            iscsi_users=['user1', 'user2'],
            iscsi_default_user='user1',
            iscsi_secret='swordfish',
            iscsi_enable_mutual_chap=True,
            iscsi_mutual_chap_user='old',
            iscsi_mutual_chap_secret='chap')

        self.assertEqual(expected, actual)

    def test_update_client_fc_info_using_name(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            ('client', 'client_name_to_object_id',
                {'return_value': CLIENT_OBJECT_ID}),
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'put', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.update_client_fc_info(
            name=CLIENT_NAME,
            fc_wwns=['1122112211221122', '2211221122112211'],
            fc_vsa=False,
            fc_as400=False)

        self.assertEqual(expected, actual)

    def test_update_client_fc_info_using_object_id(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            ('client', 'client_name_to_object_id',
                {'side_effect': NoMatchingObjectIdError(CLIENT_NAME)}),
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'put', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.update_client_fc_info(
            object_id=CLIENT_OBJECT_ID,
            fc_wwns=['1122112211221122', '2211221122112211'],
            fc_vsa=False,
            fc_as400=False)

        self.assertEqual(expected, actual)

    def test_create_client_with_fc_info(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'post', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.create_client(
            name=CLIENT_NAME,
            proto='FC',
            ip='1.2.3.4',
            client_os='Linux',
            clustered=False,
            reserved=True,
            fc_wwns=['1122112211221122', '2211221122112211'],
            fc_vsa=False,
            fc_as400=False)

        self.assertEqual(expected, actual)

    def test_create_client_with_iscsi_info(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'post', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.create_client(
            name=CLIENT_NAME,
            proto='FC',
            ip='1.2.3.4',
            client_os='Linux',
            clustered=False,
            reserved=True,
            iscsi_iqns='iqn.fake',
            iscsi_enable_authentication=True,
            iscsi_users=['user1', 'user2'],
            iscsi_default_user='user1',
            iscsi_secret='swordfish',
            iscsi_enable_mutual_chap=True,
            iscsi_mutual_chap_user='sonic',
            iscsi_mutual_chap_secret='youth')

        self.assertEqual(expected, actual)

    def test_delete_client_using_name(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            ('client', 'client_name_to_object_id',
                {'return_value': CLIENT_OBJECT_ID}),
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'delete', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.delete_client(name=CLIENT_NAME)

        self.assertEqual(expected, actual)

    def test_delete_client_using_object_id(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            (None, 'build_request_data',
                {'return_value': GENERIC_BUILD_REQUEST_DATA_ANSWER}),
            ('basic', 'delete', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.delete_client(object_id=CLIENT_OBJECT_ID)

        self.assertEqual(expected, actual)

    def test_get_iscsi_targets(self):
        '''client.get_iscsi_targets()'''
        expected = ALL_ISCSI_TARGETS_DATA

        self.mock_vmemclient(
            ('basic', 'get', {'return_value': ALL_ISCSI_TARGETS_RESPONSE}))

        actual = self.con.client.get_iscsi_targets()

        self.assertEqual(expected, actual)

    def test_get_iscsi_targets_no_results(self):
        '''client.get_iscsi_targets() returns no results'''
        expected = EMPTY_ISCSI_TARGETS_DATA

        self.mock_vmemclient(
            ('basic', 'get', {'return_value': EMPTY_ISCSI_TARGETS_RESPONSE}))

        actual = self.con.client.get_iscsi_targets()

        self.assertEqual(expected, actual)

    def test_get_iscsi_targets_with_filter(self):
        '''client.get_iscsi_targets(name)'''
        expected = FILTERED_ISCSI_TARGETS_DATA

        self.mock_vmemclient(
            ('basic', 'get',
                {'return_value': FILTERED_ISCSI_TARGETS_RESPONSE}))

        actual = self.con.client.get_iscsi_targets(ISCSI_TARGET_NAME)

        self.assertEqual(expected, actual)

    def test_iscsi_target_name_to_object_id(self):
        expected = ISCSI_TARGET_OBJECT_ID

        self.mock_vmemclient(
            ('client', 'get_iscsi_targets',
                {'return_value': FILTERED_ISCSI_TARGETS_DATA}))

        actual = self.con.client.iscsi_target_name_to_object_id(
            ISCSI_TARGET_NAME)

        self.assertEqual(expected, actual)

    def test_iscsi_target_name_to_object_id_no_match_error(self):
        self.mock_vmemclient(
            ('client', 'get_iscsi_targets', {'return_value': []}))

        self.assertRaises(
            NoMatchingObjectIdError,
            self.con.client.iscsi_target_name_to_object_id, ISCSI_TARGET_NAME)

    def test_iscsi_target_name_to_object_id_multi_match_error(self):
        self.mock_vmemclient(
            ('client', 'get_iscsi_targets',
                {'return_value': ALL_ISCSI_TARGETS_DATA}))

        self.assertRaises(
            MultipleMatchingObjectIdsError,
            self.con.client.iscsi_target_name_to_object_id, ISCSI_TARGET_NAME)

    def test_create_iscsi_target_using_client_name(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            ('client', 'get_client_info', {'return_value': CLIENT_INFO_DATA}),
            ('basic', 'post', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.create_iscsi_target(
            name=ISCSI_TARGET_NAME,
            client_name=CLIENT_NAME,
            ip=['1.2.3.4', '5.6.7.8'],
            access_mode='ReadWrite',
            starting_lun=0,
            infiniband=False,
            client_id=5)

        self.assertEqual(expected, actual)

    def test_create_iscsi_target_using_client_id(self):
        expected = GENERIC_SUCCESS_RESPONSE

        self.mock_vmemclient(
            ('client', 'get_client_info',
                {'side_effect': NoMatchingObjectIdError}),
            ('basic', 'post', {'return_value': GENERIC_SUCCESS_RESPONSE}))

        actual = self.con.client.create_iscsi_target(
            name=ISCSI_TARGET_NAME,
            client_name=CLIENT_NAME,
            ip=['1.2.3.4', '5.6.7.8'],
            access_mode='ReadWrite',
            starting_lun=0,
            infiniband=False,
            client_id=5)

        self.assertEqual(expected, actual)
