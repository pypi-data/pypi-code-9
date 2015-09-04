import json
from http.client import HTTPSConnection

from paytrail import common

class ConnectAPI:
    APINAME='PaytrailConnectAPI'

    def __init__(self, apiKey, secret, apiLocation='account.paytrail.com:443', connectionMethod=HTTPSConnection):
        self.apiLocation = apiLocation
        self.apiKey = apiKey
        self.connectionMethod = connectionMethod

        if type(secret) == str:
            self.secret = secret.encode('ascii')
        else:
            self.secret = secret

    def _dial(self, method, location, body):
        '''Make the authorization HTTP headers and call the API URL.

        Returns the standard HTTPResponse object.'''

        headers = common.makeHeaders(self.APINAME, common.makeTimestamp(), self.apiKey, self.secret, method, location, body)
        conn = self.connectionMethod(self.apiLocation)
        conn.request(method, location, body, headers)

        return conn.getresponse()

    def authorize(self, authKey, locale='fi_FI', location='/connectapi/authorizations',
        authType='email+smspin', access=['charge', 'deliveryAddress'], validity='singleCharge'):
        body = json.dumps({
            'authKey': authKey,
            'authType': authType,
            'access': access,
            'validity': validity,
            'locale': locale,
        })

        response = self._dial('POST', location, body)
        self.location = response.getheader('Location')

        return {'status': response.status, 'reason': response.reason}

    def confirmPin(self, authSecret):
        body = json.dumps({'authSecret': authSecret})
        location = self.location + '/confirmation'

        response = self._dial('POST', location, body)

        return {'status': response.status, 'reason': response.reason}

    def getAddresses(self):
        response = self._dial('GET', self.location + '/deliveryAddresses', '')
        data = json.loads(response.read().decode('utf8'))

        return {'status': response.status, 'reason': response.reason, 'addresses': data['deliveryAddresses']}

    def charge(self, orderData):
        '''
        Example orderData:

orderData={
    "paymentAmount": 39.99,
    "currency": "EUR",
    "orderNumber": "ORD12345",
    "urlSet": {
        "successUrl": "https://www.examplewebshop.com/success",
        "cancelUrl": "https://www.examplewebshop.com/cancel",
        "notifyUrl": "https://www.examplewebshop.com/notify"
    },
    "locale": "en_US",
    "deliveryAddress": {
        "firstName": "Penny",
        "lastName": "Paytrail",
        "street": "Lutakonaukio 7",
        "postalCode": "40100",
        "postalOffice": "Jyväskylä",
        "country": "FI"
    },
    "products": [
        {
            "code": "PX923423",
            "name": "Book: How to implement PaytrailConnectAPI",
            "quantity": 1,
            "unitPrice": 39.99,
            "totalRowAmount": 39.99,
            "vatPercent": 24
        }
    ]
}
'''
        body = json.dumps({'payment': orderData})
        response = self._dial('POST', self.location + '/charges', body)
        data = response.read().decode('utf8')

        if data:
            data = json.loads(data)
            return {'status': response.status, 'reason': response.reason, 'payment': data['payment']}
        else:
            return {'status': response.status, 'reason': response.reason}


