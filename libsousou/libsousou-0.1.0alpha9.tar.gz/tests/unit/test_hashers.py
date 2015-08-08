import unittest


from libsousou.hashers.pbkdf2 import PBKDF2PasswordHasherSHA256
from libsousou.hashers.pbkdf2 import PBKDF2PasswordHasherSHA512
from libsousou.hashers.base import check_password
from libsousou.hashers.base import constant_time_compare
from libsousou.hashers.base import make_password
from libsousou.hashers.base import is_password_usable


class PBKDF2PasswordHasherSHA256TestCase(unittest.TestCase):
    password = 'foo'
    salt = 'bar'
    hasher_class = PBKDF2PasswordHasherSHA256
    iterations = 1

    def setUp(self):
        self.hasher = self.hasher_class()
        self.encoded = self.hasher.encode(self.password, self.salt, iterations=self.iterations)

    def test_verify(self):
        self.assertTrue(self.hasher.verify(self.password, self.encoded))

    def test_safe_summary(self):
        summary = self.hasher.safe_summary(self.encoded)


class PBKDF2PasswordHasherSHA512TestCase(unittest.TestCase):
    password = 'foo'
    salt = 'bar'
    hasher_class = PBKDF2PasswordHasherSHA512
    iterations = 1

    def setUp(self):
        self.hasher = self.hasher_class()
        self.encoded = self.hasher.encode(self.password, self.salt, iterations=self.iterations)

    def test_safe_summary(self):
        summary = self.hasher.safe_summary(self.encoded)

    def test_verify(self):
        self.assertTrue(self.hasher.verify(self.password, self.encoded))


class PublicApiTestCase(unittest.TestCase):
    password = 'foo'
    salt = 'bar'

    def test_make_password(self):
        p = make_password(self.password)

    def test_check_password(self):
        p = make_password(self.password)
        self.assertTrue(check_password(self.password, p))

    def test_unusable_password_prefix_for_none_password(self):
        # Providing None to make_password() must result in a string
        # starting with !.
        p = make_password(None)
        self.assertTrue(p.startswith('!'), p)

    def test_unusable_password_checks_false(self):
        # check_password() must always return False for unusable passwords.
        p = make_password(None)
        self.assertTrue(not check_password(None, p))

    def test_is_password_usable_returns_false_with_invalid(self):
        self.assertFalse(is_password_usable(None))
        self.assertFalse(is_password_usable(''))

    def test_constant_time_compare(self):
        self.assertFalse(constant_time_compare('f','ff'))


if __name__ == '__main__':
    unittest.main()
