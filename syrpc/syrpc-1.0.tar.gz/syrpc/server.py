# -*- coding: UTF-8 -*-

"""RPC server implementation for SyRPC middleware"""

# System imports
import amqp.exceptions           as aexcept
import kombu

# Project imports
import syrpc.rpc_base as base
import syrpc.common   as cmn
from syrpc.common     import EmptyException
from syrpc.common     import QueueNotFoundException


class Server(base.RPCBase):
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
        super(Server, self).__init__(settings)
        self.producer = kombu.Producer(
            self.result_channel,
            exchange=self.result_exchange,
            auto_declare=False,
        )

    def get_request(self, timeout=None):
        """Wait for a request. Blocks until a request arrives or
        timeout has expired. If no request has arrived when timeout
        is expired get_request raises a EmptyException.

        :type  timeout: float
        :param timeout: Timeout after which get_request will raise
                        EmptyException()
        :returns: (type_, result_id, data) type_: type of the request,
                 result_id: result_id to put the result with, data:
                 request data

        Type of the request represents the service/method/function that
        should be called.
        """
        cmn.lg.debug("Server waiting for requests during %ss" % timeout)
        try:
            message = self.request_queue.get(block=True, timeout=timeout)
        except self.request_queue.Empty:
            raise EmptyException()
        except aexcept.NotFound as e:
            cmn.lg.critical("Server did not find queue: %s" % e)
            raise QueueNotFoundException(
                "Server did not find queue: %s" % e
            )
        cmn.lg.debug("Server received a request")
        message.ack()
        message   = message.decode()
        result_id = message['result_id']
        data      = message['data']
        type_     = message['type']
        return (type_, result_id, data)

    def put_result(self, result_id, data):
        """Puts a result to the AMQ result queue.

        :type  result_id: str
        :param result_id: the result id received with get_request"""
        str_result_id = str(result_id)
        hash_id      = cmn.get_hash(str_result_id, self.amq_num_queues)
        result_queue = self.get_result_queue(index=hash_id)
        body         = {
            'result_id': str_result_id,
            'data':      data,
        }
        self.producer.publish(
            body=body,
            routing_key=str(hash_id),
            exchange=self.result_exchange,
            declare=[result_queue],
        )
        cmn.lg.debug(
            "Server published result %s within %s" % (
                str_result_id,
                result_queue,
            )
        )
