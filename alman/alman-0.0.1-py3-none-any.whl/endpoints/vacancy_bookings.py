from ..apibits import *
from ..resources import *

class VacancyBookingsEndpoint(ApiEndpoint):
    
    def create(self, params={}, headers={}):
        method = ApiMethod("post", "/vacancies/:id/bookings", params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)
