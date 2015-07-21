import unittest
import twothirds

class TestGame(unittest.TestCase):
    def test_initialisation_from_other_than_list_gives_errors(self):
        data = 2
        self.assertRaises(ValueError, twothirds.TwoThirdsGame, data)

    def test_initialisation_from_list(self):
        data = range(100)
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(data, g.data)

    def test_initialisation_from_dictionary(self):
        data = dict(zip(range(100), range(100)))
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(data, g.data)

    def test_calculation_for_list(self):
        data = range(100)
        g = twothirds.TwoThirdsGame(data)
        two_thirds = sum(data) * 2.0 / (3.0 * len(data))
        self.assertAlmostEqual(two_thirds, g.two_thirds_of_the_average())

    def test_calculation_for_dict(self):
        data = dict(zip(range(100), range(100)))
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(data, g.data)
        two_thirds = sum(data.values()) * 2.0 / (3.0 * len(data))
        self.assertAlmostEqual(two_thirds, g.two_thirds_of_the_average())

    def test_find_winner_for_list(self):
        data = range(100)
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(33, g.find_winner())

    def test_find_winner_for_list_1(self):
        data = [5, 5, 10, 9, 1, 0]
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(5, g.find_winner())

    def test_find_winner_for_list_2(self):
        data = [0, 0, 0, 0, 0, 0]
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(0, g.find_winner())

    def test_find_winner_for_list_3(self):
        data = [100, 100, 100, 100, 100, 100]
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(100, g.find_winner())

    def test_find_winner_for_dict(self):
        data = dict(zip(range(100), range(100)))
        g = twothirds.TwoThirdsGame(data)
        self.assertAlmostEqual((33, 33), g.find_winner())

    def test_find_winner_for_dict_1(self):
        data = {'Vince' : 5,
                'Zoe' : 5,
                'David': 10,
                'Elliot': 9,
                'Kaity': 1,
                'Ben': 0}
        g = twothirds.TwoThirdsGame(data)
        self.assertEqual(('Vince', 'Zoe', 5), g.find_winner())

    def test_find_winner_for_dict_2(self):
        data = {'Vince' : 0,
                'Zoe' : 0,
                'David': 0,
                'Elliot': 0,
                'Kaity': 0,
                'Ben': 0}
        g = twothirds.TwoThirdsGame(data)
        sorted_names = sorted(data.keys())
        expected_result = tuple(sorted_names + [0])
        self.assertEqual(expected_result, g.find_winner())

    def test_find_winner_for_dict_3(self):
        data = {'Vince' : 100,
                'Zoe' : 100,
                'David': 100,
                'Elliot': 100,
                'Kaity': 100,
                'Ben': 100}
        g = twothirds.TwoThirdsGame(data)
        sorted_names = sorted(data.keys())
        expected_result = tuple(sorted_names + [100])
        self.assertEqual(expected_result, g.find_winner())

    def test_find_winner_for_dict_4(self):
        data = {'A': 1,
                'B': 2,
                'C': 3}
        g = twothirds.TwoThirdsGame(data)
        expected_result = ('A', 1)
        self.assertEqual(expected_result, g.find_winner())
