import os
import sys

USER_DIR = os.getenv(
    'XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config', 'polarbird/')
)
sys.path.insert(0, os.path.realpath(USER_DIR))

from polarbird.polarbird import PolarBird

def start_app():
    pl = PolarBird()
