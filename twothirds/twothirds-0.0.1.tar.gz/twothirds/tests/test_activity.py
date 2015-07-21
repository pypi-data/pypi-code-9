import unittest
import twothirds

class TestActivity(unittest.TestCase):
    def test_initialisation_from_xls_file(self):
        file_name = 'twothirds/tests/test_data/game.xls'
        activity = twothirds.Activity(file_name)
        dicts = [{u'A': 1, u'B': 2, u'C': 3}]
        game_data = activity.data
        for i, d in enumerate(dicts):
            self.assertEqual(game_data[i], d)
        self.assertEqual(activity.games[0].find_winner(), (u'A', 1))

    def test_initialisation_from_xls_file_with_multiple_columns(self):
        file_name = 'twothirds/tests/test_data/game2.csv'
        activity = twothirds.Activity(file_name)
        dicts = [{u'A': 1, u'B': 2, u'C': 3}, {u'A':4, u'B': 5, u'C': 6}]
        game_data = activity.data
        for i, d in enumerate(game_data):
            self.assertEqual(d, dicts[i])
        self.assertEqual(activity.games[0].find_winner(), (u'A', 1))
        self.assertEqual(activity.games[1].find_winner(), (u'A', 4))
