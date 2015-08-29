import json
import unittest

from pycards import StandardPlayingCard
from pycards import Deck
from pycards.errors import NoCardsRemaining


class StandardPlayingCardTestCase(unittest.TestCase):

    def setUp(self):
        super(StandardPlayingCardTestCase, self).setUp()

    def test_card(self):
        card = StandardPlayingCard(rank='ACE', suit='SPADES', image_path='whatever')
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')
        self.assertEqual(card.back_image, 'whatever/back.png')
        self.assertEqual(card.front_image, 'whatever/ACE-SPADES.png')

        r = card.__repr__()
        self.assertEqual(r, '<StandardPlayingCard: ACE of SPADES>')

        card_json_data = json.loads(card.to_json())
        self.assertEqual(card_json_data['rank'], 'ACE')
        self.assertEqual(card_json_data['suit'], 'SPADES')
        self.assertEqual(card_json_data['back_image'], 'whatever/back.png')
        self.assertEqual(card_json_data['front_image'], 'whatever/ACE-SPADES.png')

    def test_generate_cards(self):
        cards = StandardPlayingCard.generate_cards()
        for card in cards:
            self.assertTrue(isinstance(card, StandardPlayingCard))


class DeckTestCase(unittest.TestCase):

    def setUp(self):
        super(DeckTestCase, self).setUp()
        self.card_config = {
            'cards': ('ACE_SPADES', ),
            'image_path': 'whatever'
        }

    def test_deck_without_config(self):
        deck = Deck.generate_deck()
        self.assertEqual(deck.cards_remaining, 52)
        self.assertEqual(deck.cards_removed, 0)

        card = deck.draw_card()
        self.assertTrue(isinstance(card, StandardPlayingCard))
        self.assertEqual(deck.cards_remaining, 51)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle_remaining()
        self.assertEqual(deck.cards_remaining, 51)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle_removed()
        self.assertEqual(deck.cards_remaining, 51)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle_all()
        self.assertEqual(deck.cards_remaining, 52)
        self.assertEqual(deck.cards_removed, 0)

    def test_deck_with_config(self):
        deck = Deck.generate_deck(card_config=self.card_config)
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

        card = deck.draw_card()
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')
        self.assertEqual(card.back_image, 'whatever/back.png')
        self.assertEqual(card.front_image, 'whatever/ACE-SPADES.png')
        self.assertEqual(deck.cards_remaining, 0)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle_remaining()
        self.assertEqual(deck.cards_remaining, 0)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle_removed()
        self.assertEqual(deck.cards_remaining, 0)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle_all()
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

    def test_drawing_from_empty_deck(self):
        deck = Deck.generate_deck(card_config=self.card_config)
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

        deck.draw_card()
        self.assertRaises(NoCardsRemaining, deck.draw_card)
