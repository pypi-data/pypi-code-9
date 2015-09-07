# -*- coding: utf-8 -*-


from gaminator import Vec, CIERNA, hra


class Obdl(Vec):

    def setup(self):
        self.farba = CIERNA
        self.vyfarbenie = False
        self.svet = hra.svet

    def paint(self, c):
        c.farba = self.farba
        c.rectangle(
            (0, 0),
            self.sirka, self.vyska,
            self.vyfarbenie
        )

    def step(self):
        self.repaint()


class Oval(Vec):

    def setup(self):
        self.farba = CIERNA
        self.vyfarbenie = False
        self.svet = hra.svet

    def paint(self, c):
        c.farba = self.farba
        c.ellipse(
            (self.sirka/2, self.vyska/2),
            self.sirka/2, self.vyska/2,
            self.vyfarbenie
        )

    def step(self):
        self.repaint()
