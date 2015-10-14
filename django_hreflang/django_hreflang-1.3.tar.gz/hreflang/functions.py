
"""
	Translate urls to new languages

	With inspiration from
		http://stackoverflow.com/a/17351858/723090
		https://djangosnippets.org/snippets/2875/
"""

from django.core.urlresolvers import reverse as lang_implied_reverse, NoReverseMatch
from django.utils import lru_cache
from django.utils.translation import activate, deactivate, get_language
from django.core.urlresolvers import resolve
from django.conf import settings


def reverse(*args, lang = None, use_lang_prefix = True, **kwargs):
	"""
		Similar to django.core.urlresolvers.reverse except for the extra parameter:

		@param lang: language code in which the url is to be translated (ignored if use_lang_prefix is False)
		@use_lang_prefix: is changed to False, get an url without language prefix

		If lang is not provided, the normal reverse behavious is obtained.
	"""
	#todo: use_lang_prefix implementation is a bit of a hack now until a better way is found: http://stackoverflow.com/questions/27680748/when-using-i18n-patterns-how-to-reverse-url-without-language-code
	if lang is None and use_lang_prefix:
		return lang_implied_reverse(*args, **kwargs)
	cur_language = get_language()
	if use_lang_prefix:
		activate(lang)
	else:
		deactivate()
	url = lang_implied_reverse(*args, **kwargs)
	if not use_lang_prefix:
		if not url.startswith('/{0}'.format(settings.LANGUAGE_CODE)):
			raise NoReverseMatch('could not find reverse match with use_lang')
		url = url[len(settings.LANGUAGE_CODE)+1:]
	activate(cur_language)
	return url


def get_hreflang_info(path, default = True):
	"""
		@param path: current path (request.path)
		@param default: include the default landing page (x-default without language code)
		:return: a list of (code, url) tuples for all language versions
	"""
	reverse_match = resolve(path)
	info = []
	if default:
		info.append(('x-default', reverse(reverse_match.view_name, use_lang_prefix = True, kwargs = reverse_match.kwargs)))
	for lang in language_codes():
		info.append((lang, reverse(reverse_match.view_name, lang = lang, use_lang_prefix = True, kwargs = reverse_match.kwargs)))
	return info


@lru_cache.lru_cache()
def languages():
	"""
		Get language and regionale codes and names of all languages that are supported as a dictionary.
	"""
	return {key: name for key,name in settings.LANGUAGES}


@lru_cache.lru_cache()
def language_codes():
	"""
		Get language with regionale codes of all languages that are supported.
	"""
	return languages().keys()


