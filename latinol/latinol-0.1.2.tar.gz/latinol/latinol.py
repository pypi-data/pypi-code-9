# coding: utf-8
import re
from functools import partial


RULES = ((ur'cc', ur'ks'),
         (ur'c([aourtláóú])', ur'k\1'),
         (ur'c([eiéí])', ur's\1'),
         (ur'g([eiéí])', ur'j\1'),
         (ur'gu([eiéí])', ur'g\1'),
         (ur'([^cs]|^)h(\S|.|$)', ur'\1\2'),
         (ur'll', ur'y'),
         (ur'qu([eiéí])', ur'k\1'),
         (ur'ü', ur'u'),
         (ur'q([aouáóú])', ur'k\1'),
         (ur'w(\S|.|$)', ur'gu\1'),
         (ur'y([^aeiouáóúéí]|$)', ur'i\1'))


def replace(replacement, match):
    splitted = replacement.split('\\')

    for idx, char in enumerate(splitted):
        try:
            n = int(char)
            splitted[idx] = match.group(n)
        except ValueError:
            pass

    output = u''.join(splitted)
    is_capitalized = match.group(0).strip()[0].isupper()
    is_upper = match.group(0).strip().isupper()

    if is_capitalized:
        if output[0] == u' ':
            output = u' ' + output[1:].capitalize()
        else:
            output = output.capitalize()

    if is_upper:
        output = output.upper()

    return output


def translate(origin):
    # TODO: add a rule for transaccion
    translated = origin

    for rule, replacement in RULES:
        translated = re.sub(rule, partial(replace, replacement), translated, flags=re.I)

    return translated
