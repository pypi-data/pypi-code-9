# Import
# ----------------------------------------------------
# python
import os
import sys
import logging
import shutil
# PySide
from PySide import QtGui
from PySide import QtCore


# Import variable
do_reload = True

# ..globals

# global_variables
from ..globals import global_variables as global_variables
if(do_reload):
    reload(global_variables)

# global_functions
from ..globals import global_functions as global_functions
if(do_reload):
    reload(global_functions)

# .

# dock_widget
from . import dock_widget as dock_widget
if(do_reload):
    reload(dock_widget)


# logger
# ------------------------------------------------------------------
logger = logging.getLogger(__name__)
logging_level = logging.DEBUG
logger.setLevel(logging_level)


# Globals
# ------------------------------------------------------------------

# Paths
THIRD_PARTY_PATH = global_variables.THIRD_PARTY_PATH


# DCC
# ----------------------------------------------------

def get_main_window():
    """
    Determine current application and return main window for parenting of own windows.
    """

    # maya
    if (global_functions.check_interpreter('maya')):
        return get_maya_main_window()
    # Nuke
    elif (global_functions.check_interpreter('Nuke')):
        return get_nuke_main_window()

    # Application unknown
    return None


def get_maya_main_window():
    """
    Return the Maya main window.
    """

    try:
        # PySide
        from PySide import QtGui
        from PySide import QtCore
        import shiboken
        # maya
        import maya.OpenMayaUI as open_maya_ui

    except Exception as exception_instance:

        # log
        print('Import failed: {0}'.format(exception_instance))
        # return None
        return None



    # ptr_main_window
    ptr_main_window = open_maya_ui.MQtUtil.mainWindow()

    # if True
    if (ptr_main_window):
        return shiboken.wrapInstance(long(ptr_main_window), QtGui.QMainWindow)

    return None


def get_nuke_main_window():
    """
    Return the Maya main window.
    """

    try:
        # PySide
        from PySide import QtGui
        from PySide import QtCore

    except Exception as exception_instance:

        # log
        print('Import failed: {0}'.format(exception_instance))
        # return None
        return None

    # ptr_main_window
    ptr_main_window = QtGui.QApplication.activeWindow()

    # if True
    if (ptr_main_window):
        return ptr_main_window

    return None


# GUI
# ----------------------------------------------------

def make_dockable(wdgt):
    """
    Determine current application and dock wdgt in it.
    """

    # maya
    if (global_functions.check_interpreter('maya')):
        make_dockable_maya(wdgt)
    # Nuke
    elif (global_functions.check_interpreter('Nuke')):
        make_dockable_nuke(wdgt)
    # unknown
    else:
        # log
        logger.debug('Application unknown or standalone. Not performing any docking.')

def make_dockable_nuke(wdgt):
    """
    Dock wdgt for nuke host application.
    """

    # nuke_main_window
    nuke_main_window = get_nuke_main_window()

    # main_window_list
    main_window_list = nuke_main_window.findChildren(QtGui.QMainWindow)
    # check
    if not (main_window_list):
        # log
        logger.debug('Current Nuke configuration has no QMainWindow instance which is needed for docking\
Not performing dock behaviour.')
        return

    # main_window
    main_window = main_window_list[0]

    # wdgt_dock
    wdgt_dock = dock_widget.DockWidget(parent=main_window)
    wdgt_dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)

    # set wdgt
    wdgt_dock.setWidget(wdgt)

    # add to maya main window
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, wdgt_dock)

def make_dockable_maya(wdgt):
    """
    Dock wdgt for maya host application.
    """

    # main_window
    main_window = get_main_window()

    # wdgt_dock
    wdgt_dock = dock_widget.DockWidget(parent=main_window)
    wdgt_dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)

    # set wdgt
    wdgt_dock.setWidget(wdgt)

    # add to main window
    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, wdgt_dock)

def load_ui_type(ui_file):
    """
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    This function return the form and base classes for the given qtdesigner ui file.
    """

    # add path for integrated pysideuic if it cannot be imported
    try:
        import pysideuic
    except:
        import sys
        sys.path.append(THIRD_PARTY_PATH)

        # log
        logger.debug('pysideuic could not be imported by default.\
Adding tool integrated path to sys: {0}'.format(THIRD_PARTY_PATH))

    # lazy import
    try:
        from cStringIO import StringIO
        import xml.etree.ElementTree as xml
        # PySide
        from PySide import QtGui
        from PySide import QtCore
        from PySide import QtUiTools
        import pysideuic

    except Exception as exception_instance:
        # log
        print('Import failed: {0}'.format(exception_instance))
        # return None
        return None

    # compile ui
    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtGui.%s' % widget_class)

    return form_class, base_class


def get_widget_by_class_name_closure(wdgt_class_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_class_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_class_name from enclosing function.
        ALl this mess to be able to use it with filter.
        """
        try:
            if (type(wdgt).__name__ == wdgt_class_name):
                return True
        except:
            pass
        return False

    return get_widget_by_class_name


def get_widget_by_name_closure(wdgt_name):
    """
    Practicing closures. Doesnt really make sense here, or could at least
    be done much simpler/better.
    Want to try it with filter in order to get more into the builtins.
    """

    def get_widget_by_name(wdgt):
        """
        Function that is closed in. Accepts and checks all
        widgets against wdgt_name from enclosing function.
        ALl this mess to be able to use it with filter.
        """
        try:
            if (wdgt.objectName() == wdgt_name):
                return True
        except:
            pass
        return False

    return get_widget_by_name


def check_and_delete_wdgt_instances_with_class_name(wdgt_class_name):
    """
    Search for all occurences with wdgt_class_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_class_name_closure(wdgt_class_name)

    #wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        #schedule widget for deletion
        try:
            print('Scheduled wdgt {0} for deletion'.format(wdgt.objectName()))
            #delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list


def check_and_close_wdgt_instances_with_class_name(wdgt_class_name):
    """
    Search for all occurences with wdgt_class_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_class_name_closure(wdgt_class_name)

    #wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        #schedule widget for deletion
        try:
            print('Scheduled wdgt {0} for closing'.format(wdgt.objectName()))
            #delete
            wdgt.close()
        except:
            pass

    return wdgt_list


def check_and_delete_wdgt_instances_with_name(wdgt_name):
    """
    Search for all occurences with wdgt_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_name_closure(wdgt_name)

    #wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        #schedule widget for deletion
        try:
            print('Scheduled wdgt {0} for deletion'.format(wdgt.objectName()))
            #delete
            wdgt.deleteLater()
        except:
            pass

    return wdgt_list


def check_and_close_wdgt_instances_with_name(wdgt_name):
    """
    Search for all occurences with wdgt_name and delete them.
    """

    #get_wdgt_closure
    get_wdgt_closure = get_widget_by_name_closure(wdgt_name)

    #wdgt_list
    wdgt_list = filter(get_wdgt_closure, QtGui.QApplication.allWidgets())

    #iterate and delete
    for index, wdgt in enumerate(wdgt_list):

        #schedule widget for deletion
        try:
            print('Scheduled wdgt {0} for closing'.format(wdgt.objectName()))
            #delete
            wdgt.close()
        except:
            pass

    return wdgt_list
