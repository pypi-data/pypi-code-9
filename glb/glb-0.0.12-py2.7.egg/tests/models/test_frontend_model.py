# -*- coding: utf-8 -*-
import pytest
import exceptions
from glb.models.frontend import Frontend


class TestFront:

    def test_get_frontend(self, db, balancer):
        res = db.get_frontend(balancer.name)
        assert isinstance(res, Frontend)

        with pytest.raises(TypeError) as excinfo:
            res = db.get_frontend()
        assert excinfo.type == exceptions.TypeError

        res = db.get_frontend(balancer_name='not exits')
        assert res is None

    def test_save_frontend(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.save_frontend()
        assert excinfo.type == exceptions.TypeError

        res = db.save_frontend('', balancer.name)
        assert res is None

        frontend = Frontend.create(port=80, protocol='http')
        res = db.save_frontend(frontend, balancer.name)
        assert res.port != 80
        assert res.protocol == 'http'

    def test_delete_frontend(self, db, balancer):
        with pytest.raises(TypeError) as excinfo:
            db.delete_frontend()
        assert excinfo.type == exceptions.TypeError

        res = db.delete_frontend('not exits')
        assert res is False

        res = db.delete_frontend(balancer.name)
        assert res is True
