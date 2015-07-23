# -*- coding: utf-8 -*-

from flask import url_for


class TestBalancerName:

    def test_get(self, testapp, balancer):
        res = testapp.get(url_for('v1.balancer_balancer_name',
                                  balancer_name=balancer.name))
        assert res.status_code == 200
        assert res.json['name'] == balancer.name

    def test_delete(self, testapp, balancer):
        res = testapp.delete(url_for('v1.balancer_balancer_name',
                                     balancer_name=balancer.name))
        assert res.status_code == 200
        assert res.json == True
