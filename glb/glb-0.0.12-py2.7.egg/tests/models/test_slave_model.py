# -*- coding: utf-8 -*-
import pytest
import exceptions
from glb.models.slave import Slave


class TestSlave:

    def test_get_slave(self, db, slave):
        res = db.get_slave(slave.address)
        res.sync_time
        assert res.address == slave.address

        with pytest.raises(TypeError) as excinfo:
            res = db.get_slave()
            assert excinfo.type == exceptions.TypeError

        res = db.get_slave(address='not exits')
        assert res is None

    def test_get_slave_list(self, db, slave):
        res = db.get_slave_list()
        pre_length = len(res)
        slave_1 = Slave.create(address='192.168.0.1')
        db.save_slave(slave_1)
        res = db.get_slave_list()
        pos_length = len(res)
        assert pre_length == (pos_length - 1)

    def test_save_slave(self, db):
        with pytest.raises(TypeError) as excinfo:
            db.save_slave()
            assert excinfo.type == exceptions.TypeError

        slave = Slave.create(address='127.0.0.1')
        res = db.save_slave(slave)
        assert slave.address == res.address
