from . import Block


class BlockRunwayView(Block):
    validation = '^R\d{2}/(\d{4}|[M,P]\d{4}|\d{4}V\d{4})([U,D,N]$|$)'
    name = 'runway_view'
    patterns = {
        'qnh': [('\d{3,4}', '_qnh')],
    }

    def _qnh(self, q):
        return int(q)