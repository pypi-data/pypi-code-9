

class Range(object):

    def __init__(self, value):

        if ':' in value:
            value = int(value)
        else:
            try:
                value = int(value)
                
