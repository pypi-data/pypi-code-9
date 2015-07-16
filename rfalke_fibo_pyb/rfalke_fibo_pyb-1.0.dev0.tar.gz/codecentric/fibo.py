import sh

def fib(n):
    '''
Berechnet die Fibonacci-Nummer. Beispiel:
>>> fib(15)
610
    '''
    if n <= 2: return 1
    return fib(n - 1) + fib(n - 2)

def use_dep():
    print sh.ls("/tmp")
