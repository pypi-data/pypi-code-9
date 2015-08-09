# Import
# ------------------------------------------------------------------
# import
import os
import logging
# PySide
from PySide import QtGui


# logger
# ------------------------------------------------------------------
logger = logging.getLogger(__name__)
logging_level = logging.DEBUG
logger.setLevel(logging_level)


# Globals
# ------------------------------------------------------------------

# Administration
TITLE = 'Boilerplate DCC PySide Widget'
VERSION = '0.0.1'
LOGGING_LEVEL = logging.DEBUG

# Paths
TOOL_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              os.path.pardir,
                                              os.path.pardir))

MEDIA_PATH = os.path.join(TOOL_ROOT_PATH, 'media')
UI_PATH = os.path.join(MEDIA_PATH, 'ui')
ICONS_PATH = os.path.join(MEDIA_PATH, 'icons')
FONTS_PATH = os.path.join(MEDIA_PATH, 'fonts')

LIBRARY_PATH = os.path.join(TOOL_ROOT_PATH, 'lib')
THIRD_PARTY_PATH = os.path.join(LIBRARY_PATH, 'third_party')


# Fonts [(font_name, font_file_name)]
FONTS_LIST = [('Futura LT Light', 'futura-lt-light.ttf')]
# install
for index, current_font_tuple in enumerate(FONTS_LIST):
    # current_font_name, current_font_file_name
    current_font_name, current_font_file_name = current_font_tuple
    # check
    if not (current_font_name in QtGui.QFontDatabase().families()):
        # current_font_path
        current_font_path = os.path.join(FONTS_PATH, current_font_file_name).replace('\\', '/')
        # add
        QtGui.QFontDatabase.addApplicationFont(current_font_path)
        # log
        logger.debug('Installed tool relative font: {0} from {1}'.format(current_font_name,
                                                                         current_font_path))
