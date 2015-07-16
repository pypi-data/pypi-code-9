from lisa_api.api.speak import base
from kombu import Connection, Exchange, Queue
from lisa_api.lisa.configuration import CONF as config
from lisa_api.lisa.logger import logger


class Rabbitmq(base.SpeakBase):
    def send_message(self, message, zone='all', source='api'):
        """Send a text message.

        :param message: A string containing the message
        :type message: str
        :param zone: The zone where the message will be sent
        :type lang: str
        :param source: The zone where the message came from
        :type lang: str
        :returns: True or False.
        :rtype: Boolean
        """
        if not zone:
            zone = 'all'
        lisa_exchange = Exchange('lisa', 'topic', durable=True)
        client_queue = Queue('client', exchange=lisa_exchange, routing_key='client.%s' % zone)

        rabbitmq_creds = {
            'user': config.rabbitmq.user,
            'password': config.rabbitmq.password,
            'host': config.rabbitmq.host,
        }

        with Connection('amqp://{user}:{password}@{host}//'.format(**rabbitmq_creds),
                        transport_options={'confirm_publish': True}) as conn:
            producer = conn.Producer(serializer='json')
            producer.publish({'message': message, 'zone': zone, 'source': source},
                             exchange=lisa_exchange, routing_key='client.%s' % zone,
                             declare=[client_queue])
            logger.debug(msg='Publishing a message on %s, with %s' %
                             ('client.' + zone,
                              {'message': message, 'zone': zone, 'source': source}))
            return True
