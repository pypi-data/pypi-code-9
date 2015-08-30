import unittest

from pycards import Card
from pycards import Deck
from pycards.errors import NoCardsRemaining


class CardTestCase(unittest.TestCase):

    def setUp(self):
        super(CardTestCase, self).setUp()

    def test_card(self):
        card = Card(rank='ACE', suit='SPADES')
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')

        r = card.__repr__()
        self.assertEqual(r, '<Card: ACE of SPADES>')

        card_dict = card.to_dict()
        self.assertEqual(card_dict['rank'], 'ACE')
        self.assertEqual(card_dict['suit'], 'SPADES')

    def test_generate_cards(self):
        cards = Card.generate_cards()
        for card in cards:
            self.assertTrue(isinstance(card, Card))


class DeckTestCase(unittest.TestCase):

    def setUp(self):
        super(DeckTestCase, self).setUp()
        self.card_config = {
            'cards': ('ACE_SPADES', )
        }

    def test_deck_without_config(self):
        deck = Deck.generate_deck()
        self.assertEqual(deck.cards_remaining, 52)
        self.assertEqual(deck.cards_removed, 0)

        card = deck.draw_card()
        self.assertTrue(isinstance(card, Card))
        self.assertEqual(deck.cards_remaining, 51)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle()
        self.assertEqual(deck.cards_remaining, 52)
        self.assertEqual(deck.cards_removed, 0)

    def test_deck_with_config(self):
        deck = Deck.generate_deck(card_config=self.card_config)
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

        card = deck.draw_card()
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')
        self.assertEqual(deck.cards_remaining, 0)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle()
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

    def test_drawing_from_empty_deck(self):
        deck = Deck.generate_deck(card_config=self.card_config)
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

        deck.draw_card()
        self.assertRaises(NoCardsRemaining, deck.draw_card)

    def test_deck_to_dict(self):
        deck = Deck.generate_deck(card_config=self.card_config)
        deck_dict = deck.to_dict()
        self.assertEqual(deck_dict['cards_remaining'][0]['rank'], 'ACE')
        self.assertEqual(deck_dict['cards_remaining'][0]['suit'], 'SPADES')
