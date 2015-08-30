import contoml


def test_prettifying_against_humanly_verified_sample():
    f = contoml.load('sample.toml')
    f.prettify()
    with open('sample-prettified.toml') as fp:
        assert fp.read() == f.dumps()
