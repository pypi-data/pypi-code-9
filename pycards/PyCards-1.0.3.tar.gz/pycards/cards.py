from pycards.config import DEFAULT_CARDS_CONFIG


class StandardPlayingCard(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return '<StandardPlayingCard: {0} of {1}>'.format(self.rank, self.suit)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def generate_cards(cls, config=DEFAULT_CARDS_CONFIG):
        for card in config['cards']:
            rank, suit = card.split('_')
            yield cls(rank=rank, suit=suit)
