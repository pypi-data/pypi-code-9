"""
Helper for the Python with statement. Helps developers more
neatly, simply, and cleanly access deeply-nested data structures.
"""

class ref(object):
    """Simple with statement guard objects."""

    def __init__(self, obj):
        """Mint one!"""
        self.obj = obj

    def __enter__(self):
        """Here we go!"""
        return self.obj

    def __exit__(self, _type, value, traceback):
        """Well, that was fun!"""
        if isinstance(value, Exception):
            raise value
        else:
            return True
