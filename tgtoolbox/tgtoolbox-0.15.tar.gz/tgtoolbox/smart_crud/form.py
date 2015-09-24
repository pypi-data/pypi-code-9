# -*- coding: utf-8 -*-
import tw2.bootstrap.forms as twf
from tg import url
from sprox.formbase import AddRecordForm, EditableForm
from sprox.sa.widgetselector import SAWidgetSelector

__author__ = 'vahid'

class SmartWidgetSelector(SAWidgetSelector):
    def select(self, field):
        w = super(SmartWidgetSelector, self).select(field)
        w.css_class = 'form-control'
        return w


class SmartAddForm(AddRecordForm):
    __base_widget_type__= twf.BootstrapForm
    __widget_selector_type__ = SmartWidgetSelector
    __base_widget_args__ = {'action': url('./')}

class SmartEditForm(EditableForm):
    __base_widget_type__= twf.BootstrapForm
    __widget_selector_type__ = SmartWidgetSelector
    __base_widget_args__ = {'action': url('./')}

