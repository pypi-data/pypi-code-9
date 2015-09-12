import unittest
from bigben import errors

__author__ = 'sgiroux'

"""
    Unit tests to cover the errors module.
"""

class ErrorsTest(unittest.TestCase):
    """
        Tests for the bigben.errors module.
    """

    def testBigBenError(self):
        """
            Coverage test only the for BigBenError class.
        """
        error = errors.BigBenError('error message')
        self.assertTrue(error.message == 'error message')

    def testBigBenHttpError(self):
        """
            Coverage test only for the BenBenHttpError class.
        """
        error = errors.BigBenHttpError(401, 5, 'error message')
        self.assertTrue(error.message == 'error message')
        self.assertTrue(error.http_code == 401)
        self.assertTrue(error.error_code == 5)

        error = errors.BigBenHttpError(401, 5)
        self.assertTrue(error.message == 'Http Request failed with HTTP status code: 401')
        self.assertTrue(error.http_code == 401)
        self.assertTrue(error.error_code == 5)


if __name__ == '__main__':
    unittest.main()