
"""
"""
import weakref

from tingyun.logistics.basic_wrapper import wrap_object, FunctionWrapper
from tingyun.battlefield.tracer import Tracer
from tingyun.battlefield.proxy import proxy_instance
from tingyun.armoury.trigger.wsgi_django import wsgi_wrapper_inline


def wsgi_application_wrapper(module, object_path, framework, version):
    """
    """
    wrap_object(module, object_path, wsgi_wrapper_inline, (framework, version))


def process_environ(environ, request):
    """the environ in the default environ may not include our need environment variable when apply to wsgi application
    :param environ: returned environment from the container request.
    :param request:
    :return:
    """
    # we need this the build the request information. but not included in the environment.
    ret = {}.update(environ)
    ret["REQUEST_URI"] = request.uri
    ret["HTTP_REFERER"] = request.headers.get('Referer')

    if not environ:
        ret['PATH_INFO'] = request.path
        ret['SCRIPT_NAME'] = ""
        ret['QUERY_STRING'] = request.query

    return ret


def wrap_wsgi_container(wrapped, framework, version):
    """
    :param wrapped:
    :param framework:
    :param version:
    :return:
    """
    def wrapper(wrapped, instance, request, *args, **kwargs):
        """
        """
        tracker = getattr(request, "_self_tracker", None)

        if not tracker:
            tracker = Tracer(proxy_instance(), process_environ(instance.environ, request))
            tracker.start_work()

            # we save the tracker info current request for next use.
            request._self_tracker = tracker
            tracker._self_current_request = weakref.ref(request)
        else:
            pass

    FunctionWrapper(wrapped, wrapper)


def wsgi_container_wrapper(module, object_path, framework, version):
    """
    :param module:
    :param object_path:
    :param framework:
    :param version:
    :return:
    """
    wrap_object(module, object_path, wrap_wsgi_container, (framework, version))
