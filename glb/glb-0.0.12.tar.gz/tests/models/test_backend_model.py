# -*- coding: utf-8 -*-
import pytest
import exceptions
from glb.models.backend import Backend


class TestBackend:

    def test_get_backend_list(self, db, balancer):
        res = db.get_backend_list(balancer.name)
        assert len(res) != 0
        assert isinstance(res[0], Backend)

        with pytest.raises(TypeError) as excinfo:
            res = db.get_backend_list()
            assert excinfo.type == exceptions.TypeError

        res = db.get_backend_list(balancer_name='')
        assert len(res) == 0

    def test_save_or_update_backend(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.save_or_update_backend()
            assert excinfo.type == exceptions.TypeError

        res = db.save_or_update_backend('', balancer.name)
        assert res is None

        data = {"address": "10.0.80.8", "port": 5432, "tag": "v1.0"}
        backend = Backend.create(**data)

        res = db.save_or_update_backend(backend, '')
        assert res is None

        res = db.save_or_update_backend(backend, balancer.name)
        assert res == backend

    def test_delete_backend(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.delete_backend()
            assert excinfo.type == exceptions.TypeError

        res = db.delete_backend(
            balancer_name='',
            address='',
            port=0)
        assert res is False

        res = db.delete_backend(
            balancer.name,
            balancer.backends[0].address,
            balancer.backends[0].port)
        assert res is True

    def test_delete_backend_by_tag(self, db, balancer):
        res = db.get_backend_list(balancer.name)
        assert len(res) != 0

        res = db.delete_backend_by_tag(
            balancer.name,
            balancer.backends[0].tag)
        assert res is True

        res = db.get_backend_list(balancer.name)
        assert len(res) == 0

    def test_delete_all_backend(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.delete_all_backend()
            assert excinfo.type == exceptions.TypeError

        res = db.delete_all_backend(balancer_name='')
        assert res is False

        res = db.delete_all_backend(balancer.name)
        assert res is True
