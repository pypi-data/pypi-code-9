from bst.pygasus.core import ext
from js.extjs.theme import themes

from zope import schema
from zope.interface import Interface
from zope.component import getUtility

from fanstatic import Library
from fanstatic import Resource

from bst.pygasus.security import _
from bst.pygasus.security.plugins import FORM_LOGIN
from bst.pygasus.security.plugins import FORM_PASSWORD
from bst.pygasus.security.interfaces import IAuthentication
from bst.pygasus.core.interfaces import DEFAULT_EXTJS_APPLICATION


library = Library('securtiylogin', 'applogin')
style = Resource(library, 'resources/style.css')


class LoginPageContext(ext.ApplicationContext):
    """ Base class to easily create a login page in your
        application. All you need is inherited in your project.
    """
    ext.baseclass()
    ext.name('login')

    title = 'Login Page'
    application = 'extjs.security.LoginPageApplication'
    namespace = 'extjs.security'
    resources = Resource(library, 'application.js',
                         depends=[ext.extjs_resources_skinless,
                                  themes['neptune'],
                                  style])

    credentials_pluggins = ('request_credentials',)
    authentication_pluggins = ()


class AppClassPathMapping(ext.ClassPathMapping):
    namespace = 'extjs.security'
    path = 'fanstatic/securtiylogin'


@ext.scaffolding('Credentials')
class ICredentials(Interface):

    login = schema.TextLine(title=_('tr_lbl_username', default='Username'),
                            required=True)

    password = schema.Password(title=_('tr_lbl_password', default='Password'),
                               required=True)

    success = schema.Bool(title='Success',
                          required=False)

    defaultredirect = schema.TextLine(title='default redirect',
                                      required=False)


class Credentials(ext.Model):
    ext.schema(ICredentials)
    login = ''
    password = ''
    success = False
    defaultredirect = DEFAULT_EXTJS_APPLICATION


class CredentialsHandler(ext.AbstractModelHandler):
    """ This handler will just push the credential to request. After that a
        credential-plugin will create the information for the auth-plugin.
    """
    ext.adapts(Credentials, ext.IRequest)

    def get(self, model, batch):
        """ just return a empty list
        """
        return [model], 1

    def create(self, model):
        raise NotImplementedError('not possible...')

    def delete(self, model):
        raise NotImplementedError('not possible...')

    def update(self, model, batch):
        self.request.GET.add(FORM_LOGIN, model.login)
        self.request.GET.add(FORM_PASSWORD, model.password)

        principal = getUtility(IAuthentication).authenticate(self.request)
        model.success = principal is not None
        return [model], 1
