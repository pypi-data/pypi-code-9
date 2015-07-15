import logging
import requests
import simplejson as json
import time
from six.moves.urllib.parse import urljoin
from ._version import __version__ as hestia_version

__all__ = ['HestiaApi']


class HestiaApi:

    __version__ = hestia_version

    def __init__(self, settings):
        """Initialize a new instance of the HestiaApi."""
        self.__log = logging.getLogger("HestiaApi")
        self.__settings = settings

    def record_solar_river_reading(self, installation_code, pv_output):
        """Record the readings from a Solar River inverter."""
        payload = {
            "date": str(pv_output.date_taken),
            "temp": pv_output.internal_temperature.value,
            "vpv1": pv_output.panel1_voltage.value,
            "ipv1": pv_output.panel1_dc_current.value,
            "iac": pv_output.grid_current.value,
            "vac": pv_output.grid_voltage.value,
            "fac": pv_output.grid_frequency.value,
            "pac": pv_output.output_power.value,
            "htotal": pv_output.working_hours_total.value,
            "etoday": pv_output.accumulated_energy_today.value,
            "etotal": pv_output.accumulated_energy_total.value
        }

        self.__log.debug('Posting %s' % json.dumps(payload))
        self.__post(
            'photovoltaic/%s/inverter/solar_river/readings' % installation_code,
            json.dumps(payload),
            {'content-type': 'application/json'})

    def record_emon(self, property_code, data):
        """Record the data from the EmonHub."""
        sent_at = int(time.time())
        data_string = json.dumps(data, separators=(',', ':'))
        payload = "data=" + data_string + "&sentat=" + str(sent_at)

        self.__post('property/%s/emon/readings' % property_code, payload,
                    {'content-type': 'application/x-www-form-urlencoded'})

    def status(self):
        """Get the status of hestia.io."""
        return self.__get('status', {'content-type': 'application/json'})

    def __post(self, path, payload, headers=None):
        if not headers:
            headers = {}

        headers['User-Agent'] = 'Hestia Python API/%s' % HestiaApi.__version__

        url = self.__remote_url(path)

        self.__log.debug('Sending POST request to %s' % url)
        r = requests.post(url,
                          timeout=5,
                          data=payload,
                          headers=headers,
                          auth=self.__authentication())
        self.__log.debug('Received server response %s' % r.status_code)
        return r.status_code

    def __get(self, path, headers=None):
        if not headers:
            headers = {}

        headers['User-Agent'] = 'Hestia Python API/%s' % HestiaApi.__version__

        url = self.__remote_url(path)

        self.__log.debug('Sending GET request to %s' % url)
        r = requests.get(url,
                         timeout=5,
                         headers=headers,
                         auth=self.__authentication())
        self.__log.debug('Received server response %s' % r.status_code)
        return r.status_code

    def __remote_url(self, path):
        root = 'https://www.hestia.io'
        if 'hestia_url' in self.__settings:
            root = self.__settings['hestia_url']
        return urljoin(root, path)

    def __authentication(self):
        return self.__settings['username'], self.__settings['password']
