from unittest import TestCase
from onesheet.FileObject import *

__author__ = 'California Audio Visual Preservation Project'


class TestTimeBasedMetadata(TestCase):
    def setUp(self):
        self.f = FileObject("/Volumes/CAVPPTestDrive/test.iso")
    def test___init__(self):

        self.fail()

    def test_md5(self):
        self.assertEquals(self.f.calculate_MD5(progress=True), "324ac37692a673b913d2cfe54497f588")

    def test_filename(self):
        self.assertEquals(self.f.file_name, "test.iso")
