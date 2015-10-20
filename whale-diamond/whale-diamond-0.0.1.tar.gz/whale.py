"""
[Whale Monitoring](http://www.whale.io/) is a open-source monitoring
service.

#### Dependencies

  * [whaleapi]

#### Configuration

Enable handler

  * handlers = whale.WhaleHandler,

  * api_key = WHALE_API_KEY

  * queue_size = [optional | 20]

"""

from diamond.handler.Handler import Handler
import logging
from collections import deque

try:
    import whaleapi
    from whaleapi.utils import converter
except ImportError:
    whaleapi = None


class WhaleHandler(Handler):

    def __init__(self, config=None):
        Handler.__init__(self, config)
        logging.debug("Initialized Whale Monitoring handler.")

        if whaleapi is None:
            logging.error("Failed to load whaleapi module.")
            return

        self.api_token = self.config.get('api_token', '')
        self.api_host = self.config.get('api_host', '')
        self.queue_size = self.config.get('queue_size', 20)

        whaleapi.initialize(self.api_token, self.api_host)
        self.api = whaleapi.api
        self.queue = deque([])

    def get_default_config_help(self):
        """
        Help text
        """
        config = super(WhaleHandler, self).get_default_config_help()

        config.update({
            'api_token': 'API token',
            'api_host': 'API host',
            'queue_size': 'Bundle metrics in requests',
        })

        return config

    def get_default_config(self):
        """
        Return default config for the handler
        """
        config = super(WhaleHandler, self).get_default_config()

        config.update({
            'api_token': '',
            'api_host': '',
            'queue_size': 20,
        })

        return config

    def process(self, metric):
        """
        Process metric by sending it to whale api
        """

        self.queue.append(metric)
        if len(self.queue) >= self.queue_size:
            self._send()

    def flush(self):
        """
        Flush metrics
        """

        self._send()

    def _send(self):
        """
        Take metrics from queue and send it to whale API
        """
        metrics = []

        while len(self.queue) > 0:
            metric = self.queue.popleft()

            path = '%s.%s' % (
                metric.getCollectorPath(),
                metric.getMetricPath()
            )
            timestamp, value, host = metric.timestamp, metric.value, metric.host
            metric_type = metric.metric_type.lower()

            logging.debug(
                "Sending.. metric[%s], value[%s], timestamp[%s]",
                path,
                value,
                timestamp
            )

            metrics.append({
                'metric': path,
                'host': host,
                'metrric_type': metric_type,
                'points': [
                    {'timestamp': converter.epoch_to_iso_8601(timestamp), 'value': value}
                ]
            })

        if len(metrics) > 0:
            self.api.Metric.send(metrics=metrics)
