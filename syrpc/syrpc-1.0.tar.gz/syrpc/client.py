# -*- coding: UTF-8 -*-

"""RPC client implementation for SyRPC middleware"""

# System imports
import json
import kombu
import socket
import uuid

# Project imports
import syrpc.rpc_base as base
import syrpc.common   as cmn


class Client(base.RPCBase):
    """Initiates a connection to AMQ. The RPC objects are not thread-safe,
    please use a instance per Thread.

    :type  settings: dict
    :param settings: Dictionary holding settings:

    - app_name        (mandatory) Every server this the same app name
                                  must support the same request-types
    - amq_host        (mandatory)
    - amq_virtualhost (optional)
    - amq_user        (optional)
    - amq_password    (optional)
    - amq_transport   (optional) Used for unittesting (ie memory
                                 transport)
    - amq_ttl         (optional) Time to live for queues
    - amq_msg_ttl     (optional) Time to live for messages
    - amq_num_queues  (optional) Number of queue (default 64)
    """

    def __init__(self, settings):
        """Constructor"""
        super(Client, self).__init__(settings)
        self.consumer = kombu.Consumer(
            channel=self.result_channel,
            callbacks=[self.on_result],
            auto_declare=False,
        )

    def put_request(self, type_, data):
        """Puts request with given type and data to AMQ request queue.

        :type  type_: string
        :param type_: Type of the request represents the service/method/function
                      that should be called.
        :type   data: dict
        :param  data: Data to send to the server.
        """
        result_id = uuid.uuid4()
        body = {
            'result_id': str(result_id),
            'type':      type_.strip(),
            'data':      data
        }
        self.request_queue.put(
            message=body,
        )
        cmn.lg.debug(
            "Client put request for result %s "
            "on %s" % (result_id, self.request_queue)
        )
        return result_id

    def get_result(self, result_id, timeout=None):
        """Wait for a result. Blocks unit a result arrives or the
        timeout has expired. If no result has arrived when timeout
        is expired get_result raises a EmptyException.

        :type  result_id: string
        :param result_id: get the result for this result id
        :type  timeout: float
        :param timeout: Timeout after which get_result will raise
                        EmptyException()
        """
        routing_key   = str(result_id)
        hash_id       = cmn.get_hash(routing_key, self.amq_num_queues)
        result_queue  = self.get_result_queue(index=hash_id)
        self.wait_id  = routing_key
        self.consumer.add_queue(result_queue)
        cmn.lg.debug("Queue %s in queues: %s" % (
            result_queue, len(self.consumer.queues)
        ))
        self.consumer.consume()
        cmn.lg.debug(
            "Client waiting for result for "
            "request %s on %s during %ss" % (
                hash_id, result_queue, timeout
            )
        )
        while self.response is None:
            try:
                self.amq_connection.drain_events(timeout=timeout)
            except socket.timeout:
                cmn.lg.error("Client hit the fan after %ss" % timeout)
                raise cmn.EmptyException()

        cmn.lg.debug("Client got %s from AMQ" % result_id)
        cmn.lg.debug("Client returning %s" % self.response)
        res = self.response
        self.response = None
        return res

    def on_result(self, body, message):
        """Handles the reception of a result over AMQ."""
        cmn.lg.debug("Client received %s/%s" % (body, message))
        message_body = message.body.decode(message.content_encoding)
        body = json.loads(message_body, message.content_encoding)
        if self.wait_id == body['result_id']:
            cmn.lg.debug("Client received %s" % self.wait_id)
            self.response = body
            message.ack()
            self.consumer.queues = []
        else:
            cmn.lg.warn(
                "Client received a wrong result %s" % body['result_id']
            )
            message.reject(requeue=True)
            self.response = None
