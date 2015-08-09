import os
from os.path import join

ROOT = os.path.dirname(os.path.abspath(__file__))
JW_TEMPLATES_SEARCH_PATH = [join(ROOT, 'templates')]
JW_EXEC_PATTERN = 'execute.*'
