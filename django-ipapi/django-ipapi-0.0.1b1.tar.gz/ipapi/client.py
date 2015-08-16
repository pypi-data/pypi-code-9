# -*- coding: utf-8 -*-
import requests


class IpApiClient(object):
    """Creates an API client object

    """
    api_url = 'http://ip-api.com'
    format = 'json'

    def __init__(self):
        pass

    def request(self, method='GET', path=None, params=None):
        """Makes a request to the API with the given parameters

        :param method: the HTTP method to use
        :param path: the api path to request
        :param params: the parameters to be sent

        """
        # the api request result
        result = None
        url = '{}/{}/{}'.format(self.api_url, self.format, path)

        try:
            # send a request to the api server
            r = requests.request(
                method=method,
                url=url,
                params=params
            )
            # raise an exception if status code is not 200
            if r.status_code is not 200:
                raise Exception
            else:
                result = r.json()
        except requests.ConnectionError:
            self.error = 'API connection error.'
        except requests.HTTPError:
            self.error = 'An HTTP error occurred.'
        except requests.Timeout:
            self.error = 'Request timed out.'
        except Exception:
            self.error = 'An unexpected error occurred.'

        return result

    def _get_value(self, ip_address, field):
        """
        http://ip-api.com/json/208.80.152.201 =>
        {
            as: "AS14907 Wikimedia Foundation Inc.",
            city: "San Francisco",
            country: "United States",
            countryCode: "US",
            isp: "Wikimedia Foundation",
            lat: 37.7898,
            lon: -122.3942,
            org: "Wikimedia Foundation",
            query: "208.80.152.201",
            region: "CA",
            regionName: "California",
            status: "success",
            timezone: "America/Los_Angeles",
            zip: "94105"
        }
        """
        result = self.request(path=ip_address)
        return result.get(field) if result else None

    def get_country_code(self, ip_address):
        return self._get_value(ip_address, 'countryCode')


