import requests
import json


class Request:

  def __init__(self, method):
    self._method = method

  def __patch_data(self, data):
    patched_data = {}
    for key, val in data.items():
      patched_data[key] = json.dumps(val) if (type(val) in [bool, list, dict]) else val
    return patched_data

  def __call__(self, *args, **kwargs):
    if self._method in ['post', 'put', 'patch']:
      if ('data' in kwargs) and (type(kwargs['data']) is dict):
        kwargs['data'] = self.__patch_data(kwargs['data'])
      elif (len(args) > 1) and (type(args[1]) is dict):
        args = list(args)
        args[1] = self.__patch_data(args[1])

    response = getattr(requests, self._method)(*args, **kwargs)
    response.body = response.text
    return response


class Http:

  codes = requests.codes

  def __getattr__(self, name):
    if hasattr(requests, name):
      return Request(name)
    raise AttributeError('http object has no attribute \'{}\''.format(name))
