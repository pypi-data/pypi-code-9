from zope import component
from zope.interface import implementer
from zope.interface.interface import InterfaceClass
from zope.interface.exceptions import InvalidInterface
from bst.pygasus.scaffolding.interfaces import IRecipeDescriptive


class ScaffoldingDecorator(object):

    def __init__(self, name, title=None):
        self.name = name
        self.title = title

    def __call__(self, iclass):
        if type(iclass) is not InterfaceClass:
            raise InvalidInterface('%s is not a zope.interface' % iclass)

        if not self.title:
            self.title = iclass.__name__

        gsm = component.getGlobalSiteManager()
        descriptive = ScaffoldingDescriptiveUtility(self.name, iclass, self.title)
        gsm.registerUtility(descriptive, IRecipeDescriptive, self.name.lower())
        return iclass


@implementer(IRecipeDescriptive)
class ScaffoldingDescriptiveUtility(object):

    def __init__(self, classname, interface, title):
        self.classname = classname
        self.interface = interface
        self.title = title
