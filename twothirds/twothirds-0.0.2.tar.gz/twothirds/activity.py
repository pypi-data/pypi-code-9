"""A class for an overall activity"""
from twothirds import Data, TwoThirdsGame
import seaborn as sns
import matplotlib.pyplot as plt

class Activity:
    def __init__(self, filename):
        self.raw_data = Data(filename)
        self.raw_data.read()
        self.data = self.raw_data.out()
        self.games = [TwoThirdsGame(d) for d in self.data]

    def analyse(self):
        self.two_thirds = [game.two_thirds_of_the_average() for game in
                           self.games]
        self.winners = [game.find_winner()[:-1] for game in self.games]
        self.winning_guesses = [game.find_winner()[-1] for game in self.games]

    def __repr__(self):
        string = ''
        for i, game in enumerate(self.games):
            string += """=====================
Game {}
---------------------
2/3rds of the average: {:.2f}
Winning guess: {}
Winner(s): {}
""".format(i, self.two_thirds[i], self.winning_guesses[i], self.winners[i])
        return string

    def pairplot(self):
        figure = plt.figure()
        sns.pairplot(self.raw_data.df)
        return figure

    def distplot(self):
        figure = plt.figure()
        clrs = sns.color_palette("hls", len(self.games))
        for i, game in enumerate(self.games):
            if type(game.data) is list:
                values = game.data
            if type(game.data) is dict:
                values = game.data.values()
            sns.distplot(values, kde=False, norm_hist=False, label='Game {}'.format(i), color=clrs[i])
            two_thirds = self.two_thirds[i]
            plt.axvline(two_thirds, color=clrs[i], label='2/3rds = {:.2f}'.format(two_thirds))
        plt.xlabel('Guess')
        plt.ylabel('Frequency')
        plt.legend()
        return figure
