from hypothesis.utils.conventions import not_set

def accept(f):
    def sampled_from(elements):
        return f(elements)
    return sampled_from
