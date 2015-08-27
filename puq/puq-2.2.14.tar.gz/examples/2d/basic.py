from puq import *

def run(level=1):
    # Declare our parameters here.
    x = NormalParameter('x', 'x', mean=3, dev=1)
    y = NormalParameter('y', 'y', mean=10, dev=2)


    # Create a host
    host = InteractiveHost()

    # Declare a UQ method.
    uq = Smolyak([x,y], level=level)

    # Our test program
    prog = TestProgram('./basic_prog.py', desc='Basic identity function')

    return Sweep(uq, host, prog)
