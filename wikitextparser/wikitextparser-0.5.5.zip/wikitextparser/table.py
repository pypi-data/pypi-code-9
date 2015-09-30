"""Class and functions to facilate working with tables."""

import re


class Table:

    """Used to parse and manipulate Wikitables."""

    
    def __init__(self, wikitext):
        """Prepare the Table object."""
        
