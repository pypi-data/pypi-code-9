


class Power(CachedExpression):
    def __init__(self, a):
        super(Power, self).__init__()
        self.a = a
        self.b = b

    def _bind(self, binding):
        return bind(self.a, binding) ** bind(self.b, binding)

    def _differentiate(self, variable):
        da = differentiate(self.a, variable)
        db = differentiate(self.b, variable)
        return (da * self.b * (self.a ** (self.b - 1)) +
                db * log(self.a) * (self.a ** self.b))

    def __repr__(self):
        return "(%s ** %s)"%(self.a, self.b)
