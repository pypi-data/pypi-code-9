# -*- coding: utf-8 -*-


from unidecode import unidecode
import re


def normalize(string):
    """
        Normalize a string given in parameter.
        Accented characters are converted (Ex.: 'é' to 'e').
        Non alphanumeric characters are converted to whitespace (Ex.: '.' to ' ').
        Extra whitespace characters are removed (Ex.: '   ' to ' ').
        Leading and trailing whitespace characters are removed (Ex.: ' Paris ' to 'Paris').
    """

    if string:
        normalized = unidecode(unicode(string))
        normalized = re.sub("[^A-Za-z0-9]", " ", normalized)
        normalized = re.sub('\s+', ' ', normalized).strip()
        normalized = normalized.lower()
        return normalized
    else:
        return None
