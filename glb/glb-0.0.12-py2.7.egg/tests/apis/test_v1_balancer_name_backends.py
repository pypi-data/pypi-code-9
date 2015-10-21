# -*- coding: utf-8 -*-

from flask import url_for


class TestBackends:

    def test_get(self, testapp, balancer):
        res = testapp.get(url_for('v1.balancer_balancer_name_backends',
                                  balancer_name=balancer.name))
        assert res.status_code == 200

    def test_post01(self, testapp, balancer):
        res = testapp.post_json(url_for('v1.balancer_balancer_name_backends',
                                        balancer_name=balancer.name),
                                [])
        assert res.status_code == 201
        assert res.json is True

    def test_post02(self, testapp, balancer):
        res = testapp.get(url_for('v1.balancer_balancer_name_backends',
                                  balancer_name=balancer.name))
        pre_length = len(res.json)
        data = [{"address": "10.0.80.8", "port": 5432, "tag": "v1.0"}]
        res = testapp.post_json(url_for('v1.balancer_balancer_name_backends',
                                        balancer_name=balancer.name),
                                data)
        assert res.status_code == 201
        assert res.json is True
        res = testapp.get(url_for('v1.balancer_balancer_name_backends',
                                  balancer_name=balancer.name))
        pos_length = len(res.json)
        assert pos_length == (pre_length + 1)

    def test_put(self, testapp, balancer):
        res = testapp.put_json(
            url_for('v1.balancer_balancer_name_backends',
                    balancer_name=balancer.name), [])
        assert res.status_code == 200
        assert res.json is True

    def test_delete01(self, testapp, balancer):
        res = testapp.delete(url_for('v1.balancer_balancer_name_backends',
                                     balancer_name=balancer.name,
                                     address=balancer.backends[0].address,
                                     port=balancer.backends[0].port))
        assert res.status_code == 200
        assert res.json is True

    def test_delete02(self, testapp, balancer):
        res = testapp.delete(url_for('v1.balancer_balancer_name_backends',
                                     balancer_name=balancer.name,
                                     tag=balancer.backends[0].tag))
        assert res.status_code == 200
        assert res.json is True
