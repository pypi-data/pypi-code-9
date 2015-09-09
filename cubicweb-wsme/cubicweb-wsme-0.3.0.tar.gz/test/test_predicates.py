import mock

from cubicweb.devtools import testlib

from cubes.wsme import predicates


class PredicatesTests(testlib.CubicWebTC):
    def test_match_ws_etype(self):
        p = predicates.match_ws_etype("CWUser")

        req = mock.Mock()
        req.form = {'_ws_etype': 'CWGroup'}

        self.assertEqual(p(None, req), 0)

        req.form = {'_ws_etype': 'CWUser'}

        self.assertEqual(p(None, req), 1)
