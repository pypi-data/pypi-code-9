from hypothesis.utils.conventions import not_set

def accept(f):
    def test_floats(self, x=not_set):
        return f(self=self, x=x)
    return test_floats
