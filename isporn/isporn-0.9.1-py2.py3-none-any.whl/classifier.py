# -*- coding: utf-8 -*-
"""
  The Exadeep classifier
    The purpose of this module is to send requests to exadeep.com to
    classify the pictures vice REST api
"""

import requests
import os
import io
from PIL import Image
import json


class ExadeepClassifier():
  """
    The base service accessing for exadeep
  """
  MODEL_NAME = "model_name"
  API_KEY_NAME = "api_key"
  IMG_NAME = "images[]"
  IMG_URL = "urls[]"
  IMG_WIDTH = 270
  IMG_HEIGHT = 270

  def __init__(self, server, api_key, model_name = None, is_resize = False):
    """
      Args:
        server: the server's REST api address
        model_name: the name of the service to use
    """
    self._server = server
    self._model_name = model_name
    self._api_key = api_key
    self._images = []
    self._image_urls = []
    self._is_resize = is_resize
    self._response = None
    self._res_json = None

  def _resize_img(self, stream):
    if self._is_resize:
      img = Image.open(stream)
      ios = io.BytesIO()
      n_img = img.resize((self.IMG_WIDTH, self.IMG_HEIGHT))
      n_img.save(ios, format='jpeg')
      ios.seek(0)
      return ios
    return stream

  def add_image(self, path, name=None):
    """
      Add image to this classification request
      Args:
        name: the name of this image which the server sees
        path: the path of this image. It can be url, local file and streamio
      Returns:
        (True/False, msg)
    """
    if name is None:
      name = os.path.basename(path)
    if os.path.isfile(path):
      self._images.append((self.IMG_NAME, (name, 
        self._resize_img(open(path, 'rb')))))
      return (True, "succ")
    elif hasattr(path, 'read'):
      self._images.append((self.IMG_NAME, (name, self._resize_img(path))))
    elif self._is_valid_url(path):
      self._image_urls.append(path)
    else:
      return (False, "No file found")

  def _is_valid_url(self, value):
    return value.lower().startswith("http") or value.lower().startswith("https")

  def _parse_res(self):
    if self._res_json is None and self._response is not None:
      self._res_json = json.loads(self._response.content)

  def add_images(self, images):
    """
      add images to this request to classify
      Args:
        images: a list of image path/url/streamio
      Returns:
        (True/False, msg)
    """
    for image in images:
      if not os.path.isfile(image) and not self._is_valid_url(image):
        return (False, "File " + image + " not found")

    for image in images:
      self.add_image(image)

    return (True, "succ")

  def add(self, images):
    if isinstance(images, (list, tuple)):
      return self.add_images(images)
    else:
      return self.add_image(images)

  def reset(self):
    """
      Reset the current classifier's states to allow new request
    """
    self._images = []
    self._image_urls = []
    self._response = None
    self._res_json = None
    return True

  def http_code(self):
    """
      Returns:
        the status code(string) of http/s request
    """
    if self._response.status_code is not None:
      return str(self._response.status_code)
    else:
      return "error"

  def rest_status(self):
    """
      Returns:
        the status code of rest request
    """
    if self.http_code() == "200":
      self._parse_res()
      if self._res_json is not None:
        if self._res_json.has_key('status'):
          return str(self._res_json['status'])
        else:
          return "error"
      else:
        return "error"
    else:
      return "error"

  def response(self,):
    return self._response
  
  def classify(self, ovars=None):
    """
      Classify the images
      Args:
        ovars: other variables passed with request
      Returns:
        The result is in json format
    """
    data={}
    if ovars is not None:
      data.update(ovars)
    if self._model_name is not None:
    	data[self.MODEL_NAME] = self._model_name
    data[self.API_KEY_NAME] = self._api_key
    if len(self._image_urls) > 0:
      data[self.IMG_URL] = self._image_urls
    if len(self._images) > 0:
      self._response = requests.post(self._server, 
        files=self._images, 
        data=data
        )
    else:
      self._response = requests.post(self._server, data=data)

    return self._response


class PornClassifier(ExadeepClassifier):

  def __init__(self, server="https://exadeep.com/api/v1", 
                 api_key="exadeep_ruby_demo_key"):
    ExadeepClassifier.__init__(self, server, api_key, is_resize = True )

  def isporn(self):
    """
      Returns:
        the types: a list of porn/normal/sexy or "error"
    """
    if self._response is None:
      self.classify()
    if self.rest_status() == "200":
      if self._res_json.has_key('results'):
        results = self._res_json['results']
        return [ scores['scores'][0]['label'] for scores in results ]
      else:
        return "error"
    else:
      return "error"

def isporn(target):
  """
    Classify an image or a list of images to be porn or not.
    Args:
      target: an image/url or a list of images/urls
    Returns:
      the result category of target image file or "error" string
  """
  cla = PornClassifier()
  cla.add(target)
  ret = cla.isporn()
  if isinstance(target, (list, tuple)):
    return ret
  else:
    if isinstance(ret, (list)):
      return ret[0]
    else:
      return ret
    

if __name__ == '__main__':
  cla = PornClassifier()
  cla.add_image('http://pic1.nipic.com/2008-09-08/200898163242920_2.jpg')
  cla.add_image('http://pic1.nipic.com/2008-09-08/200898163242920_2.jpg')
  cla.add_image('http://pic1.nipic.com/2008-09-08/200898163242920_2.jpg')
  cla.add_images(['http://pic1.nipic.com/2008-09-08/200898163242920_2.jpg',
    'http://pic1.nipic.com/2008-09-08/200898163242920_2.jpg'])
  print cla.isporn()
  if cla.isporn() == "error":
    print cla.http_code()
    print cla.rest_status()
    print cla.response().content

  if os.path.isfile('./porn1.jpg'):
    cla.reset()
    cla.add_image('./porn1.jpg')
    cla.add_images(['./porn1.jpg', './porn1.jpg'])
    print cla.isporn()
    if cla.isporn() == "error":
      print cla.http_code()
      print cla.rest_status()
      print cla.response().content
  


   
