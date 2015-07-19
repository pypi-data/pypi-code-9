

def dashed_lower(config_name):
    parts = config_name.split('_')
    formatted = '-'.join(p.lower() for p in parts)
    return formatted


def dotted_lower(config_name):
    parts = config_name.split('_')
    formatted = '.'.join(p.lower() for p in parts)
    return formatted
