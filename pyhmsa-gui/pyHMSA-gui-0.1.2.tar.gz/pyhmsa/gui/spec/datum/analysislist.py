"""
Analysis list widgets
"""

# Standard library modules.

# Third party modules.
from PySide.QtGui import QSlider, QFormLayout
from PySide.QtCore import Qt

# Local modules.
from pyhmsa.gui.spec.datum.datum import _DatumWidget
from pyhmsa.gui.spec.datum.analysis import \
    (Analysis0DTableWidget, Analysis1DGraphWidget, Analysis1DTableWidget,
     Analysis2DGraphWidget, Analysis2DTableWidget)

from pyhmsa.spec.datum.analysislist import \
    AnalysisList0D, AnalysisList1D, AnalysisList2D

# Globals and constants variables.

class _AnalysisListWidget(_DatumWidget):

    def __init__(self, clasz, controller, datum=None, parent=None):
        self._datum = None
        _DatumWidget.__init__(self, clasz, controller, datum, parent)

    def _init_ui(self):
        # Widgets
        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setTickPosition(QSlider.TicksBelow)

        self._wdg_analysis = self._create_analysis_widget()

        # Layouts
        layout = _DatumWidget._init_ui(self)

        sublayout = QFormLayout()
        sublayout.addRow('Analyses', self._slider)
        layout.addLayout(sublayout)

        layout.addWidget(self._wdg_analysis)

        # Signals
        self._slider.valueChanged.connect(self._onSlide)

        return layout

    def _create_analysis_widget(self):
        raise NotImplementedError

    def _onSlide(self, value):
        if self._datum is None:
            return
        analysis = self._datum.toanalysis(value)
        self._wdg_analysis.setDatum(analysis)

    def setDatum(self, datum):
        _DatumWidget.setDatum(self, datum)
        self._datum = datum
        self._slider.setMaximum(datum.analysis_count - 1)
        self._slider.setValue(0)
        self._onSlide(0)

class AnalysisList0DTableWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList0D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis0DTableWidget(self.controller)

class AnalysisList1DTableWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList1D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis1DTableWidget(self.controller)

class AnalysisList1DGraphWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList1D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis1DGraphWidget(self.controller)

class AnalysisList2DTableWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList2D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis2DTableWidget(self.controller)

class AnalysisList2DGraphWidget(_AnalysisListWidget):

    def __init__(self, controller, datum=None, parent=None):
        _AnalysisListWidget.__init__(self, AnalysisList2D, controller,
                                     datum, parent)

    def _create_analysis_widget(self):
        return Analysis2DGraphWidget(self.controller)
