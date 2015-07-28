# kvpbase Python SDK
import requests
import json

class response(object):
  # class variables
  body = None
  status_code = None

  #constructor
  def __init__(self, response):
    self.response_body = response.text
    self.status_code = response.status_code

class kvpbase(object):
	# class variables
  api_key   = None
  endpoint  = None
  user_guid = None

  # constructor
  def __init__(self, user_guid=None, api_key=None, endpoint=None):
    self.user_guid = user_guid
    self.api_key = api_key
    self.endpoint = endpoint

  # public methods by operation
  # class methods must have 'self' in the signature but not explicitly
  # included when called (included implicitly)
  def create_container(self, path):
    url = path + '?container=true'
    return self.put(url, None, None)

  def get_obj(self, path):
    return self.get(path)

  def get_container(self, path):
    url = path + '?container=true'
    return self.get(url)

  def create_obj_specific_name(self, path, data, content_type):
    return self.put(path, data, content_type)

  def create_obj_system_name(self, path, data, content_type):
    return self.post(path, data, content_type)

  def delete_obj(self, path):
    return self.delete(path)

  def delete_container(self, path):
    url = path + '?container=true'
    return self.delete(url)

  def container_exists(self, path):
    url = path + '?container=true'
    return self.head(url)

  def obj_exists(self, path):
    return self.head(path)

  def move_obj(self, from_container, move_from, to_container, move_to):
    # from_container and to_container should be provided as an array of strings
    # i.e. [ "path", "to", "container" ]
    req_body = {}
    req_body['from_container'] = from_container
    req_body['move_from'] = move_from
    req_body['to_container'] = to_container
    req_body['move_to'] = move_to
    json_body = json.dumps(req_body)
    return self.post('move', json_body, 'application/json')

  def move_container(self, from_container, move_from, to_container, move_to):
    # from_container and to_container should be provided as an array of strings
    # i.e. [ "path", "to" ] and the actual container name should be provided in
    # the fields move_from and move_to, i.e. the container being moved should
    # not appear in from_container or to_container
    req_body = {}
    req_body['from_container'] = from_container
    req_body['move_from'] = move_from
    req_body['to_container'] = to_container
    req_body['move_to'] = move_to
    json_body = json.dumps(req_body)
    return self.post('move?container=true', json_body, 'application/json')

  def rename_obj(self, container_path, rename_from, rename_to):
    # container_path should be provided as an array of strings
    # i.e. [ "path", "to", "container" ]
    req_body = {}
    req_body['container_path'] = container_path
    req_body['rename_from'] = rename_from
    req_body['rename_to'] = rename_to
    json_body = json.dumps(req_body)
    return self.post('rename', json_body, 'application/json')

  def rename_container(self, container_path, rename_from, rename_to):
    # container_path should be provided as an array of strings
    # i.e. [ "path", "to" ] and the actual container name should be provided in
    # the fields rename_from and rename_to, i.e. the container being moved should
    # not appear in container_path
    req_body = {}
    req_body['container_path'] = container_path
    req_body['rename_from'] = rename_from
    req_body['rename_to'] = rename_to
    json_body = json.dumps(req_body)
    return self.post('rename?container=true', json_body, 'application/json')

  # public methods by HTTP verb
  # class methods must have 'self' in the signature but not explicitly
  # included when called (included implicitly)
  def get(self, path):
    return self.request("get", path, None, None)

  def head(self, path):
    return self.request("head", path, None, None)

  def post(self, path, data, content_type):
    return self.request("post", path, data, content_type)

  def put(self, path, data, content_type):
    return self.request("put", path, data, content_type)

  def delete(self, path):
    return self.request("delete", path, None, None)

  def get_headers(self, content_type=None):
    headers = {}
    headers["Content-Type"] = content_type
    headers["x-api-key"] = self.api_key
    return headers

  def request(self, type, path, data=None, content_type=None):
    headers = self.get_headers(content_type)
    url = self.endpoint + self.user_guid + "/" + path
    print("kvpbase request %s %s" % (type, url))

    if type is "get":
      resp = requests.get(url, headers=headers)
    if type is "head":
      resp = requests.head(url, headers=headers)
    if type is "post":
      resp = requests.post(url, data=data, headers=headers)
    if type is "put":
      resp = requests.put(url, data=data, headers=headers)
    if type is "delete":
      resp = requests.delete(url, headers=headers)

    return response(resp)
