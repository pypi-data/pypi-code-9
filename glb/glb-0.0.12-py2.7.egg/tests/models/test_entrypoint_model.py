# -*- coding: utf-8 -*-
import pytest
import exceptions
from glb.models.entrypoint import Entrypoint


class TestEntrypoint:

    def test_get_entrypoint_list(self, db, balancer):
        res = db.get_entrypoint_list(balancer.name)
        assert len(res) != 0
        assert isinstance(res[0], Entrypoint)

        with pytest.raises(TypeError) as excinfo:
            res = db.get_entrypoint_list()
            assert excinfo.type == exceptions.TypeError

        res = db.get_entrypoint_list(balancer_name='')
        assert len(res) == 0

    def test_save_or_update_entrypoint(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.save_or_update_entrypoint()
            assert excinfo.type == exceptions.TypeError

        res = db.save_or_update_entrypoint('', balancer.name)
        assert res is None

        data = {
            "certificate": {
                "private_key": "1234",
                "public_key_certificate": "5678",
                "certificate_chain": "9012"},
            "cipher": "123456789",
            "domain": "www.guokr.com",
            "protocol": "https",
            "port": 443}
        entrypoint = Entrypoint.create(**data)
        res = db.save_or_update_entrypoint(entrypoint, '')
        assert res is None
        res = db.save_or_update_entrypoint(entrypoint, balancer.name)
        assert res == entrypoint

    def test_delete_entrypoint(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.delete_entrypoint()
            assert excinfo.type == exceptions.TypeError

        res = db.delete_entrypoint(
            balancer_name='',
            domain=balancer.entrypoints[0].domain,
            port=balancer.entrypoints[0].port)
        assert res is False

        res = db.delete_entrypoint(
            balancer.name,
            domain=balancer.entrypoints[0].domain,
            port=balancer.entrypoints[0].port)
        assert res is True

    def test_delete_all_entrypoint(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.delete_all_entrypoint()
            assert excinfo.type == exceptions.TypeError

        res = db.delete_all_entrypoint(balancer_name='')
        assert res is False

        res = db.delete_all_entrypoint(balancer.name)
        assert res is True
        res = db.get_entrypoint_list(balancer.name)
        assert len(res) == 0
