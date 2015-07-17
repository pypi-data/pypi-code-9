from distutils.core import setup

setup(
    name='MODOI',
    version='1.0',
    packages=['SimulationClient', 'SimulationServer', 'SimulationPotential', 'SimulationUtilities'],
    url='https://suttond.github.io/MODOI',
    license='LGPL 3.0',
    author='Daniel C. Sutton',
    author_email='sutton.c.daniel@gmail.com',
    description='MOlecular Dynamics Over Ip - A boundary value problem solver for Newtons second law in the context of molecular systems. Parallelisation is achieved through TCP/IP. This is the sister project of GMFMD.'
)
