from HelperFunctions import *

TRANS_PATH = '/users/{0}/nodes/{1}/trans/{2}'

class TransactionResources():

	def __init__(self, client):
		self.client = client

	def create_trans_path(self, user_id, node_id, trans_id=None):
		# print user_id, node_id
		if trans_id:
			return TRANS_PATH.format(user_id, node_id, trans_id)
		else:
			return TRANS_PATH.replace('/{2}','').format(user_id, node_id)

	def create(self, **kwargs):
		create_keys = ['node_id', 'payload']
		ok, error = HelperFunctions.checkKwargs(create_keys, kwargs)
		if ok:
			path = self.create_trans_path(kwargs.get('node_id'))
			response = self.client.post(path, kwargs.get('payload'))
		else:
			response = error
		return HelperFunctions.analyze_response(response)

	def get(self, **kwargs):
		get_keys = ['node_id']
		ok, error = HelperFunctions.checkKwargs(get_keys, kwargs)
		if ok:
			path = self.create_trans_path(kwargs.get('node_id'), kwargs.get('trans_id'))
			response = self.client.get(path)
		else:
			response = error
		return HelperFunctions.analyze_response(response)

	'''
		Updates a transaction by giving it a comment.

		:param user_id				The id of the user whose transaction is going to be deleted.
		:param node_id				The id of the node that initiated the transaction to be deleted.
		:param trans_id				The id the transaction to be deleted.
		:param transaction_object	The object returned when the transaction was created.

		:return response 	The JSON response
	'''
	def update(self, **kwargs):
		update_keys = ['payload', 'node_id', 'trans_id']
		ok, error = HelperFunctions.checkKwargs(update_keys, kwargs)
		if ok:
			path = self.create_trans_path(kwargs.get('node_id'), kwargs.get('trans_id'))
			response = self.client.patch(path, kwargs.get('payload'))
		else:
			response = error
		return HelperFunctions.analyze_response(response)


	'''
		Deletes a specific transaction. See http://api.synapsepay.com/docs/attach-document
		for more information.

		:param user_id				The id of the user whose transaction is going to be deleted.
		:param node_id				The id of the node that initiated the transaction to be deleted.
		:param trans_id				The id the transaction to be deleted.
		:param transaction_object	The object returned when the transaction was created.

		:return response 	The JSON response
	'''
	def delete(self, node_id, trans_id):
		delete_keys = ['node_id', 'trans_id']
		ok, error = HelperFunctions.checkKwargs(delete_keys, kwargs)
		if ok:
			path = self.create_transaction_path(self.client.user_id, node_id, trans_id)
			response = self.client.delete(path)
		else:
			response = error
		return HelperFunctions.analyze_response(response)