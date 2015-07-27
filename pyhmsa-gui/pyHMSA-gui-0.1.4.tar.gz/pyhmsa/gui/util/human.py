"""
Convert code to human readable text
"""

# Standard library modules.
import re

# Third party modules.

# Local modules.

# Globals and constants variables.
_CAMELCASE_TO_WORDS_PATTERN = re.compile('([A-Z][a-z0-9]*)')

def camelcase_to_words(text):
    words = _CAMELCASE_TO_WORDS_PATTERN.split(text)
    return [word for word in words if word]