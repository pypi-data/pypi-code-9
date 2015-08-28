import logging

logger = logging.getLogger(__name__)


class SendQueue:
    """
    Queues packets to send when transport can send
    """

    def __init__(self, transport, can_send_func=lambda: True, pre_process_func=lambda x: x):
        self._q = []
        self._transport = transport
        self._can_send = can_send_func
        self._pre_process = pre_process_func

    def send(self, packet=None):
        if packet:
            self._q.append(packet)
        if self._can_send():
            for each in self._q:
                each = self._pre_process(each)
                try:
                    self._transport.write(each)
                except Exception:
                    logger.exception("Exception caught")
                logger.info('----------- written to socket')

            self._q.clear()
        else:
            logger.info("---------- can't send")
