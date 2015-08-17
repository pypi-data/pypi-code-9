# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import QueryDict
from rest_framework.views import APIView
from hipster_api.fields.base import Field


class HManager(object):

    def __init__(self):
        self.__fields = {}
        self.__request = None

    def __setitem__(self, key, value):
        if key == '__request':
            self.__request = value
        else:
            self.__fields[key] = value

    def __getattr__(self, key):
        if key not in ['_HManager__fields', '_HManager__request']:
            instance = self.__fields.get(key)
            instance.to_rules(self.__request)
            return instance.value


class HView(APIView):

    def __init__(self, **kwargs):
        self.objects = HManager()
        super(HView, self).__init__(**kwargs)

    def initialize_request(self, request, *args, **kwargs):
        new_request = super(HView, self).initialize_request(request, *args, **kwargs)

        init_dict = QueryDict('', mutable=True)
        post = getattr(new_request, 'POST', QueryDict(''))
        data = getattr(new_request, 'data', False)
        init_dict.update(getattr(new_request, 'GET', QueryDict('')))

        if data:
            init_dict.update(data)
        elif len(post) > 0:
            init_dict.update(post)

        self.__set_media(init_dict)
        self.objects['__request'] = new_request

        return new_request

    def __set_media(self, data):
        for key, val in self.__class__.__dict__['Fields'].__dict__.items():
            if isinstance(val, Field):
                val.setitem(data.get(key, val.default)).to_python()
                self.objects[key] = val
