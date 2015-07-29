from hypothesis.utils.conventions import not_set

def accept(f):
    def test_slugify_is_idempotent_on_bytes(s=not_set):
        return f(s)
    return test_slugify_is_idempotent_on_bytes
