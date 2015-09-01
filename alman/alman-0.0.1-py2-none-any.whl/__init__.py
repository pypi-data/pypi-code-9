
API_KEY = None

API_BASE = "http://almanapi.com/api/v0"

from .clients import DefaultClient
from .resources import (Calendar, Vacancy, Booking, )
from .endpoints import (CalendarsEndpoint, CalendarVacanciesEndpoint, VacanciesEndpoint, VacancyBookingsEndpoint, BookingsEndpoint, )

def default_client():
	return DefaultClient(API_KEY)