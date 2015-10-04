class FlooBase:
    """ Defines order in the provided set.
    """
    def __init__(self, sequence="01"):
        self.symbols = sequence
        self.first = self.symbols[0]

    def initial(self):
        return self.encode(0)

    def ord(self, i):
        return self.symbols.index(i)

    def encode(self, n):
        r = ""
        while n >= len(self.symbols):
            r += self.symbols[0]
            n = n / len(self.symbols)
        r = self.symbols[n % len(self.symbols)] + r
        return r

    def decode(self, floo_number):
        r = 0
        pos = len(floo_number) - 1
        for symbol in floo_number:
            r += self.ord(symbol) * pow(len(self.symbols), pos)
            pos = pos - 1
        return r


class Floo(FlooBase):
    """ Provides standard operations for the sequence.
    """
    def sum(self, i, j):
        m = self.decode(i)
        n = self.decode(j)
        r = m + n
        return self.encode(r)

    def mul(self, i, j):
        m = self.decode(i)
        n = self.decode(j)
        r = m * n
        return self.encode(r)

    def inc(self, i):
        n = self.decode(i)
        n = n + 1
        return self.encode(n)

    def dec(self, i):
        n = self.decode(i)
        n = n - 1
        return self.encode(n)
