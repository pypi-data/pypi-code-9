import unittest
from inception.constants import InceptionConstants
from inception.config.dotidentifierresolver import DotIdentifierResolver
from inception.config import ConfigTreeParser
import os
class MakeTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MakeTest, self).__init__(*args, **kwargs)
        configCode = "samsung.matissewifi.hunziker"
        self.configTreeParser = ConfigTreeParser(DotIdentifierResolver(["../" + InceptionConstants.VARIANTS_DIR, "../" + InceptionConstants.BASE_DIR]))
        self.config = self.configTreeParser.parseJSON(configCode)

    def testABC(self):
        settings = self.config.get("update.settings", {})
        psettings = settings["com.android.providers.settings"]
        self.assertTrue("schema" in psettings)

    def testEFG(self):
        import json
        fullData = self.config.dumpFullData()
        data = json.loads(fullData)
        settings = data["update"]["settings"]
        print(settings)

    def testMultiLevelCode(self):
        code = "samsung.degaswifi.rooted"
        config = self.configTreeParser.parseJSON(code)
        config.getProperty("recovery.img")



