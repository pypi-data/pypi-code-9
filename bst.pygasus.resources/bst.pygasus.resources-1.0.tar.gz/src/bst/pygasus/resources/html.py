import fanstatic
from genshi.core import Markup
from grokcore import component
from bst.pygasus.core.interfaces import IApplicationContext

from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.wsgi.interfaces import IRootDispatcher

from bst.pygasus.resources import loader


@component.implementer(IRootDispatcher)
class HtmlEntryPoint(component.MultiAdapter):
    """ generate a index html. This html site will than
        load extjs framework with css and run the
        application.
    """
    component.name('index')
    component.adapts(IApplicationContext, IRequest)

    tmpl = loader.load('index.html')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        resources = fanstatic.get_needed()
        stream = self.tmpl.generate(resources=Markup(resources.render()),
                                    title=self.context.title,
                                    launcher=Markup(self.launcher()))
        self.request.response.mimetype = 'text/html'
        self.request.response.write(stream.render('html', doctype='html'))

    def launcher(self):
        """ create a js script that launch the application.
        """

        js = """
            Ext.onReady(function() {
                Ext.application('%s');
            });
        """
        return js % self.context.application
