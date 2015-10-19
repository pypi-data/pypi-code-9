#!/usr/bin/env python

import pytest

from pygcrypt import utils

def test_setui(context):
    mpi = context.mpi(1234)
    assert mpi.value == 1234
    mpi = context.mpi(-1234)
    assert mpi.value == -1234

def test_set(context):
    mpi_a = context.mpi(1234)
    mpi_b = context.mpi(1234)
    mpi_b.mpi = mpi_a.mpi

    assert mpi_b == mpi_a

def test_copy(context):
    mpi_a = context.mpi(1234)
    mpi_b = mpi_a.copy()
    assert mpi_b == mpi_a

def test_mul(context):
    mpi = context.mpi(3)
    assert mpi * 3 == 9
    mpi *= 3
    assert mpi == 9
    assert mpi * mpi == 81
    mpi *= mpi
    assert mpi == 81

def test_add(context):
    mpi = context.mpi(3)
    assert mpi + 3 == 6
    mpi += 3
    assert mpi == 6
    assert mpi + mpi == 12
    mpi += mpi
    assert mpi == 12

def test_sub(context):
    mpi = context.mpi(12)
    assert mpi - 6 == 6
    mpi -= 6
    assert mpi == 6
    assert mpi - mpi == 0
    mpi -= mpi
    assert mpi == 0

def test_div(context):
    mpi = context.mpi(81)
    assert mpi // 9 == 9
    mpi //= 9
    assert mpi == 9
    assert mpi // mpi == 1
    mpi //= mpi
    assert mpi == 1

def test_mod(context):
    mpi = context.mpi(6)
    assert mpi % 4 == 2
    mpi %= 4
    assert mpi == 2
    assert mpi % mpi == 0
    mpi %= mpi
    assert mpi == 0

def test_addm(context):
    mpi_a = context.mpi(6)
    mpi_b = mpi_a.copy()
    mpi_c = mpi_b.copy()
    mpi_c.value = 5
    assert mpi_a.addm(mpi_b, mpi_c) == 2

def test_subm(context):
    mpi_a = context.mpi(6)
    mpi_b = mpi_a.copy()
    mpi_c = mpi_a.copy()
    mpi_c.value = 5
    assert mpi_a.subm(mpi_b, mpi_c) == 0

def test_mulm(context):
    mpi_a = context.mpi(6)
    mpi_b = mpi_a.copy()
    mpi_c = mpi_b.copy()
    mpi_c.value = 5
    assert mpi_a.mulm(mpi_b, mpi_c) == 1

def test_mul2exp(context):
    mpi = context.mpi(4)
    assert mpi.mul2exp(2) == 16

def test_powm(context):
    mpi_a = context.mpi(4)
    mpi_b = mpi_a.copy()
    mpi_c = mpi_a.copy()
    mpi_c.value = 5
    assert mpi_a.powm(mpi_b, mpi_c) == 1

def test_gcd(context):
    mpi_a = context.mpi(6)
    mpi_b = context.mpi(3)
    assert mpi_a.gcd(mpi_b) == 3

def test_invm(context):
    mpi_a = context.mpi(17)
    mpi_b = context.mpi(5)
    assert mpi_a.invm(mpi_b) == 3

def test_inv_abs(context):
    mpi = context.mpi(6)
    mpi = - mpi
    assert mpi == -6
    mpi = abs(mpi)
    assert mpi == 6

def test_swap(context):
    mpi_a = context.mpi(4)
    mpi_b = context.mpi(5)
    (mpi_a, mpi_b) = utils.swap(mpi_a, mpi_b)
    assert mpi_a == 5
    assert mpi_b == 4

def test_snatch(context):
    mpi_a = context.mpi(4)
    mpi_b = context.mpi(10)
    mpi_a = utils.snatch(mpi_b, mpi_a)
    assert mpi_a == 10

def test_isneg(context):
    mpi = context.mpi(5)
    assert utils.isneg(mpi) == False
    mpi = - mpi
    assert utils.isneg(mpi) == True

def test_eq(context):
    mpi = context.mpi(5)
    assert mpi == 5
    assert mpi == mpi.copy()

def tes_ne(context):
    mpi = context.mpi(6)
    assert mpi != 5
    mpi_b = context.mpi(5)
    assert mpi != mpi_b

def test_gt(context):
    mpi_a = context.mpi(5)
    mpi_b = context.mpi(6)
    assert mpi_b > mpi_a
    assert mpi_a > 4

def test_lt(context):
    mpi_a = context.mpi(5)
    mpi_b = context.mpi(6)
    assert mpi_a < mpi_b
    assert mpi_a < 6

def test_ge(context):
    mpi_a = context.mpi(5)
    mpi_b = context.mpi(6)
    assert mpi_b >= mpi_a
    assert mpi_a >= 4

def test_le(context):
    mpi_a = context.mpi(5)
    mpi_b = context.mpi(6)
    assert mpi_a <= mpi_b
    assert mpi_a <= 6

def test_lshift(context):
    mpi_a = context.mpi(4)
    assert mpi_a << 1 == 8
    mpi_a <<= 1
    assert mpi_a == 8

def test_rshift(context):
    mpi_a = context.mpi(4)
    assert mpi_a >> 1 == 2
    mpi_a >>= 1
    assert mpi_a == 2

def test_getbits(context):
    mpi_a = context.mpi(16) #10000
    assert mpi_a[4] == True
    assert mpi_a[1] == False

def test_setbits(context):
    mpi_a = context.mpi(16) #10000
    mpi_a[0] = True
    assert mpi_a == 17
    mpi_a[0] = False
    assert mpi_a == 16

def test_highbit(context):
    mpi_a = context.mpi(16) #10000
    mpi_a.set_highbit(3) #1000
    assert mpi_a == 8
    mpi_a.clear_highbit(3)
    assert mpi_a == 0

def test_len(context):
    mpi_a = context.mpi(16) #10000
    assert len(mpi_a) == 5

def test_randomize(context):
    assert utils.randomize(1024).value != utils.randomize(1024).value # If we have the same … we have an issue

def test_flags(context):
    a = utils.randomize(512)
    a.secure = True
    assert a.secure == True
    assert a.plop == None

def test_opaque(context):
    mpi_a = context.mpi(b'This is a test')
    assert mpi_a.opaque == True
    assert mpi_a == b'This is a test'

def test_prime(context):
    mpi = context.mpi(3)
    assert mpi.isprime() == True
    mpi = context.mpi(4)
    assert mpi.isprime() == False
