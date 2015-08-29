import json
from pycards.config import DEFAULT_CARDS_CONFIG


class StandardPlayingCard(object):

    def __init__(self, rank, suit, image_path):
        self.rank = rank
        self.suit = suit
        self.back_image = '{0}/back.png'.format(image_path)
        self.front_image = '{0}/{1}-{2}.png'.format(image_path, self.rank, self.suit)

    def __repr__(self):
        return '<StandardPlayingCard: {0} of {1}>'.format(self.rank, self.suit)

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def generate_cards(cls, config=DEFAULT_CARDS_CONFIG):
        for card in config['cards']:
            rank, suit = card.split('_')
            yield cls(rank=rank, suit=suit, image_path=config['image_path'])
