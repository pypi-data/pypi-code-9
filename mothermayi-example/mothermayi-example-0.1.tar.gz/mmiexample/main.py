import itertools
import mothermayi.colors

def plugin():
    return {
        'name'          : 'example',
        'pre-commit'    : pre_commit,
    }

DESCRIPTIONS = [
    'nice',
    'cute',
    'splendid',
    'metaphysical',
    'majestic',
    'anti-social',
]
def _to_description(f):
    index = sum([int(ord(c)) for c in f]) % len(DESCRIPTIONS)
    return DESCRIPTIONS[index]

def pre_commit(config, staged):
    descriptions = [_to_description(s) for s in staged]
    descriptions = [mothermayi.colors.green(d) for d in descriptions]
    lines = ["  {}...looks {}".format(s, d) for s, d in itertools.izip(staged, descriptions)]
    return "\n".join(lines)
