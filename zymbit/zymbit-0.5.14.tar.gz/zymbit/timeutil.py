import datetime
import logging

# it's impossible that "now" is less than this datetime
# we know we are out of sync with real time if we ever
# get a time value less than this
MIN_DT = datetime.datetime(2014, 7, 25, 17, 00, 00)  # Zymbit est date, UTC

LONG_TIME_AGO = datetime.datetime(1, 1, 1)  # a really long time ago


def now():
    return datetime.datetime.utcnow()


def timestamp(dt=None):
    if dt is None:
        dt = now()

    return dt.isoformat('T')


def get_sleep_time(seconds, start):
    """
    Wait at most the given number of seconds from the initial time given
    :param seconds: float - number of seconds to wait
    :param start: datetime - the start time
    :return: float - time to wait
    """
    _now = now()
    delta = _now - start
    diff = delta.seconds + (1.0 * delta.microseconds / 1e6)
    wait = max(0, seconds - diff)

    # print 'start={}, _now={}, delta={}, diff={}, wait={}'.format(start, _now, delta, diff, wait)

    return wait


class MillisDatetime(object):
    def __init__(self, millis):
        self.last_millis = None
        self.initial = None

        self.set_initial(millis)

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def get_time(self, millis):
        if millis < self.last_millis:
            self.logger.info(
                'time rolled over, last_millis={}, millis={}'.format(
                    self.last_millis, millis))

            self.set_initial(millis)

        delta = datetime.timedelta(milliseconds=millis)
        return self.initial + delta

    def set_initial(self, millis):
        delta = datetime.timedelta(milliseconds=millis)
        self.initial = now() - delta

        self.last_millis = millis
