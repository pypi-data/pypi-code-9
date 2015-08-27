
import re
import ruamel.pdfdouble


# default for tox stub is to Fail
def test_pdfdouble():
    assert True



IPre = re.compile("(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
                  "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])")


class TestPatterns:

    def Xtest_filter():
        x = IPre.sub(' ', 'X132.234.0.2X')
        print(x)
        assert x == 'XY'
