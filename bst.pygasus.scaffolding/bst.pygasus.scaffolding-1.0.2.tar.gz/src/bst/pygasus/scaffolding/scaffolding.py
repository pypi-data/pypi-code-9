import re
import fanstatic
from webob.exc import HTTPNotFound

from zope.component import queryUtility
from zope.component import queryMultiAdapter

from bst.pygasus.core import ext
from bst.pygasus.core.interfaces import IApplicationContext

from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.wsgi.interfaces import IRootDispatcher

from bst.pygasus.scaffolding.interfaces import IRecipeDescriptive
from bst.pygasus.scaffolding.interfaces import IScaffoldingRecipe


REGEX_URL = re.compile(r'^\/scaffolding\/([A-z_]*)\/([A-z_]*)\..*')


@ext.implementer(IRootDispatcher)
class ScaffoldinglEntryPoint(ext.MultiAdapter):
    """ generate a index html. This html site will than
        load extjs framework with css and run the
        application.
    """
    ext.name('scaffolding')
    ext.adapts(IApplicationContext, IRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        match = REGEX_URL.match(self.request.path_info)
        if match is None:
            raise HTTPNotFound()
        recipename, descname = match.groups()
        recipename, descname = recipename.lower(), descname.lower()

        descriptive = queryUtility(IRecipeDescriptive, descname)
        if descriptive is None:
            raise HTTPNotFound('No scaffolding for %s' % descname)
        recipe = queryMultiAdapter((self.context, descriptive, self.request,), IScaffoldingRecipe, recipename)
        if recipe is None:
            raise Exception('Missing Recipe to generate Exjs %s' % recipename)

        self.request.response.content_type = 'application/javascript'
        self.request.response.write(recipe())
