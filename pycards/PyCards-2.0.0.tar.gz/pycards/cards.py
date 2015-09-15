import json
from copy import deepcopy
from pycards.config import DEFAULT_CARDS_CONFIG


class BaseCard(object):

    def to_dict(self):
        return deepcopy(self.__dict__)

    @classmethod
    def from_dict(cls, card_dict):
        card = cls()
        card.__dict__.update(card_dict)
        return card

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, card_json):
        card_dict = json.loads(card_json)
        return cls.from_dict(card_dict=card_dict)

    @classmethod
    def generate_cards(cls, config):
        if type(config) == str:
            config = json.loads(config)
        for card_dict in config:
            yield cls.from_dict(card_dict=card_dict)


class PlayingCard(BaseCard):

    def __init__(self, rank=None, suit=None):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return '<PlayingCard: {0} of {1}>'.format(self.rank, self.suit)

    @classmethod
    def generate_cards(cls, config=DEFAULT_CARDS_CONFIG):
        props = ('rank', 'suit', )
        card_dicts = [dict(zip(props, c.split('_'))) for c in config]
        for card_dict in card_dicts:
            yield cls.from_dict(card_dict=card_dict)


class PlayingCardWithImages(PlayingCard):

    def __init__(self, rank=None, suit=None, front_image=None, back_image=None):
        super(PlayingCardWithImages, self).__init__(rank=rank, suit=suit)
        self.front_image = front_image
        self.back_image = back_image

    def __repr__(self):
        return '<PlayingCardWithImages: {0} of {1}>'.format(self.rank, self.suit)

    @classmethod
    def generate_cards(cls, config):
        props = ('rank', 'suit', 'front_image', 'back_image', )
        for card in config['cards']:
            rank, suit = card.split('_')
            front_image = '{0}/{1}-{2}.png'.format(config['image_path'], rank, suit)
            back_image = '{0}/back.png'.format(config['image_path'])
            card_dict = dict(zip(props, (rank, suit, front_image, back_image, )))
            yield cls.from_dict(card_dict=card_dict)
