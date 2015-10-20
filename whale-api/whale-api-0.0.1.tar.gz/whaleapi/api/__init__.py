# flake8: noqa

# API settings
api_token = None
api_host = None

cacert = None
proxies = None
timeout = 3
max_timeouts = 3
max_retries = 3
backoff_period = 300
mute = True

from whaleapi.api.events import Event
from whaleapi.api.metrics import Metric
