import itsdangerous
import calendar
import time


class Signer(itsdangerous.TimestampSigner):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('key_derivation', 'none')
        super(Signer, self).__init__(*args, **kwargs)

    def get_timestamp(self):
        return calendar.timegm(time.gmtime())
