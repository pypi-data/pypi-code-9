# -*- coding: utf-8 -*-
import pytest
import exceptions
from glb.models.balancer import Balancer
from glb.models.frontend import Frontend
from glb.models.backend import Backend
from glb.models.entrypoint import Entrypoint


class TestBalancer:

    def test_get_balancer(self, db, balancer):
        res = db.get_balancer(balancer.name)
        assert res.name == balancer.name

        with pytest.raises(TypeError) as excinfo:
            db.get_balancer()
        assert excinfo.type == exceptions.TypeError

        res = db.get_balancer('demo')
        assert res is None

    def test_get_balancer_list(self, db, balancer):
        res = db.get_balancer_list()
        assert len(res) != 0
        assert isinstance(res[0], Balancer)

    def test_save_balancer(self, db):
        data = {
            "backends": [{
                "tag": "v1.0",
                "address": "10.0.80.8",
                "port": 80}],
            "entrypoints": [{
                "certificate": {
                    "private_key": "1234",
                    "public_key_certificate": "5678",
                    "certificate_chain": "9012"},
                "cipher": "123456789",
                "domain": "www.guokr.com",
                "protocol": "https",
                "port": 443}],
            "frontend": {
                "port": 80,
                "protocol": "http"},
            "name": "test"}
        balancer_name = data.get('name')
        frontend = Frontend.create(**data.get('frontend'))
        backends = [Backend.create(**b) for b in data.get('backends')]
        entrypoints = [Entrypoint.create(**e) for e in data.get('entrypoints')]
        balancer = Balancer.create(name=balancer_name,
                                   frontend=frontend,
                                   backends=backends,
                                   entrypoints=entrypoints)
        res = db.save_balancer(balancer)
        assert res is not None
        res = db.get_balancer(balancer.name)
        assert res.name == balancer.name
        assert res.frontend.protocol == balancer.frontend.protocol
        assert len(res.backends) == len(balancer.backends)
        assert len(res.entrypoints) == len(balancer.entrypoints)

        with pytest.raises(TypeError) as excinfo:
            db.save_balancer()
            assert excinfo.type == exceptions.TypeError

        res = db.save_balancer('')
        assert res is None

    def test_delete_balancer(self, db, balancer):
        res = db.delete_balancer(balancer.name)
        assert res is True

        with pytest.raises(TypeError) as excinfo:
            db.delete_balancer()
            assert excinfo.type == exceptions.TypeError

        res = db.delete_balancer('not exists')
        assert res is False
