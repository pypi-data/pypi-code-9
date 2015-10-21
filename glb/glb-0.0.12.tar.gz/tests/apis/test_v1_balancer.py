# -*- coding: utf-8 -*-

from flask import url_for


class TestBalancer:

    def test_get01(self, testapp):
        res = testapp.get(url_for('v1.balancer'))
        assert res.status_code == 200
        assert len(res.json) == 0

    def test_get02(self, testapp, balancer):
        res = testapp.get(url_for('v1.balancer'))
        assert res.status_code == 200
        assert len(res.json) == 1
        assert res.json[0]['name'] == balancer.name

    def test_post01(self, testapp):
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
            "name": "test01"}
        res = testapp.post_json(url_for('v1.balancer'), data)
        assert res.status_code == 201
        assert res.json['name'] == 'test01'

    def test_post02(self, testapp):
        data = {
            "backends": [{
                "tag": "v1.0",
                "address": "10.0.80.8",
                "port": 80}],
            "frontend": {
                "port": 80,
                "protocol": "http"},
            "name": "test02"}
        res = testapp.post_json(url_for('v1.balancer'), data)
        assert res.status_code == 201
        assert res.json['name'] == 'test02'
