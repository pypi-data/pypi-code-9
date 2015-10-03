"""
General run test
"""

import sys
from package import main

def test10():
    sys.argv = ['main.py', '--dry-run']
    main.Main()
