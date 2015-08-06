from logilab.common import testlib

# get cubes in sys.path
import cubicweb.devtools

from cubes.cmcicpay import cmcic

class DictTranslateTC(testlib.TestCase):

    def test_dicttranslate(self):
        msg = {'one':'oui', 'two': 'non', 'three': 'trois'}
        map = {'one':'un', 'three': None}
        result = cmcic.dict_translate(msg, map)
        self.assertEqual(result, {'un': 'oui', 'two': 'non'})
