
import logging
import pytest
import random
import time

from logging import StreamHandler

from elogging.handlers.riemann import RiemannHandler

@pytest.fixture
def logger():
    RIEMANN_EVENT_FORMAT = '%(asctime)-15s [EVENT] %(event)s %(message)s'
    logging.basicConfig(format=RIEMANN_EVENT_FORMAT)

    riemann_handler = RiemannHandler()
    stream_handler = StreamHandler()

    l = logging.getLogger('foo.bar')
    l.addHandler(riemann_handler)
    l.addHandler(stream_handler)
    l.setLevel(logging.INFO)
    return l

def test_riemann_handler(logger): 
    logger.info('test riemann handler...',
                extra={'event':{'host': 'localhost',
                                'service': 'httpd',
                                'state': 'ok',
                                'time': int(time.time()),
                                'description': 'seems good',
                                'tags': ['rate', 'fooproduct'],
                                'metric': random.uniform(60.00, 100.00)}})

