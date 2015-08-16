from ipware.ip import get_real_ip
from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from .client import IpApiClient

IPAPI_ALLOWED_COUNTRIES = getattr(settings, 'IPAPI_ALLOWED_COUNTRIES', [])


class CheckCountryCodeMiddleware(object):

    def process_request(self, request):

        if IPAPI_ALLOWED_COUNTRIES and not 'ipapi' in request.path:
            ip_address = request.GET.get('__ipapi__', get_real_ip(request))
            if ip_address:
                api = IpApiClient()
                country_code = api.get_country_code(ip_address=ip_address)
                if country_code not in IPAPI_ALLOWED_COUNTRIES:
                    return HttpResponsePermanentRedirect(reverse('ipapi-disabled', kwargs={
                        'ip_address': ip_address,
                        'country_code': country_code,
                    }))