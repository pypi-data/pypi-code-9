import requests
import json


class SmsOwl:
	url = 'https://api.smsowl.in/v1/sms';

	def __init__(self, accountId, apiKey):
		self.accountId = accountId
		self.apiKey = apiKey


	def sendPromotionalSms(self,senderId,to,message,smsType='normal'):
		payload = {
		    "accountId": self.accountId,
		    "apiKey": self.apiKey,
		    "dndType": "promotional",
		    "smsType": smsType,
		    "senderId": senderId,
		    "to": to,
		    "message": message
		}
		headers = {'Content-type': 'application/json'}
		r = requests.post(SmsOwl.url, data=json.dumps(payload), headers=headers)

		if r.status_code == 200:
			json_data = json.loads(r.text)
			if isinstance(to,list):
				return json_data['smsIds']
			else:
				return json_data['smsId']
		else:
			json_error = json.loads(r.text)
			raise ValueError(json_error['message'])


	def sendTransactionalSms(self,senderId,to,templateId,placeholderDict):
		payload = {
		    "accountId": self.accountId,
		    "apiKey": self.apiKey,
		    "dndType": "transactional",
		    "smsType": 'normal',
		    "senderId": senderId,
		    "to": to,
		    "templateId": templateId,
		    "placeholders": placeholderDict
		}
		headers = {'Content-type': 'application/json'}
		r = requests.post(SmsOwl.url, data=json.dumps(payload),headers=headers)

		if r.status_code == 200:
			json_data = json.loads(r.text)
			return json_data['smsId']
		else:
			json_error = json.loads(r.text)
			raise ValueError(json_error['message'])