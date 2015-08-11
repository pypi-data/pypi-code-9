import datetime
import json
import logging

from zymbit.exceptions import ConnectionError

from zymbit.timeutil import LONG_TIME_AGO, now, timestamp

from zymbit.compat.console import Console


# interval to send a message that connection is down
CONNECTION_ERROR_INTERVAL = datetime.timedelta(seconds=30)


class ConsoleData(object):
    def __init__(self, read_callback=None):
        self.last_acquire = LONG_TIME_AGO

        self.console = Console()

        self._read_callback = read_callback or self.read_callback

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def read_callback(self, line):
        try:
            reading = json.loads(line)
        except ValueError, exc:
            self.logger.error('Unable to parse JSON: {!r}'.format(line))
        else:
            reading['timestamp'] = timestamp()
            return reading

    def get_readings(self):
        _now = now()
        readings = []

        try:
            payload = self.console.recv()
        except ConnectionError, exc:
            if _now - self.last_acquire >= CONNECTION_ERROR_INTERVAL:
                self.logger.exception(exc)
                self.logger.error('Unable to get data from arduino since {}'.format(
                    timestamp(self.last_acquire)))

            return

        self.last_acquire = _now

        self.logger.debug('payload={!r}'.format(payload))

        for line in payload.strip().splitlines():
            reading = self._read_callback(line)
            if reading is not None:
                readings.append(reading)

        return readings

    def loop(self):
        return self.get_readings()
