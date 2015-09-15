import json
import unittest

from pycards import BaseCard, PlayingCard, PlayingCardWithImages
from pycards import BaseDeck
from pycards.errors import NoCardsRemaining


class PlayingCardTestCase(unittest.TestCase):

    def setUp(self):
        super(PlayingCardTestCase, self).setUp()

    def test_playing_card(self):
        card = PlayingCard(rank='ACE', suit='SPADES')
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')

        r = card.__repr__()
        self.assertEqual(r, '<PlayingCard: ACE of SPADES>')

        card_dict = card.to_dict()
        self.assertEqual(card_dict['rank'], 'ACE')
        self.assertEqual(card_dict['suit'], 'SPADES')

    def test_playing_card_to_json(self):
        card = PlayingCard(rank='ACE', suit='SPADES')
        card_json = card.to_json()
        card_dict = json.loads(card_json)
        self.assertEqual(card_dict['rank'], 'ACE')
        self.assertEqual(card_dict['suit'], 'SPADES')

    def test_playing_card_from_json(self):
        card_json = json.dumps({'rank': 'ACE', 'suit': 'SPADES'})
        card = PlayingCard.from_json(card_json=card_json)
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')

    def test_generate_playing_cards(self):
        cards = PlayingCard.generate_cards()
        for card in cards:
            self.assertTrue(isinstance(card, PlayingCard))

    def test_playing_card_with_images(self):
        card = PlayingCardWithImages(
            rank='ACE',
            suit='SPADES',
            front_image='whatever/ACE-SPADES.png',
            back_image='whatever/back.png')
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')
        self.assertEqual(card.front_image, 'whatever/ACE-SPADES.png')
        self.assertEqual(card.back_image, 'whatever/back.png')

        r = card.__repr__()
        self.assertEqual(r, '<PlayingCardWithImages: ACE of SPADES>')

        card_dict = card.to_dict()
        self.assertEqual(card_dict['rank'], 'ACE')
        self.assertEqual(card_dict['suit'], 'SPADES')
        self.assertEqual(card_dict['front_image'], 'whatever/ACE-SPADES.png')
        self.assertEqual(card_dict['back_image'], 'whatever/back.png')

    def test_generate_playing_cards_with_images(self):
        config = {
            'cards': ('ACE_SPADES', '2_SPADES', '3_SPADES', ),
            'image_path': 'whatever'
        }
        cards = PlayingCardWithImages.generate_cards(config=config)
        for card in cards:
            self.assertTrue(isinstance(card, PlayingCardWithImages))
            self.assertIn('whatever', card.front_image)
            self.assertIn('whatever', card.back_image)

    def test_generate_base_cards(self):
        json_config = json.dumps([
            {'rank': 'ACE', 'suit': 'SPADES'},
            {'rank': 'KING', 'suit': 'SPADES'}])
        cards = BaseCard.generate_cards(config=json_config)
        for card in cards:
            self.assertTrue(isinstance(card, BaseCard))


class BaseDeckTestCase(unittest.TestCase):

    def setUp(self):
        super(BaseDeckTestCase, self).setUp()
        self.card_config = ('ACE_SPADES', )

    def test_generate_base_deck(self):
        deck = BaseDeck.generate_deck(
            card_cls=PlayingCard,
            card_config=self.card_config)
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

        card = deck.draw_card()
        self.assertTrue(isinstance(card, PlayingCard))
        self.assertEqual(card.rank, 'ACE')
        self.assertEqual(card.suit, 'SPADES')
        self.assertEqual(deck.cards_remaining, 0)
        self.assertEqual(deck.cards_removed, 1)

        deck.shuffle()
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

    def test_drawing_from_empty_base_deck(self):
        deck = BaseDeck.generate_deck(
            card_cls=PlayingCard,
            card_config=self.card_config)
        self.assertEqual(deck.cards_remaining, 1)
        self.assertEqual(deck.cards_removed, 0)

        deck.draw_card()
        self.assertRaises(NoCardsRemaining, deck.draw_card)

    def test_base_deck_to_dict(self):
        deck = BaseDeck.generate_deck(
            card_cls=PlayingCard,
            card_config=self.card_config)
        deck_dict = deck.to_dict()
        self.assertEqual(deck_dict['cards_remaining'][0]['rank'], 'ACE')
        self.assertEqual(deck_dict['cards_remaining'][0]['suit'], 'SPADES')

    def test_base_deck_to_json(self):
        deck = BaseDeck.generate_deck(
            card_cls=PlayingCard,
            card_config=self.card_config)
        deck_json = deck.to_json()
        deck_dict = json.loads(deck_json)
        self.assertEqual(deck_dict['cards_remaining'][0]['rank'], 'ACE')
        self.assertEqual(deck_dict['cards_remaining'][0]['suit'], 'SPADES')
