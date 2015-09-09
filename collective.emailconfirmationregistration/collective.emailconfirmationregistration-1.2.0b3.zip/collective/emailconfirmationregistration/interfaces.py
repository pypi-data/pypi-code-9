try:
    from collective.registrationcaptcha.interfaces import IBrowserLayer as IBaseLayer
except:
    from zope.publisher.interfaces.browser import IDefaultBrowserLayer as IBaseLayer


class ILayer(IBaseLayer):
    pass