import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
USER_DIR = os.path.join(os.path.expanduser('~'), '.polarbird/')
sys.path.insert(0, os.path.realpath(BASE_DIR))
sys.path.insert(1, os.path.realpath(USER_DIR))

from polarbird.polarbird import PolarBird

def start_app():
    pl = PolarBird()
