from okta.framework.ApiClient import ApiClient
from okta.framework.Utils import Utils
from okta.models.event.Event import Event


class EventsClient(ApiClient):
    def __init__(self, base_url, api_token):
        ApiClient.__init__(self, base_url + '/api/v1/events', api_token)

    def get_events(self, limit=None, start_date=None, after=None, filter=None):
        params = {
            'limit': limit,
            'startDate': start_date,
            'after': after,
            'filter': filter
        }

        response = ApiClient.get_path(self, '/', params=params)
        return Utils.deserialize(response.text, Event)

    def get_events_url(self, url):
        response = ApiClient.get(url)
        return Utils.deserialize(response.text, Event)