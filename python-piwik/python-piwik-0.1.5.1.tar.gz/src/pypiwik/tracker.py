# -*- coding: utf-8 -*-
from hashlib import md5
import json
import logging
import os
import time
import datetime
import requests

try:
	from urllib.parse import urljoin, urlencode
except ImportError:
	from urlparse import urljoin
	from urllib import urlencode

PARAMETERS = {
	# required parameters
	'url': 'url', # The full URL for the current action.

	# recommended parameters
	'action_name': 'action_name', # The title of the action being tracked.
	'referer': 'urlref', # The full HTTP Referrer URL.
	'visit_custom_vars': '_cvar', # Visit scope custom variables.
	'visit_count': '_idvc', # The current count of visits for this visitor.
	'view_timestamp': '_viewts', # The UNIX timestamp of this visitor's previous visit.
	'first_visit_timestamp': '_idts', # The UNIX timestamp of this visitor's first visit.
	'campaign_name': '_rcn', # The Campaign name (see Tracking Campaigns).
	'campaign_keywords': '_rck', # The Campaign Keyword (see Tracking Campaigns).
	'resolution': 'res', # The resolution of the device the visitor is using, eg 1280x1024.
	'hour': 'h', # The current hour (local time).
	'minute': 'm', # The current minute (local time).
	'second': 's', # The current second (local time).
	'flash': 'fla', # Flash,
	'java': 'java', # Java
	'director': 'dir', # Director,
	'quicktime': 'qt', # Quicktime,
	'real_player': 'realp', # Real Player,
	'pdf': 'pdf', # PDF
	'wma': 'wma', # Windows Media
	'gears': 'gears', # Gears
	'silverlight': 'ag', # Silverlight
	'cookie': 'cookie', # when set to 1, the visitor's client is known to support cookies.
	'user_agent': 'ua', # An override value for the User-Agent HTTP header field.
	'lang': 'lang', # An override value for the Accept-Language HTTP header field. This value is used to detect the visitor's country if GeoIP is not enabled.
	'user_id': 'uid', # defines the User ID for this request. User ID is any non empty unique string identifying the user (such as an email address or a username).
	'visitor_id': 'cid', # defines the visitor ID for this request.
	'new_visit': 'new_visit', # If set to 1, will force a new visit to be created for this action. This feature is also available in Javascript.

	# 'Optional Action info (measure Page view, Outlink, Download, Site search)',
	'page_custom_vars': 'cvar', # Page scope custom variables.
	'link': 'link', # An external URL the user has opened. Used for tracking outlink clicks. We recommend to also set the url parameter to this same value.
	'download': 'download', # URL of a file the user has downloaded. Used for tracking downloads. We recommend to also set the url parameter to this same value.
	'search_keyword': 'search', # The Site Search keyword. When specified, the request will not be tracked as a normal pageview but will instead be tracked as a Site Search request.
	'search_category': 'search_cat', # when search is specified, you can optionally specify a search category with this parameter.
	'search_count': 'search_count', # when search is specified, we also recommend to set the search_count to the number of search results displayed on the results page.

	'goal_id': 'idgoal', # If specified, the tracking request will trigger a conversion for the goal of the website being tracked with this ID.
	'revenue': 'revenue', # A monetary value that was generated as revenue by this goal conversion. Only used if idgoal is specified in the request.
	'gt_ms': 'gt_ms', # The amount of time it took the server to generate this action, in milliseconds.
	'charset': 'cs', # The charset of the page being tracked. Specify the charset if the data you send to Piwik is encoded in a different character set than the default utf-8.

	# Optional Event Tracking info
	'event_category': 'e_c', # The event category. Must not be empty. (eg. Videos, Music, Games...)
	'event_action': 'e_a', # The event action. Must not be empty. (eg. Play, Pause, Duration, Add Playlist, Downloaded, Clicked...)
	'event_name': 'e_n', # The event name. (eg. a Movie name, or Song name, or File name...)
	'event_value': 'e_v', # The event value. Must be a float or integer value (numeric), not a string.

	# Optional Content Tracking info
	'content_name': 'c_n', # The name of the content. For instance 'Ad Foo Bar'
	'content_piece': 'c_p', # The actual content piece. For instance the path to an image, video, audio, any text
	'content_target': 'c_t', # The target of the content. For instance the URL of a landing page
	'content_interaction': 'c_i', # The name of the interaction with the content. For instance a 'click'

	# Other parameters (require authentication via token_auth)
	'token_auth': 'token_auth', # 32 character authorization key used to authenticate the API request.
	'client_ip': 'cip', # Override value for the visitor IP (both IPv4 and IPv6 notations supported).
	'client_dt': 'cdt', # Override for the datetime of the request (normally the current time is used).
	'country': 'country', # An override value for the country. Should be set to the two letter country code of the visitor (lowercase), eg fr, de, us.
	'region': 'region', # An override value for the region. Should be set to the two letter region code as defined by MaxMind's GeoIP databases.
	'city': 'city', # An override value for the city. The name of the city the visitor is located in, eg, Tokyo.
	'lat': 'lat', # An override value for the visitor's latitude, eg 22.456.
	'long': 'long', # An override value for the visitor's longitude, eg 22.456.

	'track_bots': 'bots', # Set to true to track bots

	'heartbeat_timer': None, # Set to a positive integer to enable the heartbeat timer
}

