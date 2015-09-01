from ..apibits import *
from ..resources import *

class CalendarVacanciesEndpoint(ApiEndpoint):
    
    def all(self, params={}, headers={}):
        method = ApiMethod("get", "/calendars/:id/vacancies", params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)
        
    def all_within(self, params={}, headers={}):
        method = ApiMethod("get", "/calendars/:id/vacancies/within", params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)
        
    def create(self, params={}, headers={}):
        method = ApiMethod("post", "/calendars/:id/vacancies", params, headers, self.parent)
        json = self.client.execute(method)
        return Vacancy(json, method, client=self.client)
        
    def create_range(self, params={}, headers={}):
        method = ApiMethod("post", "/calendars/:id/vacancies/range", params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)
        
    def delete_overlap(self, params={}, headers={}):
        method = ApiMethod("delete", "/calendars/:id/vacancies/overlap", params, headers, self.parent)
        json = self.client.execute(method)
        return ApiList(Vacancy, json, method, client=self.client)
