# -*- coding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentType

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

from luhublog.models import TwitterCard


register = template.Library()

class TwitterCardTag(InclusionTag):
	name = "twitter_card"
	template = "luhublog/__twitter_card.html"

	def get_context(self, context):
		object = context.get('object', None)
		if object:
			try:
				content_type = ContentType.objects.get_for_model(object)
			except Exception, e:
				return ""
			else:

				try:
					twitter_card = TwitterCard.objects.get(content_type=content_type, object_id=object.id)
				except Exception, e:
					return ""
				else:
					return { 'twitter' : twitter_card }
		return ""

register.tag(TwitterCardTag)