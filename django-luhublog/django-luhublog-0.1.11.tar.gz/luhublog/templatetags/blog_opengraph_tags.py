# -*- coding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

from luhublog.models import OpenGraph


register = template.Library()

class OpenGraphTag(InclusionTag):
	name = "open_graph_tags"
	template = "luhublog/__open_graph_tags.html"

	def get_context(self, context):
		object = context.get('object', None)
		if object:
			try:
				content_type = ContentType.objects.get_for_model(object)
			except Exception, e:
				return ""
			else:

				try:
					opengraph = OpenGraph.objects.get(content_type=content_type, object_id=object.id)
				except Exception, e:
					return ""
				else:
					return { 'opengraph' : opengraph, 'entry' : object }
		return ""

register.tag(OpenGraphTag)