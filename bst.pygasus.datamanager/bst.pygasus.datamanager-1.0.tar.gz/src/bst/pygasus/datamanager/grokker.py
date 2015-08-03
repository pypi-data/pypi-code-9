import martian
from martian.error import GrokError
from grokcore.component import name as namedirective

from zope import component
from bst.pygasus.datamanager.model import ExtBaseModel
from bst.pygasus.datamanager.interfaces import IModelTransformer
from bst.pygasus.datamanager.transformer import ModelTransfomerUtility


class schema(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = None


class ExtModelGrokker(martian.ClassGrokker):
    martian.component(ExtBaseModel)
    martian.directive(schema)
    martian.directive(namedirective)

    def execute(self, class_, schema, name, **kw):
        if schema is None:
            raise GrokError('Class %s is missing directive "schema". Need a Interface\
                             to create the model.' % class_, class_)

        if not name:
            name = class_.__name__

        gsm = component.getGlobalSiteManager()
        transformer = ModelTransfomerUtility(class_, schema)
        gsm.registerUtility(transformer, IModelTransformer, name)
        return True
