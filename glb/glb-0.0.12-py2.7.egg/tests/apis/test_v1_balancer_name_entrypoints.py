# -*- coding: utf-8 -*-

from flask import url_for


class TestEntrypoints:

    def test_get(self, testapp, balancer):
        res = testapp.get(url_for('v1.balancer_balancer_name_entrypoints',
                                  balancer_name=balancer.name))
        assert res.status_code == 200

    def test_post01(self, testapp, balancer):
        res = testapp.post_json(url_for(
            'v1.balancer_balancer_name_entrypoints',
            balancer_name=balancer.name), [])
        assert res.status_code == 201
        assert res.json is True

    def test_post02(self, testapp, balancer):
        data = [{'domain': 'www.zaih.com',
                 'cipher': '1234',
                 'protocol': 'http',
                 'port': 7670,
                 'certificate': {
                     'public_key_certificate': '5678',
                     'certificate_chain': '9012',
                     'private_key': '1234'}}]
        res = testapp.get(url_for('v1.balancer_balancer_name_entrypoints',
                                  balancer_name=balancer.name))
        pre_length = len(res.json)
        res = testapp.post_json(url_for(
            'v1.balancer_balancer_name_entrypoints',
            balancer_name=balancer.name), data)
        assert res.status_code == 201
        assert res.json is True
        res = testapp.get(url_for('v1.balancer_balancer_name_entrypoints',
                                  balancer_name=balancer.name))
        pos_length = len(res.json)
        assert pos_length == (pre_length + 1)

    def test_put(self, testapp, balancer):
        res = testapp.put_json(url_for('v1.balancer_balancer_name_entrypoints',
                                       balancer_name=balancer.name),
                               [])
        assert res.status_code == 200
        assert res.json is True

    def test_delete01(self, testapp, balancer):
        res = testapp.delete(url_for('v1.balancer_balancer_name_entrypoints',
                                     balancer_name=balancer.name,
                                     domain=balancer.entrypoints[0].domain,
                                     port=balancer.entrypoints[0].port))
        assert res.status_code == 200
        assert res.json is True

    def test_delete02(self, testapp, balancer):
        res = testapp.delete(url_for('v1.balancer_balancer_name_entrypoints',
                                     balancer_name=balancer.name,
                                     del_type='all'))
        assert res.status_code == 200
        assert res.json is True
