from ..apibits import *

class Calendar(ApiResource):

    @classmethod
    def all(cls, params={}, headers={}):
        res = cls.default_client().calendars().all(params, headers)
        return res

    @classmethod
    def retrieve(cls, calendar_id, params={}, headers={}):
        res = cls.default_client().calendars().retrieve(calendar_id, params, headers)
        return res

    @classmethod
    def update(cls, calendar_id, params={}, headers={}):
        res = cls.default_client().calendars().update(calendar_id, params, headers)
        return res

    @classmethod
    def create(cls, params={}, headers={}):
        res = cls.default_client().calendars().create(params, headers)
        return res

    def refresh(self, params={}, headers={}):
        res = self.get_client().calendars().retrieve(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def delete(self, params={}, headers={}):
        res = self.get_client().calendars().delete(self.id, params, headers)
        return self.refresh_from(res.json, res.api_method, res.client)

    def vacancies(self):
        from ..endpoints import CalendarVacanciesEndpoint
        return CalendarVacanciesEndpoint(self.client, self)

    # Everything below here is used behind the scenes.
    def __init__(self, *args, **kwargs):
    	  super(Calendar, self).__init__(*args, **kwargs)
    	  ApiResource.register_api_subclass(self, "calendar")

    _api_attributes = {
        "created_at" : {},
        "created_at_rfc822" : {},
        "details" : {},
        "id" : {},
        "name" : {},
        "object" : {},
        "updated_at" : {},
        "updated_at_rfc822" : {},
    }
