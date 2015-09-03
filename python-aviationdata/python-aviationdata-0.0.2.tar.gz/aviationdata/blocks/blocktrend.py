from . import Block

class BlockTrend(Block):
    validation = '^NOSIG$'
    name = 'trend'
    patterns = {
        'trend': [('NOSIG', '_interpret')],
    }

    def _interpret(self, t):
        if t == 'NOSIG':
            return "No Significant Changes"
