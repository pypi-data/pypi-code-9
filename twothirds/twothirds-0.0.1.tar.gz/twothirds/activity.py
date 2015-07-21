"""A class for an overall activity"""
from twothirds import Data, TwoThirdsGame

class Activity:
    def __init__(self, filename):
        self.raw_data = Data(filename)
        self.raw_data.read()
        self.data = self.raw_data.out()
        self.games = [TwoThirdsGame(d) for d in self.data]
