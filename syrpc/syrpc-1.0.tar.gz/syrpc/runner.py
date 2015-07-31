# -*- coding: UTF-8 -*-
# pylint: disable=super-init-not-called

"""Test module with example implementations"""

# System import
import logging
import sys
# Project imports
import syrpc.common as cmn
import syrpc.server as srv
import syrpc.client as cl


def setup_logger():
    """Sets up loggers"""
    root = logging.getLogger()
    rpc_logger = root.getChild('syrpc')
    rpc_logger.setLevel(logging.DEBUG)
    rpc_log_handler = logging.StreamHandler(sys.stdout)
    root.addHandler(rpc_log_handler)


def get_settings():
    """Returns settings to be used for clients and servers"""
    return {
        'app_name':        'syrpc',
        'amq_virtualhost': '/',
        'amq_host':        'localhost',
        'amq_user':        'guest',
        'amq_password':    'guest',
    }


def run_server_forever():
    """Runs the sever forever"""
    run_server(True)


def run_server(forever=False):
    """Runs server"""
    settings = get_settings()
    setup_logger()
    rpc_server = srv.Server(settings)
    if forever:
        while True:
            serve_one(rpc_server)
    else:
        serve_one(rpc_server)


def serve_one(rpc_server):
    """Serve one request"""
    (type_, result_id, data) = rpc_server.get_request()
    cmn.lg.info("Server received request: %s" % (result_id))
    if type_ == 'echo':
        rpc_server.put_result(
            result_id=result_id, data=data
        )
        cmn.lg.debug("Server put result: {0}".format(result_id))
    else:
        cmn.lg.debug("Server got no request within timeout")


def run_client():
    """Runs client"""
    settings = get_settings()
    setup_logger()
    rpc_client = cl.Client(settings)
    type_ = 'echo'
    data = [{'foo': 'bar'}, {'baz': 9001}]
    result_id = rpc_client.put_request(
        type_=type_, data=data,
    )
    result = rpc_client.get_result(result_id=result_id)
    cmn.lg.debug("Client received data for result {0}: {1}".format(
        result_id, result
    ))
    if result['data'] == data:
        sys.exit(0)
    else:
        print("Wrong data received")
        sys.exit(1)
