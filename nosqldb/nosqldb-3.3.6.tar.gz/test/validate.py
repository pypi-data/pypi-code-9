#
#  This file is part of Oracle NoSQL Database
#  Copyright (C) 2011, 2015 Oracle and/or its affiliates.  All rights reserved.
#
# If you have received this file as part of Oracle NoSQL Database the
# following applies to the work as a whole:
#
#   Oracle NoSQL Database server software is free software: you can
#   redistribute it and/or modify it under the terms of the GNU Affero
#   General Public License as published by the Free Software Foundation,
#   version 3.
#
#   Oracle NoSQL Database is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Affero General Public License for more details.
#
# If you have received this file as part of Oracle NoSQL Database Client or
# distributed separately the following applies:
#
#   Oracle NoSQL Database client software is free software: you can
#   redistribute it and/or modify it under the terms of the Apache License
#   as published by the Apache Software Foundation, version 2.0.
#
# You should have received a copy of the GNU Affero General Public License
# and/or the Apache License in the LICENSE file along with Oracle NoSQL
# Database client or server distribution.  If not, see
# <http://www.gnu.org/licenses/>
# or
# <http://www.apache.org/licenses/LICENSE-2.0>.
#
# An active Oracle commercial licensing agreement for this product supersedes
# these licenses and in such case the license notices, but not the copyright
# notice, may be removed by you in connection with your distribution that is
# in accordance with the commercial licensing terms.
#
# For more information please contact:
#
# berkeleydb-info_us@oracle.com
#
from nosqldb import Consistency
from nosqldb import SimpleConsistency
from nosqldb import TimeConsistency
from nosqldb import VersionConsistency
from nosqldb import Durability
from nosqldb import ReadOptions
from nosqldb import WriteOptions
from nosqldb import FieldRange
from nosqldb import MultiRowOptions
from nosqldb import Direction
from nosqldb import TableIteratorOptions
from nosqldb import OperationType
from nosqldb import Operation
from nosqldb import Row
from nosqldb import IllegalArgumentException
from nosqldb import ABSOLUTE
from nosqldb import NONE_REQUIRED
from nosqldb import NONE_REQUIRED_NO_MASTER
from nosqldb import COMMIT_SYNC
from nosqldb import COMMIT_NO_SYNC
from nosqldb import COMMIT_WRITE_NO_SYNC
from nosqldb import ONDB_MASTER_SYNC
from nosqldb import ONDB_REPLICA_SYNC
from nosqldb import ONDB_REPLICA_ACK
from nosqldb import ONDB_CONSISTENCY
from nosqldb import ONDB_SIMPLE_CONSISTENCY
from nosqldb import ONDB_TIME_CONSISTENCY
from nosqldb import ONDB_VERSION_CONSISTENCY
from nosqldb import ONDB_PERMISSIBLE_LAG
from nosqldb import ONDB_DURABILITY
from nosqldb import ONDB_TIMEOUT
from nosqldb import ONDB_RETURN_CHOICE
from nosqldb import ONDB_FIELD
from nosqldb import ONDB_START_VALUE
from nosqldb import ONDB_END_VALUE
from nosqldb import ONDB_START_INCLUSIVE
from nosqldb import ONDB_END_INCLUSIVE
from nosqldb import ONDB_FIELD_RANGE
from nosqldb import ONDB_INCLUDED_TABLES
from nosqldb import ONDB_DIRECTION
from nosqldb import ONDB_MAX_RESULTS
from nosqldb import ONDB_READ_OPTIONS
from nosqldb import ONDB_OPERATION_TYPE
from nosqldb import ONDB_TABLE_NAME
from nosqldb import ONDB_OPERATION
from nosqldb import ONDB_ROW
from nosqldb import ONDB_ABORT_IF_UNSUCCESSFUL
from nosqldb import ONDB_VERSION

import unittest


