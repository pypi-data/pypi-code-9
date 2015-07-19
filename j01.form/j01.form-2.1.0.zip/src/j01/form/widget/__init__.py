###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Widgets
$Id: __init__.py 4247 2015-06-08 13:35:03Z roger.ineichen $
"""
__docformat__ = 'restructuredtext'

# checkbox
from j01.form.widget.checkbox import getCheckBoxWidget
from j01.form.widget.checkbox import getCheckBoxInlineWidget

from j01.form.widget.checkbox import getSingleCheckBoxWidget
from j01.form.widget.checkbox import getSingleCheckBoxInlineWidget

from j01.form.widget.checkbox import getCheckBoxPickerWidget
from j01.form.widget.checkbox import getCheckBoxInlinePickerWidget

from j01.form.widget.checkbox import getSingleCheckBoxPickerWidget
from j01.form.widget.checkbox import getSingleCheckBoxInlinePickerWidget

# dictionary
from j01.form.widget.dictionary import getDictKeyValueWidget

# file
from j01.form.widget.file import getFileWidget

# multi
from j01.form.widget.multi import getMultiFieldWidget

# password
from j01.form.widget.password import getPasswordWidget
from j01.form.widget.password import getPasswordConfirmationWidget

# radio
from j01.form.widget.radio import getRadioWidget
from j01.form.widget.radio import getRadioInlineWidget
from j01.form.widget.radio import getRadioPickerWidget
from j01.form.widget.radio import getRadioInlinePickerWidget

# select
from j01.form.widget.select import getSelectWidget
from j01.form.widget.select import getMultiSelectWidget
from j01.form.widget.select import getSelectPickerWidget
from j01.form.widget.select import getMultiSelectPickerWidget
from j01.form.widget.select import getGroupSelectWidget

# text and html5 variants
from j01.form.widget.text import getTextWidget
from j01.form.widget.text import getEMailWidget
from j01.form.widget.text import getDateWidget
from j01.form.widget.text import getDatetimeWidget
from j01.form.widget.text import getDatetimeLocalWidget
from j01.form.widget.text import getTimeWidget
from j01.form.widget.text import getWeekWidget
from j01.form.widget.text import getMonthWidget
from j01.form.widget.text import getColorWidget
from j01.form.widget.text import getSearchWidget
from j01.form.widget.text import getURLWidget
from j01.form.widget.text import getNumberWidget
from j01.form.widget.text import getTelWidget

# textlines
from j01.form.widget.textlines import getTextLinesWidget

# textarea
from j01.form.widget.textarea import getTextAreaWidget

# j01.datepicker
try:
    # available if j01.datepicker package is available
    from j01.form.widget.datepicker import getDatePickerWidget
    from j01.form.widget.datepicker import getStartDatePickerWidget
    from j01.form.widget.datepicker import getEndDatePickerWidget
except ImportError:
    pass

# j01.select2
try:
    # available if j01.select2 package is available
    from j01.form.widget.select2 import getSelect2Widget
    from j01.form.widget.select2 import getSingleSelect2Widget
    from j01.form.widget.select2 import getTagListSelect2Widget
    from j01.form.widget.select2 import getLiveListSelect2Widget
except ImportError:
    pass

# j01.selectordered
try:
    from j01.form.widget.selectordered import getOrderedSelectWidget
except ImportError:
    pass

