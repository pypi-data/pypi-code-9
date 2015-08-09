
# Import
# ------------------------------------------------------------------
# python
import os
import logging
# PySide
from PySide import QtCore


# Import variable
do_reload = True

# .lib.globals

# global_variables
from .lib.globals import global_variables as global_variables
if(do_reload):
    reload(global_variables)

# global_functions
from .lib.globals import global_functions as global_functions
if(do_reload):
    reload(global_functions)

# .lib.gui

# dock_widget
from .lib.gui import dock_widget as dock_widget
if(do_reload):
    reload(dock_widget)

# gui_functions
from .lib.gui import gui_functions as gui_functions
if(do_reload):
    reload(gui_functions)


# Globals
# ------------------------------------------------------------------

# Administration
TITLE = global_variables.TITLE
VERSION = global_variables.VERSION

# Pathes
TOOL_ROOT_PATH = global_variables.TOOL_ROOT_PATH
UI_PATH = global_variables.UI_PATH
MEDIA_PATH = global_variables.MEDIA_PATH
ICONS_PATH = global_variables.ICONS_PATH


# form_class, base_class
# ------------------------------------------------------------------

# ui_file_path
ui_file_name = 'boilerplate_dcc_pyside_widget.ui'
ui_file_path = os.path.join(UI_PATH, ui_file_name)

# form_class, base_class
form_class, base_class = gui_functions.load_ui_type(ui_file_path)


# BoilerplateDccPysideWidget class
# ------------------------------------------------------------------
class BoilerplateDccPysideWidget(form_class, base_class):
    """
    BoilerplateDccPysideWidget
    """

    def __new__(cls, *args, **kwargs):
        """
        Instance factory.
        """

        # delete and cleanup old instances
        gui_functions.check_and_close_wdgt_instances_with_class_name(cls.__name__)
        gui_functions.check_and_delete_wdgt_instances_with_class_name(cls.__name__)
        # delete possible dock wdgt instances
        gui_functions.check_and_close_wdgt_instances_with_class_name(dock_widget.DockWidget.__name__)
        gui_functions.check_and_delete_wdgt_instances_with_class_name(dock_widget.DockWidget.__name__)

        # wdgt_instance
        wdgt_instance = super(BoilerplateDccPysideWidget, cls).__new__(cls, args, kwargs)

        return wdgt_instance

    
    def __init__(self,
                 dock_it=True,
                 logging_level=logging.DEBUG,
                 parent=gui_functions.get_main_window()):
        """
        Customize instance.
        """

        # super
        self.parent_class = super(BoilerplateDccPysideWidget, self)
        self.parent_class.__init__(parent)

        # setObjectName
        self.setObjectName(self.__class__.__name__)

        # logger
        # ------------------------------------------------------------------
        # logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logging_level = logging_level
        self.logger.setLevel(self.logging_level)

        # instance variables
        # ------------------------------------------------------------------
        # title
        self.title = TITLE +' ' + str(VERSION)

        # dock_it
        self.dock_it = dock_it

        # init procedure
        # ------------------------------------------------------------------
        
        # setupUi
        self.setupUi(self)

        # setup_additional_ui
        self.setup_additional_ui()

        # connect_ui
        self.connect_ui()

        # style_ui
        self.style_ui()

        # test_methods
        self.test_methods()

        # dock_it
        if (self.dock_it):
            gui_functions.make_dockable(self)

    # Main UI setup methods
    # ------------------------------------------------------------------
    
    def setup_additional_ui(self):
        """
        Setup additional UI.
        """

        # make sure its floating intead of embedded
        self.setWindowFlags(QtCore.Qt.Window)
        # delete on close
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        #set title
        self.setWindowTitle(self.title)

    def connect_ui(self):
        """
        Connect UI widgets with slots or functions.
        """

        pass

    def style_ui(self):
        """
        Setup tool palette, tool stylesheet and specific widget stylesheets.
        """

        pass

    # Test
    # ------------------------------------------------------------------

    def dummy_method(self, msg='dummy'):
        """
        Dummy method
        """

        #log
        self.logger.debug('{0}'.format(msg))
        #print
        print('{0}'.format(msg))

    def test_methods(self):
        """
        Suite of test methods to execute on startup.
        """

        #log
        self.logger.debug('\n\nExecute test methods:\n-----------------------------')

        #dummy_method
        self.dummy_method()

        #log
        self.logger.debug('\n\n-----------------------------\nFinished test methods.')

    # Events
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        """
        Customized closeEvent
        """

        #log
        self.logger.debug('Close Event')

        #parent close event
        self.parent_class.closeEvent(event)


#Run
#------------------------------------------------------------------

def run():
    """
    Standardized run() method
    """
    
    # wdgt_instance
    wdgt_instance = BoilerplateDccPysideWidget()
    wdgt_instance.show()

def delete_ui():
    """
    Delete method that must be called prior to reloading this very module, because otherwise PySide from Maya 2014
    upward will behave broken and you get a - object has no attribute 'winEvent' - error. Prior to Maya 2014
    this was NOT needed. This code does the same as what was done more elegant in the constructor before.
    :return:
    """

    # close wdgt
    gui_functions.check_and_close_wdgt_instances_with_class_name(BoilerplateDccPysideWidget.__name__)
    # delete wdgt
    gui_functions.check_and_delete_wdgt_instances_with_class_name(BoilerplateDccPysideWidget.__name__)
    # close possible dock wdgt instance
    gui_functions.check_and_close_wdgt_instances_with_class_name(dock_widget.DockWidget.__name__)
    # delete possible dock wdgt instance
    gui_functions.check_and_delete_wdgt_instances_with_class_name(dock_widget.DockWidget.__name__)
