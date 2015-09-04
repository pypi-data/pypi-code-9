from . import Block
import re

class BlockCloud(Block):
    validation = '^[A-Z]{3}\d{3}'
    name = 'cloud'
    patterns = {
        'few': [('^FEW\d{3}', '_ceiling')],
        'scattert': [('^SCT\d{3}', '_ceiling')],
        'broken': [('^BKN\d{3}', '_ceiling')],
        'overcast': [('^OVC\d{3}', '_ceiling')],
        'clouds': [('CB$|TCU$', '_cloud')]
    }

    def _cloud(self, c):
        if c == 'CB':
            return 'Cumulunimbus'
        if c == 'TCU':
            return 'Towering Cumulus'
        return "unknown"

    def _ceiling(self, c):
        number = re.findall(r'\d+', c)
        return int(number[0]) * 100