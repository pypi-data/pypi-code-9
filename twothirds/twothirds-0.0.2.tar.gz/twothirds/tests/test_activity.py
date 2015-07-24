import unittest
import twothirds
import matplotlib


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
        dicts = [{u'A': 1, u'B': 2, u'C': 3}, {u'A': 4, u'B': 5, u'C': 6}]
        game_data = activity.data
        for i, d in enumerate(game_data):
            self.assertEqual(d, dicts[i])
        self.assertEqual(activity.games[0].find_winner(), (u'A', 1))
        self.assertEqual(activity.games[1].find_winner(), (u'A', 4))

    def test_analysis_of_results(self):
        file_name = 'twothirds/tests/test_data/game2.csv'
        activity = twothirds.Activity(file_name)
        activity.analyse()
        self.assertEqual(activity.two_thirds, [4.0 / 3, 2.0 * 5 / 3])
        self.assertEqual(activity.winners, [('A',), ('A',)])
        self.assertEqual(activity.winning_guesses, [1, 4])

    #def test_pairplot_results(self):
        #file_name = 'twothirds/tests/test_data/game2.csv'
        #activity = twothirds.Activity(file_name)
        #activity.analyse()
        #p = activity.pairplot()
        #self.assertIs(type(p), matplotlib.figure.Figure)

    #def test_distplot_results(self):
        #file_name = 'twothirds/tests/test_data/game2.csv'
        #activity = twothirds.Activity(file_name)
        #activity.analyse()
        #p = activity.distplot()
        #self.assertIs(type(p), matplotlib.figure.Figure)

    def test__repr__(self):
        file_name = 'twothirds/tests/test_data/game2.csv'
        activity = twothirds.Activity(file_name)
        activity.analyse()
        string = """=====================
Game 0
---------------------
2/3rds of the average: 1.33
Winning guess: 1
Winner(s): ('A',)
=====================
Game 1
---------------------
2/3rds of the average: 3.33
Winning guess: 4
Winner(s): ('A',)
"""
        self.assertMultiLineEqual(activity.__repr__(), string)
