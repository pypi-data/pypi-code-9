import inspect
import functools
import json
# from flask.exceptions import JSONBadRequest
from werkzeug.exceptions import BadRequest as JSONBadRequest
from traceback import format_exception
from flask import jsonify, request
import sys

from flask import Flask
import re

app = Flask(__name__)

def api_error_response(code=404, message="Requested resource was not found", errors=list()):
    """
        Convenience function for returning a JSON response that includes
        appropriate error messages and code.
    """

    response = jsonify(dict(code=code, message=message, errors=errors, success=False))
    response.status_code = code
    return response

def bad_json_error_response():
    """
        Convenience function for returning an error message related to
        malformed/missing JSON data.
    """

    return api_error_response(code=400,
        message="There was a problem parsing the supplied JSON data.  Please send valid JSON.")


def json_required(func=None, required_fields={}, validations=[]):
    """
        Decorator used to validate JSON input to an API request
    """

    if func is None:
        return functools.partial(json_required, required_fields=required_fields, validations=validations)
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):

        try:
            #If no JSON was supplied (or it didn't parse correctly)
            try:
                if request.json is None:
                    return bad_json_error_response()
            except JSONBadRequest:
                return bad_json_error_response()

            #Check for specific fields
            errors = []

            def check_required_fields(data, fields):
                for field, requirements in fields.iteritems():
                    nested_fields = type(requirements) == dict
                    if data.get(field) in (None, ''):
                        if nested_fields:
                            error_msg = requirements.get('message')
                        else:
                            error_msg = requirements
                        errors.append({'field': field, 'message': error_msg})
                    elif nested_fields:
                        check_required_fields(data[field], requirements.get('fields', {}))

            check_required_fields(request.json, required_fields)

            for validation_field, validation_message, validation_func in validations:
                #func_args = inspect.getargspec(validation_func).args
                #func_params = []
                #for arg in func_args:
                #    func_params.append(request.json.get(arg))

                if not validation_func(request.json,errors,request.json.get(validation_field)):
                    errors.append({'field': validation_field, 'message': validation_message})

            if errors:
                return api_error_response(code=422, message="JSON Validation Failed", errors=errors)

        except Exception:
            #For internal use, nice to have the traceback in the API response for debugging
            #Probably don't want to include for public APIs
            etype, value, tb = sys.exc_info()
            error_info = ''.join(format_exception(etype, value, tb))
            return api_error_response(code=500, message="Internal Error validating API input", errors=[{'message':error_info}])

        return func(*args, **kwargs)

    return decorated_function
