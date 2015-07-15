import requests
try:
    #python 3?
    from urllib.parse import urlparse
except ImportError:
    #nope, python2
    from urlparse import urlparse
    
class SecretClient:
    
    def __init__(self, secretKey=None, url=None, test=None):
        
        if (not secretKey):
            raise ValueError("secretKey is a required paramter")

        self._secretKey = secretKey

        if (url):
            self._setBaseUrl(url)
        elif (test):
            self._setBaseUrl("https://api-test.withkash.com/v1");
        else:
            self._setBaseUrl("https://api.withkash.com/v1");

    def createAuthorization(self, customerId=None, amount=None):

        if (not customerId):
            raise ValueError("customerId is a required parameter");

        if (not amount):
            raise ValueError("amount is a required parameter");

        url = self._baseUrl + "/authorizations"
        params = {
            'customer_id': customerId,
            'amount': amount
        }
        response = requests.post(url, params)

        authorization_id = None

        if (response.ok) :
            authorization_id  = response.json()['authorization_id']
        else:
            self._raiseAPIError(response)
        
        return authorization_id
        
    
    def removeAuthorization(self, authorizationId=None):

        if (not authorizationId):
            raise ValueError("authorizationId is a required parameter")
        
        url = self._baseUrl + "/authorization/" + authorizationId
        response = requests.delete(url)
        
        if (response.ok) :
            return
        else:
            self._raiseAPIError(response)

            
    def createTransaction(self, authorizationId=None, amount=None):
        if (not authorizationId):
            raise ValueError("authorizationId is a required parameter")

        if (not amount):
            raise ValueError("amount is a required parameter");

        url = self._baseUrl + "/transactions"
        params = {
            'authorization_id': authorizationId,
            'amount': amount
        }
        response = requests.post(url, params)

        if (response.ok):
            return response.json()['transaction_id']
        else:
            self._raiseAPIError(response)
            
        
    def _setBaseUrl(self,url):
        res = urlparse(url);
        hostname = res.hostname
        port = ':' + str(res.port) if res.port else ''
        path = res.path or ''
        
        scheme = res.scheme
        baseUrl = scheme + "://" + self._secretKey + ':@' + hostname + port + path;

        self._baseUrl = baseUrl
            
    def _raiseAPIError(self, response):
        #if we got some json explaining things, include it, otherwise full text
        try:
            json = response.json()
        except ValueError:
            #otherwise just use the text
            raise Exception(str(response.status_code) + ' - ' + response.text)

        if ('message' in json):
            moreInfo = json.get('message')
        elif ('message' in json):
            moreInfo = json.get('error')
        else:
            moreInfo = str(json)

        raise Exception(str(response.status_code) + ' - ' + moreInfo)
