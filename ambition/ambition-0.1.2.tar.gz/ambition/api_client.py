#!/usr/bin/env python
# coding: utf-8

"""Swagger generic API client. This client handles the client-
server communication, and is invariant across implementations. Specifics of
the methods and models for each application are generated from the Swagger
templates."""

from __future__ import absolute_import
from .rest import RESTClient
from . import models

import os
import re
import datetime
import mimetypes

# python 2 and python 3 compatibility library
from six import iteritems, text_type

try:
    # for python3
    from urllib.parse import quote
except ImportError:
    # for python2
    from urllib import quote


class ApiClient(object):
    """
    Generic API client for Swagger client library builds

    :type configuration: ``ApiConfiguration``
    :param configuration: The ApiConfiguration for this client
    """
    def __init__(self, configuration):
        self.configuration = configuration
        self.default_headers = {}
        self.host = configuration.host
        # Set default User-Agent.
        self.user_agent = 'Python-Swagger'

    @property
    def user_agent(self):
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        self.default_headers['User-Agent'] = value

    def call_api(
        self, resource_path, method, path_params=None, query_params=None,
        header_params=None, body=None, post_params=None, files=None,
        response=None, auth_settings=['default']
    ):

        # headers parameters
        header_params = header_params or {}
        header_params.update(self.default_headers)
        header_params = self.sanitize_for_serialization(header_params)

        # path parameters
        if path_params:
            path_params = self.sanitize_for_serialization(path_params)
            for k, v in iteritems(path_params):
                replacement = quote(str(self.to_path_value(v)))
                resource_path = resource_path.replace('{' + k + '}', replacement)

        # query parameters
        if query_params:
            query_params = self.sanitize_for_serialization(query_params)
            query_params = {k: self.to_path_value(v) for k, v in iteritems(query_params)}

        # post parameters
        if post_params:
            post_params = self.prepare_post_parameters(post_params, files)
            post_params = self.sanitize_for_serialization(post_params)

        # auth setting
        self.update_params_for_auth(header_params, query_params, auth_settings)

        # body
        if body:
            body = self.sanitize_for_serialization(body)

        # request url
        url = self.host + resource_path

        # perform request and return response
        response_data = self.request(
            method, url, query_params=query_params, headers=header_params,
            post_params=post_params, body=body)

        # deserialize response data
        if response:
            # return a tuple of models if the response is a list of objects
            if type(response_data) in [list, tuple]:
                return (
                    self.deserialize(model, response)
                    for model in response_data
                )
            return self.deserialize(response_data, response)
        else:
            return None

    def to_path_value(self, obj):
        """
        Convert a string or object to a path-friendly value

        :param obj: object or string value

        :return string: quoted value
        """
        if type(obj) == list:
            return ','.join(obj)
        else:
            return str(obj)

    def sanitize_for_serialization(self, obj):
        """
        Sanitize an object for Request.

        If obj is None, return None.
        If obj is str, int, float, bool, unicode, return directly.
        If obj is datetime.datetime, datetime.date convert to string in iso8601 format.
        If obj is list, santize each element in the list.
        If obj is dict, return the dict.
        If obj is swagger model, return the properties dict.
        """
        if isinstance(obj, type(None)):
            return None
        elif isinstance(obj, (int, float, bool, tuple, text_type, str)):
            return obj
        elif isinstance(obj, list):
            return [self.sanitize_for_serialization(sub_obj) for sub_obj in obj]
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        else:
            if isinstance(obj, dict):
                obj_dict = obj
            else:
                # Convert model obj to dict except attributes `swagger_types`, `attribute_map`
                # and attributes which value is not None.
                # Convert attribute name to json key in model definition for request.
                obj_dict = {
                    obj.attribute_map[key]: val
                    for key, val in iteritems(obj.__dict__)
                    if key not in ['swagger_types', 'attribute_map']
                    and val is not None
                }
            return {
                key: self.sanitize_for_serialization(val)
                for key, val in iteritems(obj_dict)
            }

    def deserialize(self, obj, obj_class):
        """
        Derialize a JSON string into an object.

        :param obj: string or object to be deserialized
        :param obj_class: class literal for deserialzied object, or string of class name

        :return object: deserialized object
        """
        # Have to accept obj_class as string or actual type. Type could be a
        # native Python type, or one of the model classes.

        if 'list[' in obj_class:
            match = re.match('list\[(.*)\]', obj_class)
            sub_class = match.group(1)
            return [self.deserialize(sub_obj, sub_class) for sub_obj in obj]
        if obj_class == 'str':
            return text_type(obj)
        if obj_class in ['int', 'float', 'dict', 'list', 'bool']:
            try:
                return eval(obj_class)(obj)
            except TypeError:
                return obj
        if obj_class == 'datetime':
            return self.__parse_string_to_datetime(obj)

        model_class = getattr(models, obj_class)
        return self.deserialize_model(model_class, obj)

    def deserialize_model(self, model_class, obj):
        instance = model_class()
        if obj is None or type(obj) not in [list, dict]:
            return instance
        for attr, attr_type in iteritems(instance.swagger_types):
            if instance.attribute_map[attr] not in obj:
                continue
            value = obj[instance.attribute_map[attr]]
            setattr(instance, attr, self.deserialize(value, attr_type))
        return instance

    def __parse_string_to_datetime(self, string):
        """
        Parse datetime in string to datetime.

        The string should be in iso8601 datetime format.
        """
        from dateutil.parser import parse
        return parse(string)

    def request(self, method, url, query_params=None, headers=None, post_params=None, body=None):
        """
        Perform http request using RESTClient.
        """
        if method == "GET":
            return RESTClient.GET(url, query_params=query_params, headers=headers)
        elif method == "HEAD":
            return RESTClient.HEAD(url, query_params=query_params, headers=headers)
        elif method == "POST":
            return RESTClient.POST(url, headers=headers, post_params=post_params, body=body)
        elif method == "PUT":
            return RESTClient.PUT(url, headers=headers, post_params=post_params, body=body)
        elif method == "PATCH":
            return RESTClient.PATCH(url, headers=headers, post_params=post_params, body=body)
        elif method == "DELETE":
            return RESTClient.DELETE(url, query_params=query_params, headers=headers)
        else:
            raise ValueError("http method must be `GET`, `HEAD`, `POST`, `PATCH`, `PUT` or `DELETE`")

    def prepare_post_parameters(self, post_params=None, files=None):
        params = {}

        if post_params:
            params.update(post_params)

        if files:
            for k, v in iteritems(files):
                with open(v, 'rb') as f:
                    filename = os.path.basename(f.name)
                    filedata = f.read()
                    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                    params[k] = tuple([filename, filedata, mimetype])

        return params

    def select_header_accept(self, accepts):
        """
        Return `Accept` based on an array of accepts provided
        """
        if not accepts:
            return

        accepts = list(map(lambda x: x.lower(), accepts))

        if 'application/json' in accepts:
            return 'application/json'
        else:
            return ', '.join(accepts)

    def select_header_content_type(self, content_types):
        """
        Return `Content-Type` baseed on an array of content_types provided
        """
        if not content_types:
            return 'application/json'

        content_types = list(map(lambda x: x.lower(), content_types))

        if 'application/json' in content_types:
            return 'application/json'
        else:
            return content_types[0]

    def update_params_for_auth(self, headers, querys, auth_settings):
        """
        Update header and query params based on authentication setting
        """
        if not auth_settings:
            return

        for auth in auth_settings:
            auth_setting = self.configuration.auth_settings().get(auth)
            headers[auth_setting['key']] = auth_setting['value']
