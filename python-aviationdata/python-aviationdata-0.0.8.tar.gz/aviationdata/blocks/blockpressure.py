from . import Block

class BlockPressure(Block):
    validation = '^Q\d{3,4}$'
    name = 'pressure'
    patterns = {
        'qnh': [('\d{3,4}', '_qnh')],
    }

    def _qnh(self, q):
        return int(q)