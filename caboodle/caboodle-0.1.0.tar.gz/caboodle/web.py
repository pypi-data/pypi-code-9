from selenium import webdriver

class Browser(object):
	"""
	The browser class is the core of the web module and is what creates
	the window to interact with.

	Args:
		type (str): The type of browser
	"""

	def __init__(self, type):
		self.driver = getattr(webdriver, type)()

	def __getattr__(self, attr):
		return self.driver.__getattribute__(attr)
