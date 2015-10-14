from django import template

from slugify import slugify

register = template.Library()

def slugify_link(value):
	"""slugify string value"""
	return slugify(value.lower())

register.filter('slugify_link', slugify_link)