import os

import threading
api = threading.local()

class Response(object):
	def __init__(self, code = 200, headers = {}, body = None):
		self.code = code
		self.headers = headers
		self.body = body
