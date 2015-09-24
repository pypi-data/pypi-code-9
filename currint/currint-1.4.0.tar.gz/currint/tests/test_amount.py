# encoding: utf8
from __future__ import unicode_literals
from decimal import Decimal
from unittest import TestCase
from ..currency import currencies
from ..amount import Amount, _ZeroAmount


class AmountTests(TestCase):

    def test_equality(self):
        self.assertEqual(
            Amount(currencies["GBP"], 132),
            Amount(currencies["GBP"], 132),
        )
        self.assertNotEqual(
            Amount(currencies["GBP"], 132),
            Amount(currencies["USD"], 132),
        )
        self.assertNotEqual(
            Amount(currencies["GBP"], 132),
            Amount(currencies["GBP"], 99),
        )
        self.assertNotEqual(
            Amount(currencies["GBP"], 132),
            object(),
        )

    def test_add(self):
        self.assertEqual(
            Amount(currencies["GBP"], 132) + Amount(currencies["GBP"], 100),
            Amount(currencies["GBP"], 232),
        )
        with self.assertRaises(ValueError):
            Amount(currencies["GBP"], 132) + Amount(currencies["USD"], 100)

    def test_subtract(self):
        self.assertEqual(
            Amount(currencies["GBP"], 132) - Amount(currencies["GBP"], 100),
            Amount(currencies["GBP"], 32),
        )
        with self.assertRaises(ValueError):
            Amount(currencies["GBP"], 132) - Amount(currencies["USD"], 100)

    def test_format(self):
        self.assertEqual(
            unicode(Amount(currencies["USD"], 132)),
            "$1.32",
        )
        self.assertEqual(
            unicode(Amount(currencies["USD"], -132)),
            "$-1.32",
        )
        self.assertEqual(
            unicode(Amount(currencies["GBP"], 132)),
            "£1.32",
        )
        self.assertEqual(
            unicode(Amount(currencies["MRO"], 7)),
            "1.2 MRO",
        )

    def test_bool(self):
        self.assertTrue(Amount(currencies["USD"], 1))
        self.assertFalse(Amount(currencies["USD"], 0))
        self.assertTrue(Amount.from_code_and_major("USD", Decimal('0.01')))
        self.assertFalse(Amount.from_code_and_major("USD", Decimal('0.00')))

    def test_apply_factor(self):
        self.assertEqual(
            Amount(currencies["GBP"], 150).apply_factor(2),
            Amount(currencies["GBP"], 300),
        )
        self.assertEqual(
            Amount(currencies["GBP"], 100).apply_factor(Decimal("1.004")),
            Amount(currencies["GBP"], 100),
        )
        self.assertEqual(
            Amount(currencies["GBP"], 100).apply_factor(Decimal("1.005")),
            Amount(currencies["GBP"], 101),
        )
        with self.assertRaises(ValueError):
            Amount(currencies["GBP"], 100).apply_factor(1.005)

    def test_from_code_and_minor(self):
        self.assertEqual(
            Amount.from_code_and_minor("GBP", 300),
            Amount(currencies["GBP"], 300),
        )
        self.assertEqual(
            Amount.from_code_and_minor("gbp", 300),
            Amount(currencies["GBP"], 300),
        )
        with self.assertRaises(ValueError):
            Amount.from_code_and_minor("WAITWHAT", 100)

    def test_from_code_and_major(self):
        self.assertEqual(
            Amount.from_code_and_major("GBP", "3.00"),
            Amount(currencies["GBP"], 300),
        )
        self.assertEqual(
            Amount.from_code_and_major("gbp", ".10"),
            Amount(currencies["GBP"], 10),
        )
        self.assertEqual(
            Amount.from_code_and_major("GBP", 10),
            Amount(currencies["GBP"], 1000),
        )
        self.assertEqual(
            Amount.from_code_and_major("GBP", Decimal("10.01")),
            Amount(currencies["GBP"], 1001),
        )
        with self.assertRaises(ValueError):
            Amount.from_code_and_major("WAITWHAT", 100)
        with self.assertRaises(ValueError):
            Amount.from_code_and_major("GBP", "12.432")
        with self.assertRaises(ValueError):
            Amount.from_code_and_major("GBP", "aaaaaaah")

    def test_to_major_decimal(self):
        self.assertEqual(
            Amount(currencies["GBP"], 300).to_major_decimal(),
            Decimal("3.00"),
        )
        self.assertEqual(
            Amount(currencies["USD"], 3).to_major_decimal(),
            Decimal("0.03"),
        )
        self.assertEqual(
            Amount(currencies["GBP"], -425).to_major_decimal(),
            Decimal("-4.25"),
        )
        self.assertEqual(
            Amount(currencies["MRO"], 7).to_major_decimal(),
            Decimal("1.4"),  # It's written 1.2, but is 1.4 of the major unit
        )


class ZeroAmountTests(TestCase):
    def setUp(self):
        self.nonzero = Amount(currencies["GBP"], 300)

    def test_singleton(self):
        self.assertIs(Amount.ZERO, _ZeroAmount())

    def test_simple_addition(self):
        amt = Amount.ZERO + self.nonzero
        self.assertEqual(amt.currency, self.nonzero.currency)
        self.assertEqual(amt.value, self.nonzero.value)

    def test_simple_raddition(self):
        amt = self.nonzero + Amount.ZERO
        self.assertEqual(amt.currency, self.nonzero.currency)
        self.assertEqual(amt.value, self.nonzero.value)

    def test_sum(self):
        amt = sum([self.nonzero], Amount.ZERO)
        self.assertEqual(amt.currency, self.nonzero.currency)
        self.assertEqual(amt.value, self.nonzero.value)

    def test_subr(self):
        amt = self.nonzero - Amount.ZERO
        self.assertEqual(amt.currency, self.nonzero.currency)
        self.assertEqual(amt.value, self.nonzero.value)

    def test_subl(self):
        amt = Amount.ZERO - self.nonzero
        self.assertEqual(amt.currency, self.nonzero.currency)
        self.assertEqual(amt.value, -self.nonzero.value)

    def test_sum_with_zeroes(self):
        amt = sum([Amount.ZERO, self.nonzero, Amount.ZERO], Amount.ZERO)
        self.assertEqual(amt.currency, self.nonzero.currency)
        self.assertEqual(amt.value, self.nonzero.value)

    def test_to_major_decimal(self):
        self.assertEqual(Amount.ZERO.to_major_decimal(), Decimal('0'))

    def test_unicode(self):
        try:
            unicode(Amount.ZERO)
        except:
            self.fail("unicode(Amount.ZERO) raised an exception")

    def test_repr(self):
        try:
            repr(Amount.ZERO)
        except:
            self.fail("repr(Amount.ZERO) raised an exception")

    def test_forbidden_from_code_and_minor(self):
        with self.assertRaises(NotImplementedError):
            _ZeroAmount.from_code_and_minor('USD', 100)

    def test_forbidden_from_code_and_major(self):
        with self.assertRaises(NotImplementedError):
            _ZeroAmount.from_code_and_minor('USD', Decimal('1.00'))
