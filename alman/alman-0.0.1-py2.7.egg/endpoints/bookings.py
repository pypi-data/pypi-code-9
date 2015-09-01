from ..apibits import *
from ..resources import *

class BookingsEndpoint(ApiEndpoint):
    
    def retrieve(self, booking_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "booking_id" : booking_id,
        }, params)
        method = ApiMethod("get", "/bookings/:booking_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)
        
    def delete(self, booking_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "booking_id" : booking_id,
        }, params)
        method = ApiMethod("delete", "/bookings/:booking_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)
        
    def update(self, booking_id, params={}, headers={}):
        params = ParamsBuilder.merge({
            "booking_id" : booking_id,
        }, params)
        method = ApiMethod("put", "/bookings/:booking_id", params, headers, self.parent)
        json = self.client.execute(method)
        return Booking(json, method, client=self.client)
