# -*- coding: utf-8 -*-
import pytest
import exceptions
from glb.models.slave import Slave


class TestSlave:

    def test_get_slave(self, db, slave):
        res = db.get_slave(slave.address)
        assert res.address == slave.address

        with pytest.raises(TypeError) as excinfo:
            res = db.get_slave()
            assert excinfo.type == exceptions.TypeError

        res = db.get_slave(address='not exits')
        assert res is None

    def test_get_slave_list(self, db, slave):
        res = db.get_slave_list()
        assert len(res) == 1
        assert res[0].address == slave.address

    def test_save_slave(self, db):
        with pytest.raises(TypeError) as excinfo:
            db.save_slave()
            assert excinfo.type == exceptions.TypeError

        slave = Slave(address='127.0.0.1')
        redis_slave = db.save_slave(slave)
        assert slave.address == redis_slave.address
