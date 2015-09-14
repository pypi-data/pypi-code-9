import uuid


class ExceptionHandler(object):

    def __init__(self, app_name, logging_service):
        self.e = None
        self.stack_trace = None
        self.request = None
        self.app_name = app_name
        self.logging_service = logging_service

    def update_with_exception_data(self, exception_obj, app_request, stack_trace):
        self.e = exception_obj
        self.request = app_request
        self.stack_trace = stack_trace

    @staticmethod
    def _create_exception_identifier():
        return uuid.uuid1().hex

    def _construct_error_info(self, code, error_message, additional_info):
        log_id = self._create_exception_identifier()
        return {"app_err_code": (self.app_name + "_" + code).upper(), "logref": log_id,
                "error_message": error_message, "additional_info": additional_info}

    def construct_error_details(self):
        error_details = self._construct_error_info(self.e.app_err_code, self.e.error_message, self.e.additional_info)
        self.logging_service.log_error(self.e.log_level, error_details, self.request, self.stack_trace)
        return error_details

    def get_http_status_code(self):
        return self.e.status_code

