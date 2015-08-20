SELF_CLOSING_TAG = ['area', 'base', 'br', 'col', 'command',
                    'embed', 'hr', 'img', 'input', 'keygen',
                    'link', 'meta', 'param', 'source', 'track',
                    'wbr']

def is_self_closing(tag):
    return tag in SELF_CLOSING_TAG
