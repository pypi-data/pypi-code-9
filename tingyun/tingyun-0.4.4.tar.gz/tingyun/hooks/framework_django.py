import logging

from tingyun.api.hooks_entrance import wsgi_application_wrapper
from tingyun.api.tracert.error_trace import wrap_error_trace
from tingyun.api.tracert.function_trace import wrap_function_trace
from wrapper_django import should_ignore, wrap_view_dispatch, wrap_template_block, wrap_url_resolver
from wrapper_django import wrap_url_resolver_nnn, wrap_middleware_trace


_logger = logging.getLogger(__name__)


def detect_django_core_handlers_wsgi(module):
    # Wrap the WSGI application entry point for django.
    import django

    framework = 'Django'
    version = django.get_version()

    wsgi_application_wrapper(module.WSGIHandler, "__call__", (framework, version))


# Post import hooks for modules.
def detect_django_core_handlers_base(module):
    """process the http/response middleware
    :param module: the module need to detect
    :return:
    """
    wrap_middleware_trace(module, 'BaseHandler.load_middleware')


def detect_django_views_generic_base(module):
    """process the views info
    :param module: the views module
    :return:
    """
    module.View.dispatch = wrap_view_dispatch(module.View.dispatch)


def detect_django_core_urlresolvers(module):
    """process the url
    :param module:
    :return:
    """
    # for grab the resolver map error. detect the function name mapping to views, this is base call for resolver
    wrap_error_trace(module, 'get_callable', ignore_errors=should_ignore)

    # wrap the regex url mapping to views. get_callable is used inline
    module.RegexURLResolver.resolve = wrap_url_resolver(module.RegexURLResolver.resolve)

    if hasattr(module.RegexURLResolver, 'resolve403'):
        module.RegexURLResolver.resolve403 = wrap_url_resolver_nnn(module.RegexURLResolver.resolve403, priority=3)

    if hasattr(module.RegexURLResolver, 'resolve404'):
        module.RegexURLResolver.resolve404 = wrap_url_resolver_nnn(module.RegexURLResolver.resolve404, priority=3)

    if hasattr(module.RegexURLResolver, 'resolve500'):
        module.RegexURLResolver.resolve500 = wrap_url_resolver_nnn(module.RegexURLResolver.resolve500, priority=1)


def detect_django_template_loader_tags(module):
    """
    :param module:
    :return:
    """
    module.BlockNode.render = wrap_template_block(module.BlockNode.render)


def detect_django_template(module):
    """ detect the template render
    :param module:
    :return:
    """
    def template_name(template, *args):
        return template.name

    if hasattr(module.Template, '_render'):
        wrap_function_trace(module, 'Template._render', name=template_name, group='Template/Render')

    if hasattr(module.Template, 'render'):
        wrap_function_trace(module, 'Template.render', name=template_name, group='Template/Render')


def detect_django_http_multipartparser(module):
    """ detect for file upload
    :param module:
    :return:
    """
    wrap_function_trace(module, 'MultiPartParser.parse')


def detect_django_core_mail(module):
    """
    :param module:
    :return:
    """
    wrap_function_trace(module, 'mail_admins')
    wrap_function_trace(module, 'mail_managers')
    wrap_function_trace(module, 'send_mail')


def detect_django_core_mail_message(module):
    """
    :param module:
    :return:
    """
    wrap_function_trace(module, 'EmailMessage.send')


# TODO: not detected now.
def detect_django_views_debug(module):
    """
    :param module:
    :return:
    """
    pass
    # module.technical_404_response = wrap_view_handler(module.technical_404_response, priority=3)
    # module.technical_500_response = wrap_view_handler(module.technical_500_response, priority=1)
