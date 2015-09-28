from . import Block


class BlockView(Block):
    validation = '^\d{4}$|CAVOK'
    name = 'view'
    patterns = {
        'distance': ['\d{4}$', ('^CAVOK$', '_cavok')],
    }

    def _cavok(self, c):
        return 'Ceiling And Visibility OKay' # No cloud below 5000ft, no Cn Tc, visability >= 10km, nosig