AUTH_RESTRICTED_PARAMS = ('token_auth', 'client_ip', 'client_dt', 'country', 'region', 'city', 'lat', 'long')

class PiwikTracker(object):
	API_VERSION = 1

	def __init__(self, piwik_url, site_id, request=None, values=None, **kwargs):
		super(PiwikTracker, self).__init__()
		self.piwik_url = piwik_url
		self.idsite = site_id

		# initialize all tracking variables on this instance
		values = values or {}
		values.update(kwargs)
		self.update(dict((p, values.get(p, None)) for p in PARAMETERS.keys()))

		self.visit_custom_vars = {}
		self.page_custom_vars = {}

		self.spoof_request = True

		# defaults for the requests module
		self.request_headers = {}
		self.requests_arguments = {
			'timeout': 3
		}

		# default filenames for the tracker file and the js file
		self.piwik_php_file = 'piwik.php'
		self.piwik_js_file = 'piwik.js'

		self.update_from_request(request)

	def update(self, values):
		for property_name in PARAMETERS.keys():
			if property_name in values:
				setattr(self, property_name, values[property_name])

	@property
	def php_url(self):
		return urljoin(self.piwik_url, self.piwik_php_file)

	@property
	def js_url(self):
		return urljoin(self.piwik_url, self.piwik_js_file)

	def update_from_request(self, request):
		"""
		Initializes the current tracker instance from a Django-like requests object.
		If the request argument is None or does not have a dict as the META attribute, this function does nothing.
		"""
		if not request:
			return

		meta = getattr(request, 'META', {})

		if not isinstance(meta, dict):
			return

		self.user_agent = meta.get('HTTP_USER_AGENT', None)
		self.referer = meta.get('HTTP_REFERER', None)
		self.lang = meta.get('HTTP_ACCEPT_LANGUAGE', None)

		if hasattr(request, 'build_absolute_uri'):
			bau = request.build_absolute_uri
			if callable(bau):
				self.url = bau()

		def _get_client_ip():
			if 'HTTP_X_FORWARDED_FOR' in meta:
				return meta['HTTP_X_FORWARDED_FOR'].split(",")[0]
			else:
				return meta.get('REMOTE_ADDR', None)

		self.client_ip = _get_client_ip()

	def _build_cvars(self, value):
		"""
		Converts a custom vars dictionary to it's JSON representation usable for the Piwik API.
		"""
		if not value:
			return None

		d = {}

		for i, item in enumerate(value.items(), start=1):
			d[i] = list(item)

		return json.dumps(d)

	def _build_parameters(self, **kwargs):
		d = {
			'idsite': self.idsite,
			'rec': '1',
			'apiv': PiwikTracker.API_VERSION,
		}

		for property_name, parameter_name in PARAMETERS.items():
			if not parameter_name:
				continue

			value = kwargs.get(property_name, None) or getattr(self, property_name, None)

			token_auth = kwargs.get('token_auth', None) or getattr(self, 'token_auth', None)
			if value and property_name in AUTH_RESTRICTED_PARAMS and not token_auth:
				logging.info("Skipping %s because token_auth not set" % property_name)
				continue

			if value is None:
				continue

			if isinstance(value, bool):
				value = 1 if value else 0
			elif isinstance(value, datetime.datetime):
				if not value.tzinfo:
					logging.warning("Passing a naive datetime may result in wrong data. Make sure you pass a datetime object with UTC timezone")
				value = value.strftime('%Y-%m-%d %H:%M:%S')

			if property_name in ('page_custom_vars', 'visit_custom_vars'):
				value = self._build_cvars(value)
				if not value:
					continue

			d[parameter_name] = value

		return d

	def build_request_headers(self, params):
		headers = {
			'Accept': '*/*',
			'Accept-Encoding': 'gzip, deflate',
		}
		headers.update(self.request_headers)

		if self.spoof_request:
			# this is only used for server-to-server calls. By putting the values into the HTTP headers
			# and dropping them from the payload we will transfer less to the server while carrying the same information.
			for p, h in (('ua', 'User-Agent'), ('lang', 'Accept-Language'), ('urlref', 'Referer')):
				if p in params:
					headers[h] = params[p]
					del params[p]

		return headers

	def track_page_view(self, **kwargs):
		params = self._build_parameters(**kwargs)
		if '_id' not in params:
			params['_id'] = md5(os.urandom(16)).hexdigest()[:15]
		if '_idts' not in params:
			params['_idts'] = int(time.time())

		headers = self.build_request_headers(params)
		logging.debug("Tracking variables: %s" % params)
		logging.debug("Tracking headers: %s" % headers)
		try:
			response = requests.post(self.php_url, data=params, headers=headers, **self.requests_arguments)
			logging.debug("Tracking response: %s" % response)
		except:
			logging.exception("Tracking request failed")

	def tracking_code(self, **kwargs):
		return TrackingCodeBuilder(self).render(self._build_parameters(**kwargs))


