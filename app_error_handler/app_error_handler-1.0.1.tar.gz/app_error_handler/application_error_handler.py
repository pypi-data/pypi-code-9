import json
import traceback
from werkzeug.wrappers import Request, Response
from app_error_handler.exception_handling_service import ExceptionHandler
from app_error_handler.logging_service import LoggingService
from app_error_handler.root_exception import RootException


def register_app_for_error_handling(wsgi_app, app_name, app_logger, custom_logging_service=None):
    """Wraps a WSGI app and handles uncaught exceptions and defined exception and outputs a the exception in a
    structured format.
    Parameters:
    - wsgi_app is the app.wsgi_app of flask,
    - app_name should in correct format e.g. APP_NAME_1,
    - app_logger is the logger object"""

    logging_service = LoggingService(app_logger) if custom_logging_service is None else custom_logging_service
    exception_manager = ExceptionHandler(app_name, logging_service)

    def wrapper(environ, start_response):
        try:
            return wsgi_app(environ, start_response)
        except RootException as e:
            app_request = Request(environ)
            stack_trace = traceback.format_exc().splitlines()[-1]
            exception_manager.update_with_exception_data(e, app_request, stack_trace)
        except Exception:
            app_request = Request(environ)
            stack_trace = traceback.format_exc()
            e = RootException("FATAL_000", {}, {}, {}, status_code=500)
            e.error_message = "Unknown System Error"
            exception_manager.update_with_exception_data(e, app_request, stack_trace)

        error_details = exception_manager.construct_error_details()
        http_status_code = exception_manager.get_http_status_code()
        response = Response(json.dumps(error_details), status=http_status_code, content_type='application/json')

        return response(environ, start_response)
    return wrapper

