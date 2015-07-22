# -*- coding: utf-8 -*-

from flask import url_for


class TestFrontend:

    def test_get(self, testapp, balancer):
        res = testapp.get(url_for('v1.balancer_balancer_name_frontend',
                                  balancer_name=balancer.name))
        assert res.status_code == 200
        assert res.json['protocol'] == balancer.frontend.protocol

    def test_put(self, testapp, balancer):
        data = dict(protocol="http")
        res = testapp.put_json(url_for('v1.balancer_balancer_name_frontend',
                                       balancer_name=balancer.name), data)
        assert res.status_code == 200
        assert res.json is True
