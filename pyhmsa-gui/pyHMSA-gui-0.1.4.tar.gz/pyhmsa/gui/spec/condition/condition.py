"""
Base widget for conditions
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.gui.util.parameter import ParameterWidget

# Globals and constants variables.

class _ConditionWidget(ParameterWidget):

    def __init__(self, clasz, parent=None):
        ParameterWidget.__init__(self, clasz, parent)

        name = clasz.TEMPLATE
        if clasz.CLASS is not None:
            name += ' (%s)' % clasz.CLASS
        self.setAccessibleName(name)

    def condition(self, condition=None):
        return self.parameter(condition)

    def setCondition(self, condition):
        self.setParameter(condition)
