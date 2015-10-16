import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser import widget

from .interfaces import IISBNWidget
from z3c.form.browser.text import TextWidget
from plone import api

@zope.interface.implementer_only(IISBNWidget)
class ISBNWidget(TextWidget):
    """Input type text widget implementation."""

    klass = u'isbn-widget'
    
    def canChangeISBN(self):
        mtool = api.portal.get_tool('portal_membership')
        result= mtool.checkPermission('Modify portal content', self.context)
        return result

    def update(self):
        super(ISBNWidget, self).update()


@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def ISBNFieldWidget(field, request):
    return FieldWidget(field, ISBNWidget(request))
