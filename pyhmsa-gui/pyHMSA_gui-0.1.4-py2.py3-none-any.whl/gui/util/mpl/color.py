"""
Utilities for color between matplotlib and PySide
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QColor

import matplotlib.colors as colors

# Local modules.

# Globals and constants variables.

def convert_color_qt_to_mpl(color):
    return (color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0)

def convert_color_mpl_to_qt(color):
    r, g, b = colors.colorConverter.to_rgb(color)
    return QColor(int(r * 255), int(g * 255), int(b * 255))