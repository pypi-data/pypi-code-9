from ..apibits import *

class Vacancy(ApiResource):

    @classmethod
    def retrieve(cls, vacancy_id, params={}, headers={}):
        res = cls.default_client().vacancies().retrieve(vacancy_id, params, headers)
        return res

    def refresh(self, params={}, headers={}):
        res = self.get_client().vacancies().retrieve(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def delete(self, params={}, headers={}):
        res = self.get_client().vacancies().delete(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def bookings(self):
        from ..endpoints import VacancyBookingsEndpoint
        return VacancyBookingsEndpoint(self.client, self)

    # Everything below here is used behind the scenes.
    def __init__(self, *args, **kwargs):
    	  super(Vacancy, self).__init__(*args, **kwargs)
    	  ApiResource.register_api_subclass(self, "vacancy")

    _api_attributes = {
        "created_at" : {},
        "created_at_rfc822" : {},
        "end_at" : {},
        "end_at_rfc822" : {},
        "id" : {},
        "object" : {},
        "start_at" : {},
        "start_at_rfc822" : {},
        "updated_at" : {},
        "updated_at_rfc822" : {},
    }
