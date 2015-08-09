
# Import
# ------------------------------------------------------------------
# python
import logging
# PySide
from PySide import QtGui


# Globals
# ------------------------------------------------------------------


# DockWidget class
# ------------------------------------------------------------------
class DockWidget(QtGui.QDockWidget):
    """
    Subclass of QDockWidget to allow for custom styling
    """

    def __new__(cls, *args, **kwargs):
        """
        Instance factory.
        """

        # wdgt_instance
        wdgt_instance = super(DockWidget, cls).__new__(cls, args, kwargs)

        return wdgt_instance

    def __init__(self,
                 logging_level= logging.DEBUG,
                 parent=None):
        """
        DockWidget instance customization.
        """

        # parent_class
        self.parent_class = super(DockWidget, self)
        self.parent_class.__init__(parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)
        
        # instance variables
        # ------------------------------------------------------------------
        
        # logger
        # ------------------------------------------------------------------
        # logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        # stylesheets
        # ------------------------------------------------------------------

        # Init procedure
        # ------------------------------------------------------------------

        # setup_ui
        self.setup_ui()

        # connect_ui
        self.connect_ui()

        # style_ui
        self.style_ui()

    # UI setup methods
    # ------------------------------------------------------------------
    
    def setup_ui(self):
        """
        Setup UI.
        """

        pass

    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """
        
        pass

    def style_ui(self):
        """
        Style UI widgets.
        """
        
        pass

    # Getter & Setter
    # ------------------------------------------------------------------

    #  Methods
    # ------------------------------------------------------------------

    # Events
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        # log
        self.logger.debug('Close Event')

        # parent close event
        self.parent_class.closeEvent(event)
