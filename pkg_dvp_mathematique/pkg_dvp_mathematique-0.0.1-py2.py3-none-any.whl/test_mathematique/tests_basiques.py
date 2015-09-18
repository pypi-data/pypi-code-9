import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from mathematique.operations_basiques import addition
from mathematique.operations_basiques import soustraction
from mathematique.operations_basiques import multiplication
from mathematique.operations_basiques import division

def test_addition():
    result = addition(1, 2)
    if result == 3:
        print('Test addition OK')
    else:
        print('Test addition KO')

def test_soustraction():
    result = soustraction(3, 2)
    if result == 1:
        print('Test soustraction OK')
    else:
        print('Test soustraction KO')

def test_multiplication():
    result = multiplication(2, 3)
    if result == 6:
        print('Test multiplication OK')
    else:
        print('Test multiplication KO')

def test_division():
    result = division(float(3), 4)
    if result == 0.75:
        print('Test division OK')
    else:
        print('Test division KO')


if __name__ == '__main__':
    test_addition()
    test_soustraction()
    test_multiplication()
    test_division()
