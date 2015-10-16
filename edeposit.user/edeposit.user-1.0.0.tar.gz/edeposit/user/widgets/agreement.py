from zope.interface import implementer, implements, implementsOnly
from zope.component import adapter
from edeposit.user.producent import IAgreementFileField

from z3c.form.interfaces import IFieldWidget, IFormLayer, IDataManager, NOVALUE
from z3c.form.widget import FieldWidget
from plone.formwidget.namedfile.widget import NamedFileWidget
from interfaces import IAgreementFileWidget

class AgreementFileWidget(NamedFileWidget):
    implements(IAgreementFileWidget)
    pass

@implementer(IFieldWidget)
@adapter(IAgreementFileField, IFormLayer)
def AgreementFileFieldWidget(field, request):
    return FieldWidget(field, AgreementFileWidget(request))
