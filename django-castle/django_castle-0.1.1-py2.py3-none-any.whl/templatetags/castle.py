import hashlib
import hmac
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from Crypto.Hash import HMAC, SHA256

register = template.Library()


@register.simple_tag
def castle_load(user=None, secure=False, track=False):
	user_id = str(user.id) if user else ""
	app_id = getattr(settings, "CASTLE_APP_ID", False)
	if not app_id:
		raise ImproperlyConfigured("Trying to include {% castle_track %} without settings.CASTLE_APP_ID")

	script = """
<script type="text/javascript">
	(function(e,t,n,r){function i(e,n){e=t.createElement("script");e.async=1;e.src=r;n=t.getElementsByTagName("script")[0];n.parentNode.insertBefore(e,n)}e[n]=e[n]||function(){(e[n].q=e[n].q||[]).push(arguments)};e.attachEvent?e.attachEvent("onload",i):e.addEventListener("load",i,false)})(window,document,"_castle","//d2t77mnxyo7adj.cloudfront.net/v1/c.js")
	_castle('setAppId', '%(app_id)s');""" % {"app_id": app_id}

	if user:
		script += \
			"""
	_castle('identify', '%(user_id)s', {
		created_at: '%(user_created_at)s',
		email: '%(user_email)s',
		name: '%(user_name)s'
	});""" % {
		"user_id": user.id,
		"user_email": user.email,
		"user_name": user.get_full_name(),
		"user_created_at": user.date_joined.isoformat()
		}

		if secure:
			api_secret = getattr(settings, "CASTLE_API_SECRET", False)
			if not api_secret:
				raise ImproperlyConfigured(
					"Trying to include {% castle_track secret=True %} without settings.CASTLE_API_SECRET")
			hash_obj = HMAC.new(key=api_secret, msg=str(user.id), digestmod=SHA256)
			signature = hash_obj.hexdigest()
			script += \
				"""
		_castle('secure', '%(signature)s');""" % {
					"signature": signature,
				}

	if track:
		script += """
	_castle('trackPageview');
"""

	script += """</script>"""
	return script
