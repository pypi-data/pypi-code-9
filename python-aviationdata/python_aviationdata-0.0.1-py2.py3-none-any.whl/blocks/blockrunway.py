from . import Block


class BlockRunwayDetail(Block):
    patterns = {
        'runway': ('(?<=^R)\d{2}', '_runway'),#['\d{4}$', ('^CAVOK$', '_cavok')],
        'situation': ('(?<=^R\d{2}/).*', '_situation')
    }

    states = {
        '0': 'clean',
        '1': 'wet',
        '2': 'water',
        '3': 'covered partial ice',
        '4': 'dry snow',
        '5': 'wet snow',
        '6': 'snow puddle',
        '7': 'ice',
        '8': 'prepared snow',
        '9': 'freezed lanes or grooves',
        '/': 'no information'
    }


    def _situation(self, s):
        state = s[0]
        coverage = s[1]
        thicknes = s[2:4]
        breaking = s[4:6]
        return {
            'state': self.states[state],
            'coverage': coverage,
            'thick': thicknes,
            'breaking': breaking

        }

    def _runway(self, r):
        if r == '88':
            return 'All runways'
        if r == '99':
            return 'previous report'
        return r

class BlockRunway(Block):
    validation = '^R.*/.*(/|\d)$'
    name = 'runways'
    patterns = {
        'runway': ('^R.*/.*(/|\d)$', '_runway'),
    }

    def _runway(self, r):
        b = BlockRunwayDetail(r)
        return [b.parse()]