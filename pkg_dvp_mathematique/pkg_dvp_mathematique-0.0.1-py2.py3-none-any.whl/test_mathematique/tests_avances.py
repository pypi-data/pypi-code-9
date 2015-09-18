import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from mathematique.operations_avances import puissance
from mathematique.operations_avances import racine_x

def test_puissance():
    result = puissance(2, 3)
    if result == 8:
        print('Test puissance OK')
    else:
        print('Test puissance KO')

def test_racine_x():
    result = racine_x(float(8), 3)
    if result == 2:
        print('Test racine_x OK')
    else:
        print('Test racine_x KO')


if __name__ == '__main__':
    test_puissance()
    test_racine_x()
