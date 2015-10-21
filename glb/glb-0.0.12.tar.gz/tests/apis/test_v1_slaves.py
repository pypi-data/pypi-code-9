# -*- coding: utf-8 -*-

from flask import url_for


class TestSlaves:

    def test_get(self, testapp):
        res = testapp.get(url_for('v1.slaves'))
        assert len(res.json) == 0
        assert res.status_code == 200

    def test_get02(self, testapp, slave):
        res = testapp.get(url_for('v1.slaves'))
        assert len(res.json) == 1
        assert res.status_code == 200
        assert res.json[0]['address'] == slave.address
