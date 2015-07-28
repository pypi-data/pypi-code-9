from __future__ import unicode_literals
from django.conf import settings


def site(request):

	try:
		return {
			'site': request.site
		}
	except:
		return {
			'site': None
		}
	

def custom_settings(request):
	object = {}

	try:

		all_settings = settings.CUSTOM_SETTINGS	
		for setting in all_settings:
			if hasattr(request, setting):
			    value = getattr(request, setting)
			    object[setting] = value		    
	except:
	 	pass

	return object


def impersonating(request):
	object = {}

	return {
			'impersonating': request.impersonating
		}
