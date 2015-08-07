import unittest, doctest

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        doctest.DocFileSuite('test_extjs.txt',
                             package='js.extjs'),
        ])
    return suite
