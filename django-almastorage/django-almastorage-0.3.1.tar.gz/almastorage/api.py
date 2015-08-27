from tastypie import fields, http
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.serializers import Serializer
from .models import SwiftContainer, SwiftFile
from django.conf.urls import url
from tastypie.utils import trailing_slash
import datetime
import base64
import simplejson as json
import swiftclient

class SwiftContainerResource(ModelResource):

	class Meta:
		queryset = SwiftContainer.objects.all()
		resource_name = 'storage'
		detail_allowed_methods = ['get', 'post']

	def prepend_urls(self):
		return [
			url(
				r"^(?P<resource_name>%s)/(?P<slug>\w+)/upload%s$" %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('upload'),
				name='api_upload'
			),
		]

	def upload(self, request, **kwargs):
		data = self.deserialize(
			request, request.body,
			format=request.META.get('CONTENT_TYPE', 'application/json'))
		file_contents = base64.b64decode(data['uploaded_file'])
		filename = data['filename']
		content_type = data['content_type']
		author = request.user if not request.user.is_anonymous() else None

		try:
			swiftfile = SwiftFile.upload_file(file_contents=file_contents, filename=filename, 
											content_type=content_type, author=author)
		except swiftclient.ClientException:
			return http.HttpUnauthorized("You are not authorized in stackswift service, \
				please, make sure that you add your username and key to your settings")

		bundle = SwiftFileResource().build_bundle(obj=swiftfile, request=request)
		bundle = SwiftFileResource().full_dehydrate(bundle)
		
		return self.create_response(
			request, {
				'file': bundle
			},
			response_class=http.HttpAccepted)


class SwiftFileResource(ModelResource):

	class Meta:
		queryset = SwiftFile.objects.all()
		resource_name = 'files'
		detail_allowed_methods = ['get', 'post']

	def prepend_urls(self):
		return [
			url(
				r"^(?P<resource_name>%s)/(?P<id>\d+)/download%s$" %
				(self._meta.resource_name, trailing_slash()),
				self.wrap_view('download'),
				name='api_download'
			),
		]

	def download(self, request, **kwargs):
		swiftfile = SwiftFile.objects.get(pk=kwargs.get('id'))
		try:
			temp_url =swiftfile.get_temp_download_url()
		except swiftclient.ClientException:
			return http.HttpUnauthorized("You are not authorized in stackswift service, \
				please, make sure that you add your username and key to your settings")
		return self.create_response(
			request, {
				'temp_url': temp_url
			},
			response_class=http.HttpAccepted)