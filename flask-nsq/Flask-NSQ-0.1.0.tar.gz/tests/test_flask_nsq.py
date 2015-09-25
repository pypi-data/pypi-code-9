#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_flask-nsq
----------------------------------

Tests for `flask-nsq` module.
"""

import pytest
from flask_nsq import Nsq
from flask import Flask
from .integration_server import NsqdIntegrationServer
from gnsq import protocol as nsq
from gnsq import states, errors


def test_unset_clientlibrary():
    app = Flask(__name__)
    with pytest.raises(Exception):
        Nsq(app)


@pytest.fixture(scope='function')
def flaskapp():
    app = Flask(__name__)
    app.config['NSQ_CLIENT_TYPE'] = 'gnsq'
    return app


def test_daemon_connection(flaskapp):
    with NsqdIntegrationServer() as server:
        config = {
            'address': server.address,
            'http_port': server.http_port,
            'tcp_port': server.tcp_port
        }
        client = Nsq(flaskapp, config)
        client.daemon.connect()
        assert client.daemon.state == states.CONNECTED

        client.daemon.close()
        frame, error = client.daemon.read_response()
        assert frame == nsq.FRAME_TYPE_ERROR
        assert isinstance(error, errors.NSQInvalid)


def test_reader(flaskapp):
    with NsqdIntegrationServer() as server:

        class Accounting(object):
            count = 0
            total = 500
            error = None

        config = {
            'address': server.address,
            'http_port': server.http_port,
            'tcp_port': server.tcp_port
        }

        client = Nsq(flaskapp, config)
        client.daemon.connect()

        for _ in xrange(Accounting.total):
            client.daemon.publish_http('test', 'danger zone!')

        reader_config = {
            'nsqd_tcp_addresses': server.tcp_address,
            'max_in_flight': 100
        }
        reader = client.create_reader('test', 'test', reader_config)

        @reader.on_exception.connect
        def error_handler(reader, message, error):
            if isinstance(error, errors.NSQSocketError):
                return
            Accounting.error = error
            reader.close()

        @reader.on_message.connect
        def handler(reader, message):
            assert message.body == 'danger zone!'

            Accounting.count += 1
            if Accounting.count == Accounting.total:
                assert not reader.is_starved
                reader.close()

        # use the stored reader to start to test that it stored
        r = client.get_reader('test', 'test')
        r.start()

        if Accounting.error:
            raise Accounting.error

        assert Accounting.count == Accounting.total
