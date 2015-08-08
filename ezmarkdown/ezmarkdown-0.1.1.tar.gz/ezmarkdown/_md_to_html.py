## -*- coding: utf-8 -*-

import markdown as md


def preprocessing(s):
    """
    Returns string where \\ is replaced by \\\ so that latex new lines work
    """
    return  s.replace(r'\\', r'\\\\')


def md_to_html(text_md):
	"""
	Returns HTML string
	The input string should be of the raw 'r' type
	"""
	return md.markdown(preprocessing(text_md).decode('utf-8'), extensions=['markdown.extensions.tables'])

