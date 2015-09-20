from setuptools import setup
from spinwarrior import __version__

setup(
    name='PySpinWarrior',
    version=__version__,
    author='Michael V. DePalatis',
    author_email='depalatis@phys.au.dk',
    url='http://phys.au.dk/forskning/forskningsomraader/amo/the-ion-trap-group/',
    description='SpinWarrior control',
    packages=['spinwarrior']
)
