import unirest
import json

class Lifecycle:

    def __init__(self, api_key):
        self.apiKey = api_key

    def getApiKey(self):
        return self.apiKey
    def identify(self, params):
        response = unirest.post("http://localhost:3400/v1/identify", headers={ "Content-Type": "application/json", "lifecycle-api-key": self.apiKey},
          params=json.dumps(params)
        )
        return response

    def track(self, event_id, unique_id):
        response = unirest.post("http://localhost:3400/v1/track", headers={ "Content-Type": "application/json", "lifecycle-api-key": self.apiKey},
          params=json.dumps({
            "event_id": event_id,
            "unique_id": unique_id
          })
        )
        return response
