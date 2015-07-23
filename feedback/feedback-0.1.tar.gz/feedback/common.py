import sys

class _Common(object):
    """
    Common class for sharing attributes with child classes
    for the feedback module.
    """
    def __init__(self):
        
        # Stream / color boolean / color values / label width
        self.stream = sys.stdout
        self.colors = self._has_colors()
        self.color  = { 'red': '31', 'green': '32', 'yellow': '33' }
        self.width  = 9
        
    def _has_colors(self):
        """
        Check if the terminal supports colors
        
        :rtype: boolean
        """
        if not hasattr(self.stream, 'isatty'):
            return False
        if not self.stream.isatty():
            return False
        try:
            import curses
            curses.setupterm()
            return curses.tigetnum('colors') > 2
        except:
            return False