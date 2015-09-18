import json
from random import shuffle
from pycards.errors import NoCardsRemaining


class BaseDeck(object):

    def __init__(self, cards=None, count=1):
        self._cards_remaining = [] if cards is None else cards * count
        self._cards_removed = []

    @property
    def cards_remaining(self):
        return len(self._cards_remaining)

    @property
    def cards_removed(self):
        return len(self._cards_removed)

    def shuffle(self):
        self._cards_remaining.extend(self._cards_removed)
        self._cards_removed = []
        shuffle(self._cards_remaining)

    def draw_card(self):
        try:
            card = self._cards_remaining.pop()
        except IndexError:
            raise NoCardsRemaining
        else:
            self._cards_removed.append(card)
            return card

    def to_dict(self):
        return {
            'cards_remaining': [card.to_dict() for card in self._cards_remaining],
            'cards_removed': [card.to_dict() for card in self._cards_removed]
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, card_cls, deck_dict):
        deck = cls()
        deck._cards_remaining = [card_cls.from_dict(card_dict=card_dict) for card_dict
                                 in deck_dict['cards_remaining']]
        deck._cards_removed = [card_cls.from_dict(card_dict=card_dict) for card_dict
                               in deck_dict['cards_removed']]
        return deck

    @classmethod
    def from_json(cls, card_cls, deck_json):
        deck_dict = json.loads(deck_json)
        return cls.from_dict(card_cls=card_cls, deck_dict=deck_dict)

    @classmethod
    def generate_deck(cls, card_cls, card_config, count=1):
        cards = list(card_cls.generate_cards(config=card_config))
        return cls(cards=cards, count=count)
