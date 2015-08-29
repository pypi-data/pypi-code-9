from random import shuffle
from pycards.cards import StandardPlayingCard
from pycards.errors import NoCardsRemaining


DEFAULT_CARD_CLASS = StandardPlayingCard


class Deck(object):

    def __init__(self, cards, count=1):
        self._cards_remaining = cards * count
        self._cards_removed = []

    @property
    def cards_remaining(self):
        return len(self._cards_remaining)

    @property
    def cards_removed(self):
        return len(self._cards_removed)

    def shuffle_remaining(self):
        shuffle(self._cards_remaining)

    def shuffle_removed(self):
        shuffle(self._cards_removed)

    def shuffle_all(self):
        self._cards_remaining.extend(self._cards_removed)
        self._cards_removed = []
        self.shuffle_remaining()

    def draw_card(self):
        try:
            card = self._cards_remaining.pop()
        except IndexError:
            raise NoCardsRemaining
        else:
            self._cards_removed.append(card)
            return card

    @classmethod
    def generate_deck(cls, card_cls=DEFAULT_CARD_CLASS, card_config=None, count=1):
        if card_config is None:
            cards = list(card_cls.generate_cards())
        else:
            cards = list(card_cls.generate_cards(config=card_config))
        return cls(cards=cards, count=count)
