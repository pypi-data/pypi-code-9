# -*- coding: utf-8 -*-
from pypiwik.tracker import PiwikTracker

ON_SUCCESS = 1
ON_ERROR = 2
ALWAYS = 3

def track_page_view(tracker=None, piwik_url=None, site_id=None, when=ON_SUCCESS, **tracker_kwargs):
	if not ((piwik_url and site_id) or tracker):
		raise ValueError("Either 'tracker' or 'piwik_url' and 'site_id' must be set")

	def decorator_wrapper(func):
		def inner(*args, **kwargs):
			pt = tracker or PiwikTracker(piwik_url, site_id, **tracker_kwargs)

			try:
				ret = func(*args, **kwargs)

				if when in (ON_SUCCESS, ALWAYS):
					pt.track_page_view(**kwargs)

				return ret
			except:
				if when in (ON_ERROR, ALWAYS):
					pt.track_page_view(**kwargs)
				raise
		return inner
	return decorator_wrapper
