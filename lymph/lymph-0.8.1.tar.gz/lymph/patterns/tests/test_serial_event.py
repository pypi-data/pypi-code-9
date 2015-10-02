import uuid
import kombu

import lymph

from lymph.events.kombu import KombuEventSystem
from lymph.discovery.static import StaticServiceRegistryHub
from lymph.testing import LymphIntegrationTestCase, AsyncTestsMixin
from lymph.patterns.serial_events import serial_event
from lymph.config import Configuration


class TestInterface(lymph.Interface):
    def __init__(self, *args, **kwargs):
        super(TestInterface, self).__init__(*args, **kwargs)
        self.collected_events = []

    @serial_event('foo', key=lambda e: 1)
    def on_foo(self, event):
        self.collected_events.append(event)


class SerialEventIntegrationTest(LymphIntegrationTestCase, AsyncTestsMixin):
    use_zookeeper = True

    def setUp(self):
        super(SerialEventIntegrationTest, self).setUp()
        self.discovery_hub = StaticServiceRegistryHub()
        self.exchange_name = 'test-%s' % uuid.uuid4()
        self.the_container, self.the_interface = self.create_container(TestInterface, 'test', config=Configuration({
            'components': {
                'SerialEventHandler': {
                    'zkclient': {
                        'class': 'kazoo.client:KazooClient',
                        'hosts': self.hosts,
                    }
                }
            }
        }))
        self.lymph_client = self.create_client()

    def tearDown(self):
        super(SerialEventIntegrationTest, self).tearDown()
        connection = self.get_kombu_connection()
        exchange = kombu.Exchange(self.exchange_name)
        exchange(connection).delete()

    def get_kombu_connection(self):
        return kombu.Connection(transport='amqp', host='127.0.0.1')

    def create_event_system(self, **kwargs):
        return KombuEventSystem(self.get_kombu_connection(), self.exchange_name)

    def create_registry(self, **kwargs):
        return self.discovery_hub.create_registry(**kwargs)

    def received_check(self, n):
        def check():
            return len(self.the_interface.collected_events) == n
        return check

    def test_emit(self):
        self.lymph_client.emit('foo', {})
        self.assert_eventually_true(self.received_check(1), timeout=10)
        self.assertEqual(self.the_interface.collected_events[0].evt_type, 'foo')
