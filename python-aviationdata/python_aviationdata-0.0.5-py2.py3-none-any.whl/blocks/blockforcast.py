from datetime import datetime, date
import pytz
from . import Block

class BlockForcast(Block):
    validation = '^TEMPO$|^BECMG$|^FM|^\d{4}/\d{4}$'
    name = 'forcast'
    patterns = {
        'type': [('^TEMPO$|^BECMG$|^FM', '_type')],
        'time': [('^\d{4}/\d{4}$', '_time'), ('\d{4}$', '_time_from')],

    }

    def _type(self, t):
        if t == 'TEMPO':
            return "temporary"
        if t == 'BECMG':
            return "becoming"
        if t == 'FM':
            return "from"
        return t

    def _time_from(self, t):
        from_date = datetime(date.today().year, date.today().month, date.today().day, int(t[0:2]), int(t[2:4]), tzinfo=pytz.utc)
        return from_date.isoformat()

    def _time(self, t):
        x = t.split('/')

        from_day = int(x[0][0:2])
        from_hour = int(x[0][2:4])
        to_day = int(x[1][0:2])
        to_hour = int(x[1][2:4])

        from_date = datetime(date.today().year, date.today().month, from_day, from_hour, tzinfo=pytz.utc)
        to_date = datetime(date.today().year, date.today().month, to_day, to_hour, tzinfo=pytz.utc)

        return {
            'from': from_date.isoformat(),
            'to': to_date.isoformat()
        }