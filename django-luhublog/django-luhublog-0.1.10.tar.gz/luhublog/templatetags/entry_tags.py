# -*- coding: utf-8 -*-

from django import template

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

register = template.Library()

class EntrySeoTag(InclusionTag):
	name = "entry_meta_seo"
	template = "luhublog/__seo_entry_meta.html"

	def get_context(self, context):
		entry = context.get('entry', None)
		if entry:
			try:
				meta = entry.entryseo
			except Exception, e:
				return ""
			else:
				return { 'meta' : meta, 'entry' : entry }
		return ""

register.tag(EntrySeoTag)