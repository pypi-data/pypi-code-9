from ..apibits import *
from ..resources import *

class CalendarsEndpoint(ApiEndpoint):
    
    def all(self, params={}, headers={}):
        method = ApiMethod("get", "/calendars", params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Calendar, json, method, client=self.client)
        
    def retrieve(self, calendar_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "calendar_id" : calendar_id,
        }, params)
        method = ApiMethod("get", "/calendars/:calendar_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)
        
    def delete(self, calendar_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "calendar_id" : calendar_id,
        }, params)
        method = ApiMethod("delete", "/calendars/:calendar_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)
        
    def update(self, calendar_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "calendar_id" : calendar_id,
        }, params)
        method = ApiMethod("put", "/calendars/:calendar_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)
        
    def create(self, params={}, headers={}):
        method = ApiMethod("post", "/calendars", params, headers, self.parent)
        json = self.client.execute(method)
        return Calendar(json, method, client=self.client)
