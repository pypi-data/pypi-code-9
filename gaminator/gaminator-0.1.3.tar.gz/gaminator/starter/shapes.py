# -*- coding: utf-8 -*-


from gaminator import Thing, BLACK, game


class Rect(Thing):

    def setup(self):
        self.color = BLACK
        self.filled = False
        self.world = game.world

    def paint(self, c):
        c.color = self.color
        c.rectangle(
            (0, 0),
            self.width, self.height,
            self.filled
        )

    def step(self):
        self.repaint()


class Oval(Thing):

    def setup(self):
        self.color = BLACK
        self.filled = False
        self.world = game.world

    def paint(self, c):
        c.color = self.color
        c.ellipse(
            (self.width/2, self.height/2),
            self.width/2, self.height/2,
            self.filled
        )

    def step(self):
        self.repaint()
