from pyiso.base import BaseClient
from os import environ
from datetime import datetime
import pytz


class ISONEClient(BaseClient):
    NAME = 'ISONE'

    base_url = 'https://webservices.iso-ne.com/api/v1.1'
    TZ_NAME = 'America/New_York'

    fuels = {
        'Coal': 'coal',
        'Hydro': 'hydro',
        'Natural Gas': 'natgas',
        'Nuclear': 'nuclear',
        'Oil': 'oil',
        'Solar': 'solar',
        'Wind': 'wind',
        'Wood': 'biomass',
        'Refuse': 'refuse',
        'Landfill Gas': 'biogas',
    }

    def __init__(self, *args, **kwargs):
        super(ISONEClient, self).__init__(*args, **kwargs)
        try:
            self.auth = (environ['ISONE_USERNAME'], environ['ISONE_PASSWORD'])
        except KeyError:
            msg = 'Must define environment variables ISONE_USERNAME and ISONE_PASSWORD to use ISONE client.'
            raise RuntimeError(msg)

    def get_generation(self, latest=False, start_at=False, end_at=False, **kwargs):
        # set args
        self.handle_options(data='gen', latest=latest,
                            start_at=start_at, end_at=end_at, **kwargs)

        # set up storage
        raw_data = []
        parsed_data = []

        # collect raw data
        for endpoint in self.request_endpoints():
            # carry out request
            data = self.fetch_data(endpoint, self.auth)
            raw_data += data['GenFuelMixes']['GenFuelMix']

        # parse data
        for raw_dp in raw_data:
            # set up storage
            parsed_dp = {}

            # add values
            parsed_dp['timestamp'] = self.utcify(raw_dp['BeginDate'])
            parsed_dp['gen_MW'] = raw_dp['GenMw']
            parsed_dp['fuel_name'] = self.fuels[raw_dp['FuelCategory']]
            parsed_dp['ba_name'] = self.NAME
            parsed_dp['market'] = self.options['market']
            parsed_dp['freq'] = self.options['frequency']

            # add to full storage
            parsed_data.append(parsed_dp)

        return parsed_data

    def get_load(self, latest=False, start_at=False, end_at=False,
                 forecast=False, **kwargs):
        # set args
        self.handle_options(data='load', latest=latest, forecast=forecast,
                            start_at=start_at, end_at=end_at, **kwargs)

        # set up storage
        raw_data = []
        parsed_data = []

        # collect raw data
        for endpoint in self.request_endpoints():
            # carry out request
            data = self.fetch_data(endpoint, self.auth)

            # pull out data
            if 'FiveMinSystemLoads' in data.keys():
                raw_data += data['FiveMinSystemLoads']['FiveMinSystemLoad']
            elif 'FiveMinSystemLoad' in data.keys():
                raw_data += data['FiveMinSystemLoad']
            elif 'HourlyLoadForecasts' in data.keys():
                raw_data += data['HourlyLoadForecasts']['HourlyLoadForecast']
            else:
                raise ValueError('Could not parse ISONE load data %s' % data)

        # parse data
        now = pytz.utc.localize(datetime.utcnow())
        for raw_dp in raw_data:
            # set up storage
            parsed_dp = {}

            # add values
            parsed_dp['timestamp'] = self.utcify(raw_dp['BeginDate'])
            parsed_dp['load_MW'] = raw_dp['LoadMw']
            parsed_dp['ba_name'] = self.NAME
            parsed_dp['market'] = self.options['market']
            parsed_dp['freq'] = self.options['frequency']

            # add to full storage
            if self.options['forecast'] and parsed_dp['timestamp'] < now:
                # don't include past forecast data
                pass
            else:
                parsed_data.append(parsed_dp)

        return parsed_data

    def handle_options(self, **kwargs):
        # default options
        super(ISONEClient, self).handle_options(**kwargs)

        # handle market
        if not self.options.get('market'):
            if self.options['data'] == 'gen':
                # generation on n/a market
                self.options['market'] = self.MARKET_CHOICES.na
            else:
                # load on real-time 5-min or hourly forecast
                if self.options['forecast']:
                    self.options['market'] = self.MARKET_CHOICES.dam
                else:
                    self.options['market'] = self.MARKET_CHOICES.fivemin

        # handle frequency
        if not self.options.get('frequency'):
            if self.options['data'] == 'gen':
                # generation on n/a frequency
                self.options['frequency'] = self.FREQUENCY_CHOICES.na
            else:
                # load on real-time 5-min or hourly forecast
                if self.options['market'] == self.MARKET_CHOICES.dam:
                    self.options['frequency'] = self.FREQUENCY_CHOICES.dam
                else:
                    self.options['frequency'] = self.FREQUENCY_CHOICES.fivemin

    def request_endpoints(self):
        """Returns a list of endpoints to query, based on handled options"""
        # base endpoint
        if self.options['data'] == 'gen':
            base_endpoint = 'genfuelmix'
        elif self.options['market'] == self.MARKET_CHOICES.dam:
            base_endpoint = 'hourlyloadforecast'
        else:
            base_endpoint = 'fiveminutesystemload'

        # set up storage
        request_endpoints = []

        # handle dates
        if self.options['latest']:
            request_endpoints.append('/%s/current.json' % base_endpoint)

        elif self.options['start_at'] and self.options['end_at']:
            for date in self.dates():
                date_str = date.strftime('%Y%m%d')
                request_endpoints.append('/%s/day/%s.json' % (base_endpoint, date_str))

        else:
            msg = 'Either latest or forecast must be True, or start_at and end_at must both be provided.'
            raise ValueError(msg)

        # return
        return request_endpoints

    def fetch_data(self, endpoint, auth):
        url = self.base_url + endpoint
        response = self.request(url, auth=auth)
        return response.json()
