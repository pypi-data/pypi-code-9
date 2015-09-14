from logging import CRITICAL, ERROR, WARN
import string


class RootException(Exception):
    def __init__(self, app_err_code, warning_messages_mapping, error_messages_mapping, fatal_error_messages_mapping,
                 status_code=500, **kwargs):
        error_message = warning_messages_mapping.get(app_err_code) or error_messages_mapping.get(app_err_code) or \
                        fatal_error_messages_mapping.get(app_err_code)

        self.message = {}
        self.app_err_code = app_err_code
        self.error_message = error_message
        self.log_level = self._determine_log_level(app_err_code, warning_messages_mapping, error_messages_mapping,
                                                   fatal_error_messages_mapping)
        self.status_code = status_code
        self.additional_info = kwargs.get('additional_info')
        self._determine_message(kwargs)

    def _determine_message(self, kwargs):
        if self.error_message:
            template = string.Template(self.error_message)
            self.error_message = template.safe_substitute(**kwargs)
        else:
            self.error_message = "**FlaskErrorHandler - Unable to find error code '{}' in provided " \
                                 "error code mapping".format(self.app_err_code)

    def __str__(self):
        return u"%s: %s, status code: %s" % (self.app_err_code, self.error_message, self.status_code)

    @staticmethod
    def _determine_log_level(app_err_code, warning_messages_mapping, error_messages_mapping,
                             fatal_error_messages_mapping):
        if app_err_code in warning_messages_mapping.keys():
            return WARN
        elif app_err_code in error_messages_mapping.keys():
            return ERROR
        elif app_err_code in fatal_error_messages_mapping.keys():
            return CRITICAL

        return CRITICAL


