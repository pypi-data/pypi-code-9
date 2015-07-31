# -*- coding: UTF-8 -*-

"""RPC base class for SyRPC middleware"""

# System imports
import kombu

# Project imports
import syrpc.common    as cmn
import syrpc.constants as const


class RPCBase(object):
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
        self.app_name            = settings['app_name']
        if 'amq_virtualhost' in settings:  # pragma: no cover
            self.amq_virtualhost = settings['amq_virtualhost']
        else:  # pragma: no cover
            self.amq_virtualhost = const.AMQ.VIRTUALHOST
        # Queue TTL in seconds
        if 'amq_ttl' in settings:  # pragma: no cover
            self.amq_ttl = settings['amq_ttl']
        else:  # pragma: no cover
            self.amq_ttl = const.AMQ.TTL
        # Message TTL in seconds
        if 'amq_msg_ttl' in settings:  # pragma: no cover
            self.amq_msg_ttl = settings['amq_msg_ttl']
        else:  # pragma: no cover
            self.amq_msg_ttl = const.AMQ.MSG_TTL
        if 'amq_num_queues' in settings:  # pragma: no cover
            self.amq_num_queues = settings['amq_num_queues']
        else:  # pragma: no cover
            self.amq_num_queues = const.AMQ.NUM_QUEUES
        if 'amq_user' in settings:  # pragma: no cover
            self.amq_user = settings['amq_user']
        else:  # pragma: no cover
            self.amq_user = "guest"
        if 'amq_password' in settings:  # pragma: no cover
            self.amq_password = settings['amq_password']
        else:  # pragma: no cover
            self.amq_password = "guest"
        if 'amq_transport' in settings:  # pragma: no cover
            self.amq_transport = settings['amq_transport']
        else:  # pragma: no cover
            self.amq_transport = None
        self.amq_host            = settings['amq_host']
        self.amq_connection      = None
        self.response            = None
        self.wait_id             = None
        self.result_channel      = None
        self.result_exchange     = None
        self.result_queues       = [None] * self.amq_num_queues
        self.init_amq_connection()
        self.setup_request_queue()
        self.setup_result_queues()

    def __del__(self):
        """Class destructor, closes connection to AMQ."""
        if self.amq_connection:
            self.amq_connection.close()
            cmn.lg.debug("Closed connection to AMQ")

    def init_amq_connection(self):
        """Initialises a connection to AMQ."""
        self.amq_connection = kombu.Connection(
            hostname=self.amq_host,
            userid=self.amq_user,
            password=self.amq_password,
            virtual_host=self.amq_virtualhost,
            transport=self.amq_transport,
        )
        self.amq_connection.connect()
        cmn.lg.debug(
            "Successfully connected to AMQ: %s" % self.amq_connection.connected
        )

    def setup_request_queue(self):
        """Sets up a work queue for handling requests.
        Uses exchange `direct`, with all the same exchange name, routing key
        and queue name."""
        self.request_queue = self.amq_connection.SimpleQueue(
            name=const.RPC.REQUEST_NAME.format(self.app_name),
            queue_opts=dict(auto_delete=False),
            exchange_opts=dict(auto_delete=False),
        )

    def setup_result_queues(self):
        """Sets up publish/subscribe queues for handling results."""
        self.result_channel  = self.amq_connection.channel()
        self.result_exchange = kombu.Exchange(
            name=const.RPC.RESULT_EXCHANGE_NAME.format(self.app_name),
            type=const.RPC.RESULT_EXCHANGE_TYPE,
            channel=self.result_channel,
        )

    def get_result_queue(self, index):
        """Creates or returns result queue for given index"""
        queue = self.result_queues[index]
        if queue:
            return queue
        else:
            queue = kombu.Queue(
                name=const.RPC.RESULT_QUEUE_NAME.format(self.app_name, index),
                channel=self.result_channel,
                exchange=self.result_exchange,
                routing_key=str(index),
                queue_arguments={
                    'x-expires':     self.amq_ttl     * 1000,
                    'x-message-ttl': self.amq_msg_ttl * 1000,
                },
            )
            queue.declare()
            self.result_queues[index] = queue
            return queue
