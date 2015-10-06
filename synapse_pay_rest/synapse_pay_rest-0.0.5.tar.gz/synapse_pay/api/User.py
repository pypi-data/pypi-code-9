from HelperFunctions import *

USER_PATH = '/users'

class UserResources():

	def __init__(self, client):
		self.client = client

	def create_user_path(user_id=None):
		if self.client.user_id and not user_id:
			return USER_PATH + '/{0}'.format(self.client.user_id)
		elif user_id and not self.client.user_id:
			return USER_PATH + '/{0}'.format(user_id)
		elif user_id and self.client.user_id:
			return USER_PATH + '/{0}'.format(user_id)
		else:
			return USER_PATH

	'''
		Creates a SynapsePay user and updates the client with the new oauth key.

		:api add_doc		http://api.synapsepay.com/docs/attach-document

		:param user_id		The id of the user to add SSN info to.
		:param options		The body of the API response.

		:return response 	The JSON response
	'''
	def create(self, **kwargs):
		create_keys = ['payload']
		ok, error = HelperFunctions.checkKwargs(create_keys, kwargs)
		if ok:
			path = self.create_user_path()
			response = self.client.post(path, payload)
			if response.has_key('_id'):
				self.client.set_user_id(response['_id'])
		else:
			response = error
		return HelperFunctions.analyze_response(response)

	def get(self, **kwargs):
		path = self.create_user_path(kwargs.get('user_id'))
		params={}
		if 'query' in kwargs:
			params['query'] = kwargs.get('query')
		if 'page' in kwargs:
			params['page'] = kwargs.get('page')
		if 'page_count' in kwargs:
			params['per_page'] = kwargs.get('per_page')
		response = self.client.get(path, params)
		if response.has_key('_id'):
			self.client.set_user_id(response['_id'])
		return HelperFunctions.analyze_response(response)

	def update(self, **kwargs):
		update_keys = ['payload']
		ok, error = HelperFunctions.checkKwargs(update_keys, kwargs)
		if ok:
			path = self.create_user_path()
			response = self.client.patch(path, kwargs.get('payload'))
		else:
			response = error
		return HelperFunctions.analyze_response(response)

	def refresh(self, **kwargs):
		refresh_keys = ['payload']
		ok, error = HelperFunctions.checkKwargs(refresh_keys, kwargs)
		if ok:
			path = '/oauth/{0}'.format(self.client.user_id)
			response = self.client.post(path, kwargs.get('payload'))
		else:
			response = error
		return HelperFunctions.analyze_response(response)

	'''
		Adds the SSN information for the specific user. See
		http://api.synapsepay.com/docs/attach-document for more
		detailed explanation of this api and more example payloads.

		:param user_id	The id of the user to add SSN info to.
		:param options	The body of the API response.

		:return response 	The JSON response
	'''
	def add_doc(self, **kwargs):
		update_keys = ['payload']
		ok, error = HelperFunctions.checkKwargs(update_keys, kwargs)
		if ok:
			path = self.create_user_path()
			response = self.client.patch(path, kwargs.get('payload'))
		else:
			response = error
		return HelperFunctions.analyze_response(response)

	def verifY(self, **kwargs):
		update_keys = ['payload']
		ok, error = HelperFunctions.checkKwargs(update_keys, kwargs)
		if ok:
			path = self.create_user_path()
			response = self.client.patch(path, kwargs.get('payload'))
		else:
			response = error
		return HelperFunctions.analyze_response(response)

	'''
		Uploads a file for the user to help verify their identity. Can be an image, pdf, etc.
		See 
	'''
	def attach_file(self, file):
		base64_image = HelperFunctions.convert_file_to_base64(file)
		payload = {
			'doc': {
				'attachment':base64_image
			}
		}
		response = self.client.patch(USER_PATH + '/{0}'.format(str(self.client.user_id)), payload)
		return HelperFunctions.analyze_response(response)


	'''
		Adds the SSN information for the specific user. See
		http://api.synapsepay.com/docs/attach-document for more
		detailed explanation of this api and more example payloads.

		:param user_id	The id of the user to add SSN info to.
		:param options	The body of the API response.

		:return response 	The JSON response
	'''
	def answer_kba(self, payload):
		response = self.client.patch(USER_PATH + '/{0}'.format(str(self.client.user_id)), payload)