class TrackingCodeBuilder(object):
	template = """<script type="text/javascript">
  var _paq = _paq || [];
{custom_vars}
{event_tracking}
{js_vars}
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {{
    _paq.push(['setTrackerUrl', '{tracker_url}']);
    _paq.push(['setSiteId', {idsite}]);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.defer=true; g.src='{javascript_url}'; s.parentNode.insertBefore(g,s);
  }})();
</script>
<noscript><p><img src="{tracker_url}?{tracking_args}" style="border:0;" alt="" /></p></noscript>"""

	def __init__(self, tracker):
		self.tracker = tracker

	def _paq_push(self, l):
		# python3's filter() does not return a list
		return "_paq.push(%s);" % json.dumps(list(l))

	def _event_tracker(self):
		if not (self.tracker.event_category and self.tracker.event_action):
			return ""
		l = ['trackEvent', self.tracker.event_category, self.tracker.event_action, self.tracker.event_name, self.tracker.event_value]
		return self._paq_push(filter(lambda x: x, l))

	def _custom_vars(self):
		def _inner():
			for d, scope in (self.tracker.page_custom_vars, 'page'), (self.tracker.visit_custom_vars, 'visit'):
				for i, item in enumerate(d.items(), start=1):
					if i > 5:
						break
					k, v = item
					l = ['setCustomVariable', i, k, v, scope]
					yield self._paq_push(l)
		return '\n'.join(_inner())

	def _common_vars(self, params):
		def _inner():
			extra_tracking_params = {}
			if 'url' in params:
				yield self._paq_push(['setCustomUrl', params['url']])
			if 'urlref' in params:
				yield self._paq_push(['setReferrerUrl', params['urlref']])
			if 'action_name' in params:
				yield self._paq_push(['setDocumentTitle', params['action_name']])
			if 'new_visit' in params and params['new_visit']: # http://piwik.org/faq/how-to/#faq_187
				extra_tracking_params['new_visit'] = 1
				yield self._paq_push(["deleteCookies"])
			if self.tracker.heartbeat_timer and int(self.tracker.heartbeat_timer) > 0:
				yield self._paq_push(['enableHeartBeatTimer', self.tracker.heartbeat_timer])
			if 'bots' in params and params['bots']:
				extra_tracking_params['bots'] = 1

			if extra_tracking_params:
				yield self._paq_push(['appendToTrackingUrl', urlencode(extra_tracking_params)])

		return '\n'.join(_inner())

	def render(self, params):
		# remove all tracking variables which doesn't do any good when used with the image or javascript
		# tracking api
		for x in ['url', 'ua', 'lang'] + [PARAMETERS[x] for x in AUTH_RESTRICTED_PARAMS]:
			if x in params:
				del params[x]

		return TrackingCodeBuilder.template.format(tracker_url=self.tracker.php_url,
							javascript_url=self.tracker.js_url,
							idsite=self.tracker.idsite,
							tracking_args=urlencode(params),
							event_tracking=self._event_tracker(),
							custom_vars=self._custom_vars(),
							js_vars=self._common_vars(params),
				)
