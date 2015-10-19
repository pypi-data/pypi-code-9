import json


class json_response_body:

  def __init__(self, fn):
    self._fn = fn

  def __call__(self, *args, **kwargs):
    response = self._fn(*args, **kwargs)
    if type(response.body) is str:
      response.body = json.loads(response.body)
    return response
