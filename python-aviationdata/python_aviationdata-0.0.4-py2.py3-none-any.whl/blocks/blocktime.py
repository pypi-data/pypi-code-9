from . import Block
from datetime import datetime, date
import pytz

class BlockTime(Block):
    validation = '^\d{6}Z$|AUTO'
    name = 'time'
    patterns = {
        'time': [('\d{6}', '_time'), ('AUTO', '_time')],
        'auto_time': 'AUTO',
    }

    def _time(self, t):
        if t == 'AUTO':
            return date.today().isoformat()
        day = int(t[0:2])
        hour = int(t[2:4])
        minute = int(t[4:6])

        d = datetime(date.today().year, date.today().month, day, hour, minute, tzinfo=pytz.utc)

        return d.isoformat()