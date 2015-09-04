from .hello import hello_world
from .namaste import namaste_duniya

from .packchild.hola import hola

def hello_and_namaste():
    hello_world()
    namaste_duniya()
    hola()

if __name__ == '__main__':
    hello_and_namaste()