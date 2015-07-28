import unittest
from ebzl.modules import bundle


class This(unittest.TestCase):

    def test_bundle(self):
        args = type("Args", (), {"force": False})()

        bundle.get_source_bundle_file_path(args)

