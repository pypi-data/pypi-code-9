from django.test import TestCase
from tastypie.test import ResourceTestCase
from django.db import models
from django.contrib.auth.models import User
import swiftclient
from datetime import datetime
from django.conf import settings
from .models import SwiftContainer, SwiftFile, DEFAULT_CONTAINER_TITLE
import os

USERNAME = settings.SW_USERNAME
KEY = settings.SW_KEY
AUTH_URL = settings.SW_AUTH_URL

class SwiftContainerTestCase(TestCase):
	def setUp(self):
		super(self.__class__, self).setUp()

	def test_create_default_container(self):
		container = SwiftContainer.create_default_container()
		self.assertEqual(container.title, DEFAULT_CONTAINER_TITLE)
		self.assertEqual(container.service_slug, USERNAME)
		try:
			conn = swiftclient.Connection(user=USERNAME, key=KEY, authurl=AUTH_URL)
			_m, objects = conn.get_container(container.title)
			self.assertEqual(len(objects), 0)
		except swiftclient.ClientException:
			raise Exception("Access denied")
		else:
			container.delete()
			self.assertEqual(SwiftContainer.objects.all().count(), 0)

class SwiftFileTestCase(TestCase):
	def setUp(self):
		super(self.__class__, self).setUp()

	def test_upload(self):
		file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
								 'almastorage/__init__.py')
		from mimetypes import MimeTypes
		mime = MimeTypes()
		mime_type = mime.guess_type(file_path)
		f = open(file_path, "rb")

		swf = SwiftFile.upload_file(file_contents=f.read(), filename='__init__.py', content_type=mime_type)

		self.assertEqual(SwiftContainer.objects.all().count(), 1)
		self.assertEqual(SwiftContainer.objects.first().title, DEFAULT_CONTAINER_TITLE)

		try:
			conn = swiftclient.Connection(user=USERNAME, key=KEY, authurl=AUTH_URL)
			_m, objects = conn.get_container(DEFAULT_CONTAINER_TITLE)
			self.assertEqual(len(objects), 1)
		except swiftclient.ClientException:
			raise Exception("Access denied")
		else:
			SwiftContainer.objects.first().delete()
			self.assertEqual(SwiftContainer.objects.all().count(), 0)
			self.assertEqual(SwiftFile.objects.all().count(), 0)

	def test_temp_url(self):
		file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
								 'almastorage/__init__.py')
		from mimetypes import MimeTypes
		mime = MimeTypes()
		mime_type = mime.guess_type(file_path)
		f = open(file_path, "rb")

		swf = SwiftFile.upload_file(file_contents=f.read(), filename='__init__.py', content_type=mime_type)

		url = swf.get_temp_download_url()
		swf.delete()

		try:
			conn = swiftclient.Connection(user=USERNAME, key=KEY, authurl=AUTH_URL)
			_m, objects = conn.get_container(DEFAULT_CONTAINER_TITLE)
			self.assertEqual(len(objects), 0)
		except swiftclient.ClientException:
			raise Exception("Access denied")
		else:
			SwiftContainer.objects.first().delete()
			self.assertEqual(SwiftContainer.objects.all().count(), 0)

class AlmastorageResourceTest(ResourceTestCase):

	def setUp(self):
		super(self.__class__, self).setUp()

		self.api_path_container= '/api/v1/storage/'

		self.api_path_files = '/api/v1/files/'

		self.get_resp_files = lambda path: self.api_client.get(
			self.api_path_files + path,
			format='json',
			HTTP_HOST='localhost')
		self.get_des_res_files = lambda path: self.deserialize(self.get_resp_files(path))


		self.get_resp = lambda path: self.api_client.get(
			self.api_path_container + path,
			format='json',
			HTTP_HOST='localhost')
		self.get_des_res = lambda path: self.deserialize(self.get_resp(path))

	def test_upload_and_download(self):
		container = SwiftContainer.create_default_container()
		self.assertEqual(container.title, DEFAULT_CONTAINER_TITLE)
		self.assertEqual(container.service_slug, USERNAME)
		try:
			conn = swiftclient.Connection(user=USERNAME, key=KEY, authurl=AUTH_URL)
			_m, objects = conn.get_container(container.title)
			# self.assertEqual(len(objects), 0)
		except swiftclient.ClientException:
			raise Exception("Access denied")
		else:
			file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
								 'almastorage/models.py')
			from mimetypes import MimeTypes
			mime = MimeTypes()
			mime_type = mime.guess_type(file_path)
			f = open(file_path, "rb")
			filename='models.py'

			import base64
			post_data={
				'filename': filename,
				'content_type': mime_type,
				'uploaded_file': base64.b64encode(open(file_path, "rb").read())
				}

			resp = self.api_client.post(
				self.api_path_container+"%s/upload/"%container.service_slug, format='json', data=post_data)
			des_resp = self.deserialize(resp)

			conn = swiftclient.Connection(user=USERNAME, key=KEY, authurl=AUTH_URL)
			_m, objects = conn.get_container(DEFAULT_CONTAINER_TITLE)
			# self.assertEqual(len(objects), 1)
			resp = self.api_client.get(self.api_path_files+str(des_resp['file']['id'])+'/download/',
										format='json')
			des_resp = self.deserialize(resp)

			import requests
			r = requests.get(des_resp['temp_url'], stream=True)
			context = ""
			for chunk in r.iter_content():
				context += chunk
			self.assertTrue(len(context) != 0)
			container.delete()
			self.assertEqual(SwiftContainer.objects.all().count(), 0)