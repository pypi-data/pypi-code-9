import json
import fanstatic

from zope.interface import implementer
from zope.component import subscribers

from grokcore import component

from bst.pygasus.core.interfaces import IBaseUrl
from bst.pygasus.core.interfaces import IApplicationContext

from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.wsgi.interfaces import IRootDispatcher

from bst.pygasus.resources.interfaces import IClassPathMapping


CLASS_PATH_MAPPER = 'Ext.Loader.addClassPathMappings(%s);'


@implementer(IRootDispatcher)
class BootstrapEntryPoint(component.MultiAdapter):
    """ generate a boostrap.js with all
        required class-path-mappings.
    """
    component.name('bootstrap')
    component.adapts(IApplicationContext, IRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.request.response.content_type = 'application/javascript'

        mapping = dict()
        for mapper in subscribers((self.context,), IClassPathMapping):
            mapping[mapper.namespace] = IBaseUrl(self.request).url(mapper.path)

        out = json.dumps(mapping, indent=' ' * 4)
        self.request.response.write(CLASS_PATH_MAPPER % out)
        self.request.response.content_type = 'application/javascript'
