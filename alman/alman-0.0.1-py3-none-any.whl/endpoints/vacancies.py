from ..apibits import *
from ..resources import *

class VacanciesEndpoint(ApiEndpoint):
    
    def retrieve(self, vacancy_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "vacancy_id" : vacancy_id,
        }, params)
        method = ApiMethod("get", "/vacancies/:vacancy_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Vacancy(json, method, client=self.client)
        
    def delete(self, vacancy_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "vacancy_id" : vacancy_id,
        }, params)
        method = ApiMethod("delete", "/vacancies/:vacancy_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Vacancy(json, method, client=self.client)
