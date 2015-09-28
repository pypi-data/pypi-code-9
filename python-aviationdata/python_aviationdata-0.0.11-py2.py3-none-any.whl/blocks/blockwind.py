from  . import Block

class BlockWind(Block):
    validation = "KT$|\d{3}V\d{3}"
    name = 'wind'
    patterns = {
        'windspeed': ('\d{2}(?=KT)', '_windspeed'),
        'direction': ['^\d{3}', ('^VRB', '_variable'), ('\d{3}V\d{3}', '_directionVariable')],
        'gust': '\d{2}(?=G)',
    }

    def _directionVariable(self, x):
        y = x.split('V')
        return {'lowest': y[0], 'highest': y[1]}

    def _variable(self, x):
        return 'variable'

    def _windspeed(self, ws):
        return int(ws)