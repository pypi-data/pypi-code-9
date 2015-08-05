"""template automatic tests"""

from logilab.common.testlib import unittest_main
from cubicweb.devtools.testlib import AutomaticWebTest

class AutomaticWebTest(AutomaticWebTest): pass

if __name__ == '__main__':
    unittest_main()
