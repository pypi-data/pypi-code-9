from datetime import datetime, date
import pytz
from . import Block


class BlockTemperature(Block):
    validation = '^M?\d{2}/M?\d{2}$|^T.\d{2}/\d{4}Z$'
    name = 'temperature'
    patterns = {
        'temperature': [('^M?\d{2}/M?\d{2}$', '_temp')],
        'temperature_forcast': ('^T.\d{2}/\d{4}Z$', '_temp_forcast'),
    }

    def _temp_forcast(self, t):
        x = t.split('/')
        temperature = int(x[0][2:4])
        type = 'minimum' if x[0][0:2] == 'TN' else 'maximum'
        temperature_date = datetime(date.today().year, date.today().month, int(x[1][0:2]), int(x[1][2:4]), tzinfo=pytz.utc)

        return {'type': type, 'temperature': temperature, 'time': temperature_date.isoformat()}

    def _temp(self, t):
        x = t.split('/')
        x = map(lambda y: 0 - int(y[1:3]) if y[0] == 'M' else int(y), x)
        return {'t':t,'temperature': x[0], 'dewpoint': x[1], 'spread': (x[0] - x[1])}