class ValidateTest(unittest.TestCase):

    def testAbsoluteConsistency(self):
        con = SimpleConsistency({ONDB_SIMPLE_CONSISTENCY: 'ABSOLUTE'})
        con.validate()
        self.assertTrue(True)

    def testNoneRequiredConsistency(self):
        con = SimpleConsistency({ONDB_SIMPLE_CONSISTENCY: 'NONE_REQUIRED'})
        con.validate()
        self.assertTrue(True)

    def testNoneRequiredNoMasterConsistency(self):
        con = SimpleConsistency({
            ONDB_SIMPLE_CONSISTENCY: 'NONE_REQUIRED_NO_MASTER'})
        con.validate()
        self.assertTrue(True)

    def testTimeConsistency(self):
        con = TimeConsistency({
            ONDB_PERMISSIBLE_LAG: 500,
            ONDB_TIMEOUT: 1000})
        con.validate()
        self.assertTrue(True)

    def testTimeConsistencyNoTimeout(self):
        con = TimeConsistency({
            ONDB_PERMISSIBLE_LAG: 500})
        self.assertRaises(IllegalArgumentException, con.validate)

    def testTimeConsistencyNoPermissibleLag(self):
        con = TimeConsistency({
            ONDB_TIMEOUT: 1000})
        self.assertRaises(IllegalArgumentException, con.validate)

    def testVersionConsistency(self):
        con = VersionConsistency({
            ONDB_VERSION: bytearray('!@$!$C$'),
            ONDB_TIMEOUT: 500})
        con.validate()
        self.assertTrue(True)

    def testVersionConsistencyNoTimeout(self):
        con = VersionConsistency({
            ONDB_VERSION: bytearray('#@%#%')})
        self.assertRaises(IllegalArgumentException, con.validate)

    def testVersionConsistencyNoVersion(self):
        con = VersionConsistency({
            ONDB_TIMEOUT: 1000})
        self.assertRaises(IllegalArgumentException, con.validate)

    def testBadKeyConsistency(self):
        self.assertRaises(KeyError, Consistency,
            {'badkey': 'badvalue'})

    def testBadValueConsistency(self):
        con = Consistency({
            ONDB_SIMPLE_CONSISTENCY: 'SOME'})
        self.assertRaises(IllegalArgumentException, con.validate)

    def testReadOptions(self):
        con = Consistency({ONDB_SIMPLE_CONSISTENCY: 'NONE_REQUIRED'})
        ro = ReadOptions({
            ONDB_CONSISTENCY: con,
            ONDB_TIMEOUT: 10})
        ro.validate()
        self.assertTrue(True)

    def testJSONConsistencyReadOptions(self):
        ro = ReadOptions({
            ONDB_CONSISTENCY: {
                ONDB_SIMPLE_CONSISTENCY: 'NONE_REQUIRED_NO_MASTER'},
            ONDB_TIMEOUT: 10})
        ro.validate()
        self.assertTrue(True)

    def testJSONTimeConsistencyReadOptions(self):
        con = {
            ONDB_PERMISSIBLE_LAG: 500,
            ONDB_TIMEOUT: 1000}
        ro = ReadOptions({
            ONDB_CONSISTENCY: {ONDB_TIME_CONSISTENCY: con},
            ONDB_TIMEOUT: 1000})
        ro.validate()
        self.assertTrue(True)

    def testJSONVersionConsistencyReadOptions(self):
        con = {
            ONDB_VERSION: bytearray('!$@%@^2'),
            ONDB_TIMEOUT: 1000}
        ro = ReadOptions({
            ONDB_CONSISTENCY: {ONDB_VERSION_CONSISTENCY: con},
            ONDB_TIMEOUT: 1000})
        ro.validate()
        self.assertTrue(True)

    def testJSONVersionConsistencyReadOptions2(self):
        ro = ReadOptions({
            'consistency': {
                'version': {
                    'version': bytearray('!$@%@^2'),
                    'timeout': 1000}},
            ONDB_TIMEOUT: 1000})
        ro.validate()
        self.assertTrue(True)

    def testBadJSONVersionConsistencyReadOptions(self):
        con = {
            ONDB_VERSION: bytearray('!$@%@^2')}
        ro = ReadOptions({
            ONDB_CONSISTENCY: {ONDB_VERSION_CONSISTENCY: con},
            ONDB_TIMEOUT: 1000})
        self.assertRaises(IllegalArgumentException, ro.validate)

    def testBadJSONTimeConsistencyReadOptions(self):
        con = {
            ONDB_PERMISSIBLE_LAG: 500}
        ro = ReadOptions({
            ONDB_CONSISTENCY: {ONDB_TIME_CONSISTENCY: con},
            ONDB_TIMEOUT: 1000})
        self.assertRaises(IllegalArgumentException, ro.validate)

    def testBadJSONConsistencyReadOptions(self):
        ro = ReadOptions({
            ONDB_CONSISTENCY: {
                ONDB_SIMPLE_CONSISTENCY: 'SOME'
                },
            ONDB_TIMEOUT: 10})
        self.assertRaises(IllegalArgumentException, ro.validate)

    def testBadTimeoutReadOptions(self):
        ro = ReadOptions({ONDB_CONSISTENCY: {
                ONDB_SIMPLE_CONSISTENCY: 'ABSOLUTE'},
            ONDB_TIMEOUT: 'SOME'})
        self.assertRaises(IllegalArgumentException, ro.validate)

    def testCommitNoSyncDurability(self):
        dur = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        dur.validate()
        self.assertTrue(True)

    def testCommitSyncDurability(self):
        dur = Durability({
            ONDB_MASTER_SYNC: 'SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        dur.validate()
        self.assertTrue(True)

    def testCommitWriteNoSyncDurability(self):
        dur = Durability({
            ONDB_MASTER_SYNC: 'WRITE_NO_SYNC',
            ONDB_REPLICA_SYNC: 'WRITE_NO_SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        dur.validate()
        self.assertTrue(True)

    def testBadKeyDurability(self):
        self.assertRaises(KeyError, Durability,
            {'master_blaster': True})

    def testBadContentDurability(self):
        dur = Durability({ONDB_MASTER_SYNC: 'SOME'})
        self.assertRaises(IllegalArgumentException, dur.validate)

    def testAllTreeDurabilityOptionsRequired(self):
        dur = Durability({ONDB_MASTER_SYNC: 'WRITE_NO_SYNC'})
        self.assertRaises(IllegalArgumentException, dur.validate)

    def testWriteOptions(self):
        dur = COMMIT_NO_SYNC
        wo = WriteOptions({
            ONDB_DURABILITY: dur,
            ONDB_TIMEOUT: 10,
            ONDB_RETURN_CHOICE: 'ALL',
            'if_absent': False,
            'if_present': False,
            'if_version': None})
        wo.validate()
        self.assertTrue(True)

    def testJSONDurabilityWriteOptions(self):
        dur = {ONDB_MASTER_SYNC: 'SYNC', ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'}
        wo = WriteOptions({
            ONDB_DURABILITY: dur,
            ONDB_TIMEOUT: 10,
            ONDB_RETURN_CHOICE: 'NONE'})
        wo.validate()
        self.assertTrue(True)

    def testBadJSONDurabilityWriteOptions(self):
        dur = {'master_blaster': 'SOME', ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'}
        wo = WriteOptions({
            ONDB_DURABILITY: dur,
            ONDB_TIMEOUT: 10,
            ONDB_RETURN_CHOICE: 'NONE'})
        self.assertRaises(KeyError, wo.validate)

    def testBadTimeoutWriteOptions(self):
        wo = WriteOptions({ONDB_TIMEOUT: 'NOTHING'})
        self.assertRaises(IllegalArgumentException, wo.validate)

    def testBadReturValueVersionWriteOptions(self):
        wo = WriteOptions({ONDB_RETURN_CHOICE: 'PARTIAL'})
        self.assertRaises(IllegalArgumentException, wo.validate)

    def testFieldRange(self):
        fr = FieldRange({
            ONDB_FIELD: 'id',
            ONDB_START_VALUE: '10',
            ONDB_END_VALUE: '20',
            ONDB_START_INCLUSIVE: False,
            ONDB_END_INCLUSIVE: True})
        fr.validate()
        self.assertTrue(True)

    def testBadField(self):
        fr = FieldRange({
            ONDB_FIELD: 123,
            ONDB_START_VALUE: '10'})
        self.assertRaises(IllegalArgumentException, fr.validate)

    def testBadStartField(self):
        fr = FieldRange({
            ONDB_FIELD: 'id',
            ONDB_END_VALUE: '20',
            ONDB_START_INCLUSIVE: 'NO'})
        self.assertRaises(IllegalArgumentException, fr.validate)

    def testBadEndField(self):
        fr = FieldRange({
            ONDB_FIELD: 'id',
            ONDB_END_VALUE: 20,
            ONDB_END_INCLUSIVE: 'NO'})
        self.assertRaises(IllegalArgumentException, fr.validate)

    def testMissingStartAndEndValue(self):
        fr = FieldRange({
            ONDB_FIELD: 'id',
            ONDB_START_INCLUSIVE: 'NO'})
        self.assertRaises(IllegalArgumentException, fr.validate)

    def testMultiRowOptions(self):
        fr = FieldRange({
            ONDB_FIELD: 'id',
            ONDB_START_VALUE: '10',
            ONDB_END_VALUE: '20',
            ONDB_START_INCLUSIVE: False,
            ONDB_END_INCLUSIVE: True})
        mro = MultiRowOptions({
            ONDB_FIELD_RANGE: fr,
            ONDB_INCLUDED_TABLES: ['parent1', 'parent2', 'parent3',
                'child1', 'child2', 'child3']})
        mro.validate()
        self.assertTrue(True)

    def testJSONFieldRangeMultiRowOptions(self):
        mro = MultiRowOptions({
            ONDB_FIELD_RANGE: {
                ONDB_FIELD: 'id',
                ONDB_START_VALUE: '1',
                ONDB_END_VALUE: '100',
                ONDB_START_INCLUSIVE: True,
                ONDB_END_INCLUSIVE: True},
            ONDB_INCLUDED_TABLES: ['parent1', 'parent2', 'parent3',
                'child1', 'child2', 'child3']})
        mro.validate()
        self.assertTrue(True)

    def testBadJSONFieldRangeMultiRowOptions(self):
        mro = MultiRowOptions({
            ONDB_FIELD_RANGE: {
                ONDB_FIELD: 'field1',
                ONDB_START_VALUE: 1,
                'bad_key': 'bad_value'},
            ONDB_INCLUDED_TABLES: ['parent1', 'parent2', 'parent3',
                'child1', 'child2', 'child3']})
        self.assertRaises(KeyError, mro.validate)

    def testBadPatentTablesMultiRowOptions(self):
        mro = MultiRowOptions({
            ONDB_FIELD_RANGE: {
                ONDB_FIELD: 'id',
                ONDB_END_VALUE: '123'},
            ONDB_INCLUDED_TABLES: 'parent1'})
        self.assertRaises(IllegalArgumentException, mro.validate)

    def testBadChildTablesMultiRowOptions(self):
        mro = MultiRowOptions({
            ONDB_FIELD_RANGE: {
                ONDB_FIELD: 'id',
                ONDB_END_VALUE: '123'},
            ONDB_INCLUDED_TABLES: 'child2'})
        self.assertRaises(IllegalArgumentException, mro.validate)

    def testForwardDirection(self):
        direction = Direction({ONDB_DIRECTION: 'FORWARD'})
        direction.validate()
        self.assertTrue(True)

    def testReverseDirection(self):
        direction = Direction({ONDB_DIRECTION: 'REVERSE'})
        direction.validate()
        self.assertTrue(True)

    def testUnorderedDirection(self):
        direction = Direction({ONDB_DIRECTION: 'UNORDERED'})
        direction.validate()
        self.assertTrue(True)

    def testBadDirection(self):
        direction = Direction({ONDB_DIRECTION: 'NODIR'})
        self.assertRaises(IllegalArgumentException, direction.validate)

    def testNoneDirection(self):
        direction = Direction({ONDB_DIRECTION: None})
        self.assertRaises(IllegalArgumentException, direction.validate)

    def testTableIteratorOptions(self):
        direction = Direction({ONDB_DIRECTION: 'FORWARD'})
        read_opts = ReadOptions({
            ONDB_CONSISTENCY: {ONDB_SIMPLE_CONSISTENCY: 'ABSOLUTE'},
            ONDB_TIMEOUT: 10})
        table_iter = TableIteratorOptions({
            ONDB_DIRECTION: direction,
            ONDB_MAX_RESULTS: 200,
            ONDB_READ_OPTIONS: read_opts})
        table_iter.validate()
        self.assertTrue(True)

    def testBadDirectionIteratorOptions(self):
        read_opts = ReadOptions({
            ONDB_CONSISTENCY: {ONDB_SIMPLE_CONSISTENCY: 'ABSOLUTE'},
            ONDB_TIMEOUT: 10})
        table_iter = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'RIGHT'},
            ONDB_MAX_RESULTS: 200,
            ONDB_READ_OPTIONS: read_opts})
        self.assertRaises(IllegalArgumentException, table_iter.validate)

    def testBadMaxResultsByBatch(self):
        direction = Direction({ONDB_DIRECTION: 'UNORDERED'})
        read_opts = ReadOptions({
            ONDB_CONSISTENCY: ABSOLUTE,
            ONDB_TIMEOUT: 10})
        table_iter = TableIteratorOptions({
            ONDB_DIRECTION: direction,
            ONDB_MAX_RESULTS: '200',
            ONDB_READ_OPTIONS: read_opts})
        self.assertRaises(IllegalArgumentException, table_iter.validate)

    def testBadReadOptionsIteratorOptions(self):
        direction = Direction({ONDB_DIRECTION: 'UNORDERED'})
        read_opts = ReadOptions({
            ONDB_CONSISTENCY: 'ABSOLUTE',
            ONDB_TIMEOUT: 10})
        table_iter = TableIteratorOptions({
            ONDB_DIRECTION: direction,
            ONDB_MAX_RESULTS: '200',
            ONDB_READ_OPTIONS: read_opts})
        self.assertRaises(IllegalArgumentException, table_iter.validate)

    def testDeleteOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'DELETE'})
        op_type.validate()
        self.assertTrue(True)

    def testDeleteIfVersionOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'DELETE_IF_VERSION'})
        op_type.validate()
        self.assertTrue(True)

    def testPutOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT'})
        op_type.validate()
        self.assertTrue(True)

    def testPutIfAbsentOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT_IF_ABSENT'})
        op_type.validate()
        self.assertTrue(True)

    def testPutIfPresentOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT_IF_PRESENT'})
        op_type.validate()
        self.assertTrue(True)

    def testPutIfVersionOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT_IF_VERSION'})
        op_type.validate()
        self.assertTrue(True)

    def testBadTypeOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'GET'})
        self.assertRaises(IllegalArgumentException, op_type.validate)

    def testNoneOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: None})
        self.assertRaises(IllegalArgumentException, op_type.validate)

    def testNoStringOperationType(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: True})
        self.assertRaises(IllegalArgumentException, op_type.validate)

    def testMinimalOperation(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT'})
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row})
        op.validate()
        self.assertTrue(True)

    def testDictRowMinimalOperation(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT'})
        row = {
            'id': 100,
            'name': 'John Doe',
            'age': 25}
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row})
        op.validate()
        self.assertTrue(True)

    def testAbortIfUnsuccessfulOperation(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT'})
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_ABORT_IF_UNSUCCESSFUL: True})
        op.validate()
        self.assertTrue(True)

    def testVersionOperation(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT_IF_VERSION'})
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver})
        op.validate()
        self.assertTrue(True)

    def testReturnChoiceOperation(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT_IF_VERSION'})
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver,
            ONDB_RETURN_CHOICE: 'ALL'})
        op.validate()
        self.assertTrue(True)

    def testBadOperationTypeOperation(self):
        op_type = {ONDB_OPERATION_TYPE: 'PUT_IF_YOU_WANT'}
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testNoOperationTypeOperation(self):
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_ROW: row,
            ONDB_VERSION: ver})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testNoTableNameOperation(self):
        op_type = {ONDB_OPERATION_TYPE: 'PUT'}
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testBadRowOperation(self):
        op_type = {ONDB_OPERATION_TYPE: 'PUT_IF_YOU_WANT'}
        row = 'name: John Doe'
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testNoRowOperation(self):
        op_type = {ONDB_OPERATION_TYPE: 'PUT'}
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_VERSION: ver})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testBadVersionOperation(self):
        op_type = {ONDB_OPERATION_TYPE: 'PUT_IF_YOU_WANT'}
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = '$#@%$#'
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testNoVersionOperation(self):
        op_type = {ONDB_OPERATION_TYPE: 'PUT_IF_VERSION'}
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testBadAbortIfUnsuccessfulOperation(self):
        op_type = {ONDB_OPERATION_TYPE: 'DELETE_IF_VERSION'}
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver,
            ONDB_ABORT_IF_UNSUCCESSFUL: 1})
        self.assertRaises(IllegalArgumentException, op.validate)

    def testBadReturnChoiceOperation(self):
        op_type = OperationType({ONDB_OPERATION_TYPE: 'PUT_IF_VERSION'})
        row = Row({
            'id': 100,
            'name': 'John Doe',
            'age': 25})
        ver = bytearray('$#@%$#')
        op = Operation({
            ONDB_TABLE_NAME: 'table1',
            ONDB_OPERATION: op_type,
            ONDB_ROW: row,
            ONDB_VERSION: ver,
            ONDB_RETURN_CHOICE: 'SOME'})
        self.assertRaises(IllegalArgumentException, op.validate)


if __name__ == '__main__':
    unittest.main()