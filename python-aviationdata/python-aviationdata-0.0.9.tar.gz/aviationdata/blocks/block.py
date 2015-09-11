import re

class Block(object):
    block = None
    patterns = {}
    validation = None
    name = 'unknown'

    def __init__(self, block):
        self.block = block.upper()

    def validate(self):
        if not self.validation:
            return False
        if self.validation is True:
            return True

        if re.search(self.validation, self.block, re.I | re.S | re.M):
            return True
        return False

    def parse(self):
        data = {'_raw': self.block}
        for (name, value) in self.patterns.iteritems():
            if not isinstance(value, (list,)):
                value = [value]

            for x in value:
                if isinstance(x, (tuple,)):
                    y = self._parse(regex=x[0], callback=x[1])
                else:
                    y = self._parse(regex=x)

                if y:
                    data[name] = y
        return data

    def _parse(self, regex, callback=None):
        data=None
        match = re.search(regex, self.block, re.I | re.S | re.M)
        if match:
            data = match.group()
            if callback:
                callback = getattr(self, callback)
                data = callback(data)
        return data

    @classmethod
    def doit(cls, block):
        x = cls(block)
        if x.validate():
            return x.parse()
        return False